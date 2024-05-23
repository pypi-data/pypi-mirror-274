"""
Network Simulation Module
Developed by Alexandre Levert, NBC (National Bank du Canada)
May 2024

This module simulates network latency based on trading activity and high-activity periods identified
by the VolumeAnalyser. It uses the DataFrame of trading data to adjust timestamps based on calculated latencies.
"""

from pythonAPI.runnbboquote import OneTickQueryRunner
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from modules.volume_analyser import VolumeAnalyser
from modules.cross_over_controller import CrossOverController

MINUTES_IN_HOUR = 60
PERCENTAGE = 100
LATENCY_FACTOR = 1.0
BIN_FOR_PLOT = 50
ALPHA_FOR_PLOT = 0.7

class NetworkSimulator:
    def __init__(self, from_date, to_date, symbol, batch_size, timezone, volume_analyser_min, volume_analyser_percentile,
                 min_latency_ns, max_latency_ns, mean_latency_ns, std_dev_ns, jitter_factor,username, password,
                 onetick_dir="/home/ubuntu/onetick-onboarding/onetick",working_dir="/home/ubuntu/projects/onetick_latency",
                 plot_latency=False,plot_quotes=False, show_metrics=True, otq_file_path=None,
                 save_to_pickle=False, pickle_path=None):
        """
        Initialize the Network Simulator with all parameters needed for simulation.

        Parameters:
        - All necessary parameters for setting up and running the latency simulation.
        """
        self.plot_latency = plot_latency
        self.plot_quotes = plot_quotes
        self.show_metrics = show_metrics
        self.query_runner = OneTickQueryRunner(username, password, onetick_dir, working_dir)
        self.df = self.query_runner.run_market(
            from_date=from_date,
            to_date=to_date,
            symbol=symbol,
            batch_size=batch_size,
            timezone=timezone,
            otq_file_path=otq_file_path,
            save_to_pickle=save_to_pickle,
            pickle_path=pickle_path
        )
        self.volume_analyser = VolumeAnalyser(self.df, volume_analyser_min, percentile=volume_analyser_percentile)

        self.latency_params = {
            'min_latency_ns': min_latency_ns,
            'max_latency_ns': max_latency_ns,
            'mean_latency_ns': mean_latency_ns,
            'std_dev_ns': std_dev_ns,
            'high_latency_periods': self.get_high_latency_periods(),
            'jitter_factor': jitter_factor
        }

        print("\n--------------------LATENCY PARAMETERS------------------------------")
        print("Initial Latency Parameters Set:")
        for key, value in self.latency_params.items():
            print(f"  {key}: {value}\n")

        self.cross_control = CrossOverController(self.df)


    def get_high_latency_periods(self):
        """
        Retrieve high latency periods from the volume analyzer and format them for latency simulation.

        Returns:
        - list of tuples: Each tuple contains start hour, end hour, and percentage increase in latency.
        """
        high_activity_periods = self.volume_analyser.find_recurrent_high_activity_periods()
        latency_periods = []

        if self.plot_quotes:
            self.volume_analyser.plot_quotes_over_time()

        print("----------------INTERVAL OF HIGH QUOTE COUNT-----------------------")
        for period in high_activity_periods:

            start_hour = pd.to_datetime(period['Start']).hour + pd.to_datetime(period['Start']).minute / MINUTES_IN_HOUR
            end_hour = pd.to_datetime(period['End']).hour + pd.to_datetime(period['End']).minute / MINUTES_IN_HOUR
            latency_periods.append((start_hour, end_hour, period['Delta from Mean (%)']))

            print(f"\nFrom {period['Start']} to {period['End']} with {period['quote Count']} quotes, Average Delta: {period['Delta from Mean (%)']:.2f}%")

        return latency_periods


    def generate_latency_factors(self):
        """
        Precompute latency factors for each timestamp in the DataFrame based on high latency periods.
        """
        if self.df.empty or 'Time' not in self.df.columns:
            raise ValueError("DataFrame is empty or missing required 'Time' column.")

        self.df['hour_of_day'] = self.df['Time'].dt.hour + self.df['Time'].dt.minute / MINUTES_IN_HOUR
        self.df['latency_factor'] = LATENCY_FACTOR
        for start, end, increase in self.latency_params['high_latency_periods']:
            self.df.loc[(self.df['hour_of_day'] >= start) & (self.df['hour_of_day'] < end), 'latency_factor'] += increase / PERCENTAGE


    def report_simulation_metrics(self):
        """
        Report metrics such as mean and standard deviation of the simulated latencies.
        """
        simulated_mean = np.mean(self.df['latency_ns'])
        simulated_std = np.std(self.df['latency_ns'])
        print("\n----------------------SIMULATION METRICS---------------------------------\n")
        print(f"Simulated Mean Latency: {simulated_mean} ns")
        print(f"Simulated Standard Deviation: {simulated_std} ns")


    def adjust_timestamps(self):
        """
        Adjust the timestamps in the DataFrame by applying the generated latency values,
        ensuring each timestamp reflects realistic network delays while maintaining specified statistical properties.
        """
        self.generate_latency_factors()

        # Parameters
        specified_mean = self.latency_params['mean_latency_ns']
        specified_std = self.latency_params['std_dev_ns']
        jitter_factor = self.latency_params['jitter_factor']

        # Generate base latency values from a normal distribution
        base_latency = np.random.normal(specified_mean, specified_std, size=len(self.df))

        # Apply jitter
        jitter = np.random.normal(0, specified_std * jitter_factor, size=len(self.df))

        # Adjusted latencies incorporating volume-based factors
        adjusted_latencies = base_latency * self.df['latency_factor'] + jitter

        # Normalize the adjusted latencies to have the specified mean and standard deviation
        normalized_latencies = specified_std * ((adjusted_latencies - np.mean(adjusted_latencies)) / np.std(adjusted_latencies)) + specified_mean

        # Apply the calculated latencies to the DataFrame, clipping to specified ranges
        self.df['latency_ns'] = np.clip(normalized_latencies, self.latency_params['min_latency_ns'], self.latency_params['max_latency_ns']).astype(int)

        # Adjust timestamps based on the calculated latencies
        self.df['latency_ns'] = np.round(normalized_latencies).astype(int)
        self.df['adjusted_time'] = self.df['Time'] + pd.to_timedelta(self.df['latency_ns'], unit='ns')

        #option set for plotting latency distribution graph
        if self.plot_latency:
            self.plot_latency_distribution()

        if self.show_metrics:
            self.report_simulation_metrics()

        #module control for timestamp crossovers
        self.cross_control.detect_timestamp_crossovers()


    def plot_latency_distribution(self):
        """
        Plot the distribution of the simulated latency values to visualize the impact of network latency.
        """
        plt.hist(self.df['latency_ns'], bins=BIN_FOR_PLOT, color='blue', alpha=ALPHA_FOR_PLOT)
        plt.title('Latency Distribution')
        plt.xlabel('Latency (ns)')
        plt.ylabel('Frequency')
        plt.show()


if __name__ == '__main__':
    simulator = NetworkSimulator(
        from_date='2024-05-08',
        to_date='2024-05-11',
        symbol='QQQT',
        batch_size=20,
        timezone='America/New_York',
        volume_analyser_min=5,
        volume_analyser_percentile=80,
        min_latency_ns=40,
        max_latency_ns=1200,
        mean_latency_ns=150,
        std_dev_ns=20,
        jitter_factor=0.15,
        username='user',
        password='pass',
        plot_latency=True,
        plot_quotes=True,
        show_metrics=True
    )
    simulator.adjust_timestamps()
    print(simulator.df.tail(20))

