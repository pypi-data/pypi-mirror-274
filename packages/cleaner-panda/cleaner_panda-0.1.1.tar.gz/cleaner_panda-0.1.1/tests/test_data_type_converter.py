import unittest
import pandas as pd
from cleaner_panda.data_type_converter import DataTypeConverter


class TestDataTypeConverter(unittest.TestCase):

    def setUp(self):
        self.converter = DataTypeConverter()
        self.data = {
            'numeric_str': ['1', '2', '3', 'invalid'],
            'category_str': ['apple', 'banana', 'apple', 'orange']
        }
        self.df = pd.DataFrame(self.data)

    def test_convert_to_numeric(self):
        column = 'numeric_str'
        df_result = self.converter.convert_to_numeric(self.df.copy(), column)
        print("\n\nCONVERT TO NUMERIC TEST")
        print("-" * 60)
        print("\nBefore Converting to Numeric:")
        print(self.df)
        print(f"\nAfter Converting to Numeric for column '{column}':")
        print(df_result)
        print("-" * 60)

    def test_convert_to_categorical(self):
        column = 'category_str'
        df_result = self.converter.convert_to_categorical(self.df.copy(), column)
        print("\n\nCONVERT TO CATEGORICAL TEST")
        print("-" * 60)
        print("\nBefore Converting to Categorical:")
        print(self.df)
        print(f"\nAfter Converting to Categorical for column '{column}':")
        print(df_result)
        print("-" * 60)


if __name__ == '__main__':
    unittest.main()
