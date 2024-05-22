import unittest
import pandas as pd
from datetime import datetime
from cleaner_panda.date_time_handler import DateTimeHandler


class TestDateTimeHandler(unittest.TestCase):

    def setUp(self):
        self.handler = DateTimeHandler()
        self.data = {
            'date': [
                datetime(2023, 1, 1, 12, 0, 0),
                datetime(2023, 1, 2, 13, 30, 0),
                datetime(2023, 1, 3, 15, 45, 0),
                pd.NaT
            ]
        }
        self.df = pd.DataFrame(self.data)

    def test_calculate_datetime_differences(self):
        column = 0
        df_result = self.handler.calculate_datetime_differences(self.df.copy(), column)
        print("\n\nCALCULATE DATETIME DIFFERENCES TEST")
        print("-"*60)
        print("\nBefore Calculating Datetime Differences:")
        print(self.df)
        print(f"\nAfter Calculating Datetime Differences for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_convert_date_to_strings(self):
        column = 0
        df_result = self.handler.convert_date_to_strings(self.df.copy(), column)
        print("\n\nCONVERT DATE TO STRINGS TEST")
        print("-" * 60)
        print("\nBefore Converting Date to Strings:")
        print(self.df)
        print(f"\nAfter Converting Date to Strings for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_convert_datetime_to_different_timezones(self):
        column = 0
        df_result = self.handler.convert_datetime_to_different_timezones(self.df.copy(), column, from_tz='UTC',
                                                                         to_tz='America/New_York')
        print("\n\nCONVERT DATETIME TO DIFFERENT TIMEZONES TEST")
        print("-" * 60)
        print("\nBefore Converting Datetime to Different Timezones:")
        print(self.df)
        print(f"\nAfter Converting Datetime to Different Timezones for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_extract_components(self):
        column = 0
        df_result = self.handler.extract_components(self.df.copy(), column)
        print("\n\nCONVERT DATETIME TO DIFFERENT TIMEZONES TEST")
        print("-" * 60)
        print("\nBefore Extracting Components:")
        print(self.df)
        print(f"\nAfter Extracting Components for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_handle_irregular_time_intervals(self):
        column = 0
        df_result = self.handler.handle_irregular_time_intervals(self.df.copy(), column)
        print("\n\nHANDLE IRREGULAR TIME INTERVALS TEST")
        print("-" * 60)
        print("\nBefore Handling Irregular Time Intervals:")
        print(self.df)
        print(f"\nAfter Handling Irregular Time Intervals for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_reformat_date(self):
        column = 0
        df_result = self.handler.reformat_date(self.df.copy(), column)
        print("\n\nREFORMAT DATE TEST")
        print("-" * 60)
        print("\nBefore Reformatting Date:")
        print(self.df)
        print(f"\nAfter Reformatting Date for column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)

    def test_shift_time(self):
        column = 0
        shift_value = 1
        unit = 'days'
        df_result = self.handler.shift_time(self.df.copy(), column, shift_value, unit)
        print("\n\nSHIFT TIME TEST")
        print("-" * 60)
        print("\n\nBefore Shifting Times:")
        print(self.df)
        print(f"\nAfter Shifting Times for {shift_value} {unit} to column '{self.df.columns[column]}':")
        print(df_result)
        print("-" * 60)


if __name__ == '__main__':
    unittest.main()
