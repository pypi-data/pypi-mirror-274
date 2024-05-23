import onetick.query as otq
import os
import pandas as pd
import time
import datetime as dt
import pytz

class OneTickQueryRunner:

    def __init__(self, username_authentication, password_authentication,onetick_dir, working_dir, context="DEFAULT"):
        self.context = context
        self.onetick_dir = onetick_dir
        self.working_dir = working_dir
        self.onetick_lib = otq.OneTickLib(None)
        self.username_authentication = self.onetick_lib.set_username_for_authentication(username_authentication)
        self.password = self.onetick_lib.set_password(password_authentication)
        self.env = os.environ["ONE_TICK_CONFIG"] = f"{self.onetick_dir}/client_data/config/one_tick_config.txt"  # point to OneTick main config file on your local machine


    def run_query(self, query, query_timezone, params, save_to_pickle, pickle_path):
        current_time = dt.datetime.now(pytz.timezone(query_timezone))
        print(f"{current_time}: run_query: context: {self.context}: starting")

        tic = time.time()
        query_result = otq.run(
            query,
            username=self.username_authentication,
            context=self.context,
            query_params=params,
            timezone=query_timezone,
            time_as_nsec=True
        )
        toc = time.time()
        df = self.print_query_result(query_result, save_to_pickle, pickle_path)
        print(f"{current_time}: run_query: query finished in {toc - tic:.2f} seconds.\n")
        return df

    def print_query_result(self, query_result, save_to_pickle, pickle_path):
        if not query_result:
            return

        full_symbol_names_sorted = sorted(query_result, key=lambda s: s.name)
        for symbol_data in full_symbol_names_sorted:
            df = pd.DataFrame(query_result[symbol_data])
            if not df.empty:
                symbol = self.extract_symbol(symbol_data.name)
                if symbol:
                    df["Symbol"] = symbol
                    print(f"Data for {symbol}:\n{df.head(30)}\n")
                    if save_to_pickle:
                        df.to_pickle(f"{pickle_path}/{symbol}_query_result.pkl")
        return df

    def extract_symbol(self, name):
        return name.split("::")[-1] if "::" in name else name

    def run_market(self, from_date, to_date, symbol, batch_size, timezone, otq_file_path=None, save_to_pickle=True, pickle_path=None):
        if otq_file_path is None:
            otq_file_path = f"{self.onetick_dir}/client_data/otqs/NBBO.otq::soni"  # default OTQ file path
        if pickle_path is None:
            pickle_path = f"{self.working_dir}/modules"  # default pickle save path

        params = {
            "START_TIME": from_date.replace('-', '') + "000000",
            "END_TIME": to_date.replace('-', '') + "235959",
            "SYMBOL_PATTERN": symbol,
            "BATCH_SIZE": str(batch_size),
            "time_zone": timezone
        }
        df = self.run_query(query=otq_file_path, params=params, query_timezone=timezone, save_to_pickle=save_to_pickle, pickle_path=pickle_path)
        print("Success for HITS JOB\n")


        return df