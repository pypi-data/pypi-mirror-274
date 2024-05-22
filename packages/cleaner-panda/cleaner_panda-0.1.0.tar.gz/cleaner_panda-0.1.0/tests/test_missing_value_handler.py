import unittest
import pandas as pd
import datetime
from cleaner_panda.missing_value_handler import MissingValueHandler


class TestMissingValueHandler(unittest.TestCase):

    def setUp(self):
        self.handler = MissingValueHandler()
        self.data = {
            'numeric': [1, 2, None, 4],
            'string': ['a', None, 'c', 'd'],
            'datetime': [datetime.datetime(2023, 1, 1), None, datetime.datetime(2023, 1, 3),
                         datetime.datetime(2023, 1, 4)]
        }
        self.df = pd.DataFrame(self.data)

    def test_replace_mean(self):
        column = 'numeric'
        df_result = self.handler.replace_mean(self.df.copy(), column)
        print("\n\nREPLACE MEAN TEST")
        print("-" * 60)
        print("\nBefore Replacing Mean:")
        print(self.df)
        print(f"\nAfter Replacing Mean for column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_replace_median(self):
        column = 'numeric'
        df_result = self.handler.replace_median(self.df.copy(), column)
        print("\n\nREPLACE MEDIAN TEST")
        print("-" * 60)
        print("\nBefore Replacing Median:")
        print(self.df)
        print(f"\nAfter Replacing Median for column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_replace_constant(self):
        column = 'numeric'
        df_result = self.handler.replace_constant(self.df.copy(), column)
        print("\n\nREPLACE CONSTANT TEST (Numeric)")
        print("-"*60)
        print("\nBefore Replacing Constant:")
        print(self.df)
        print(f"\nAfter Replacing Constant for column '{column}':")
        print(df_result)
        print("-" * 60)

        column = 'string'
        df = self.df.copy()
        df['string'] = df['string'].astype(str)
        df_result = self.handler.replace_constant(df, column)
        print("\n\nREPLACE CONSTANT TEST (String)")
        print("-"*60)
        print("\nBefore Replacing Constant:")
        print(df)
        print(f"\nAfter Replacing Constant for column '{column}':")
        print(df_result)
        print("-" * 60)

        column = 'datetime'
        df_result = self.handler.replace_constant(self.df.copy(), column)
        print("\n\nREPLACE CONSTANT TEST (Datetime)")
        print("-"*60)
        print("\nBefore Replacing Constant:")
        print(self.df)
        print(f"\nAfter Replacing Constant for column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_replace_remove_row(self):
        column = 'numeric'
        df_result = self.handler.replace_remove_row(self.df.copy(), column)
        print("\n\nREPLACE REMOVE ROW TEST")
        print("-" * 60)
        print("\nBefore Removing Rows:")
        print(self.df)
        print(f"\nAfter Removing Rows with NaNs in column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_replace_remove_column(self):
        column = 'numeric'
        df_result = self.handler.replace_remove_column(self.df.copy(), column)
        print("\n\nREPLACE REMOVE COLUMN TEST")
        print("-" * 60)
        print("\nBefore Removing Column:")
        print(self.df)
        print(f"\nAfter Removing Column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_replace_forward_backward(self):
        column = 'numeric'
        df_result = self.handler.replace_forward_backward(self.df.copy(), column)
        print("\n\nREPLACE FORWARD BACKWARD TEST")
        print("-" * 60)
        print("\nBefore Forward/Backward Fill:")
        print(self.df)
        print(f"\nAfter Forward/Backward Fill for column '{column}':")
        print(df_result)
        print("-" * 60)


if __name__ == '__main__':
    unittest.main()
