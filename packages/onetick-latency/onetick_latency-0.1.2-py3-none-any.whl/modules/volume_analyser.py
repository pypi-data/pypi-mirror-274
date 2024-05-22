"""
Volume Analyser Module
Developed by Alexandre Levert, NBC (National Bank du Canada)
May 2024

This module analyses a pandas DataFrame of NBBO quotes and determines intervals of high trading activity.
It utilizes a rolling window approach to calculate trade counts and deviations from mean activity over
specified time intervals. These analyses help identify potential periods of network latency or trading volatility,
which are crucial for performance tuning and risk management in financial trading systems.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

PERCENTAGE = 100
SECONDS_IN_HOUR = 3600
SECONDS_IN_MIN = 60
FIG_X = 12
FIG_Y = 6
FIG_ROTATION = 45

class VolumeAnalyser:
    def __init__(self, df, minutes_rolling, percentile=80):

        #Check if necessary columns are present in dataframe
        if 'SIZE' not in df.columns or 'Time' not in df.columns:

            raise ValueError("DataFrame must contain 'SIZE' and 'Time' columns for volume analysis.")

        #Check if dataframe is empty
        if df.empty:
            raise ValueError("The provided DataFrame is empty.")

        self.df = df.copy()
        try:
            self.df['Time'] = pd.to_datetime(self.df['Time'])  # Ensure 'Time' is in datetime format
        except Exception as e:
            raise ValueError("Error converting 'Time' column to datetime format:", e)

        self.df.set_index('Time', inplace=True)  # Set 'Time' as index for rolling operation

        self.minutes_rolling = minutes_rolling
        self.percentile = percentile

    def calculate_quote_thresholds(self):
        #Calculate quote counts within the rolling window specified
        try:
            quote_counts = self.df['SIZE'].rolling(f'{self.minutes_rolling}T', closed='right').count()
        except Exception as e:
            raise Exception("Failed to calculate rolling quote counts:", e)

        if quote_counts.empty:
            raise ValueError("No quote counts were calculated, possibly due to insufficient data.")

        mean_quote_count = quote_counts.mean()
        return mean_quote_count

    def analyze_high_activity_periods(self):

        """Identify periods with high trading activity based on quote count within a rolling window."""

        self.df['Rolling quote Count'] = self.df['SIZE'].rolling(f'{self.minutes_rolling}T', closed='right').count()

        mean_quote_count = self.calculate_quote_thresholds()

        self.df['Delta from Mean (%)'] = ((self.df['Rolling quote Count'] - mean_quote_count) / mean_quote_count) * PERCENTAGE
        count_threshold = np.percentile(self.df['Rolling quote Count'].dropna(), self.percentile)
        high_activity_periods = self.df[self.df['Rolling quote Count'] > count_threshold].copy()
        return high_activity_periods.reset_index()

    def find_recurrent_high_activity_periods(self):
        periods = self.analyze_high_activity_periods()
        periods['Seconds'] = periods['Time'].apply(lambda x: x.hour * SECONDS_IN_HOUR + x.minute * SECONDS_IN_MIN + x.second)
        periods.sort_values('Seconds', inplace=True)
        merged = []

        for _, row in periods.iterrows():
            if not merged or merged[-1]['End Seconds'] < row['Seconds'] - (self.minutes_rolling*SECONDS_IN_MIN):
                merged.append({
                    'Start': row['Time'],
                    'End': row['Time'],
                    'End Seconds': row['Seconds'],
                    'quote Count': row['Rolling quote Count'],
                    'Delta from Mean (%)': row['Delta from Mean (%)']
                })
            else:
                if row['Seconds'] > merged[-1]['End Seconds']:
                    merged[-1]['End'] = row['Time']
                    merged[-1]['End Seconds'] = row['Seconds']
                if row['Time'] > merged[-1]['End']:
                    merged[-1]['quote Count'] = row['Rolling quote Count']  # Reset the count to the latest window count

        for m in merged:
            m['Start'] = m['Start'].strftime('%H:%M')
            m['End'] = m['End'].strftime('%H:%M')
        merged.sort(key=lambda x: -x['Delta from Mean (%)'])
        return merged

    def plot_quotes_over_time(self):
        """Plot the distribution of quotes over time based on rolling data."""
        plt.figure(figsize=(FIG_X, FIG_Y))
        plt.plot(self.df.index, self.df['Rolling quote Count'], linestyle='-')
        plt.title(f'Number of quotes Over Time (Rolling {self.minutes_rolling} Minutes)')
        plt.xlabel('Time')
        plt.ylabel('Number of quotes')
        plt.grid(True)
        plt.xticks(rotation=FIG_ROTATION)
        plt.tight_layout()
        plt.show()

    def analyze_volume(self): #only for dev, not in final
        try:
            mean_quotes, quote_thresholds = self.calculate_quote_thresholds()
            print(f"Mean quotes per {self.minutes_rolling}-min Interval:", mean_quotes)
            print("quote Thresholds:", quote_thresholds)
            recurrent_periods = self.find_recurrent_high_activity_periods()
            print("Filtered High Activity Intervals:")
            for period in recurrent_periods:
                print(f"From {period['Start']} to {period['End']} with {period['quote Count']} quotes, Average Delta: {period['Delta from Mean (%)']:.2f}%")
            self.plot_quotes_over_time()
        except Exception as e:
            print("An error occurred during volume analysis:", e)