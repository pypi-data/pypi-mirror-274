import unittest
import pandas as pd
from cleaner_panda.categorical_encoder import label_encoding, one_hot_encoding, ordinal_encoding, binary_encoding, target_encoding

class TestEncodingMethods(unittest.TestCase):

    def setUp(self):
        # Sample DataFrame for testing
        self.data = pd.DataFrame({
            'color': ['red', 'blue', 'green', 'blue', 'red'],
            'size': ['S', 'M', 'L', 'M', 'S'],
            'price': [10, 20, 30, 20, 10]
        })

    def test_label_encoding(self):
        df = self.data.copy()
        print("Before label encoding:\n")
        print(df)
        
        result = label_encoding(df, 'color')
        
        print("\nAfter label encoding:\n")
        print(result)

    def test_one_hot_encoding(self):
        df = self.data.copy()
        print("\nBefore one-hot encoding:\n")
        print(df)
        
        result = one_hot_encoding(df, 'color')
        
        print("\nAfter one-hot encoding:\n")
        print(result)

    def test_ordinal_encoding(self):
        df = self.data.copy()
        print("\nBefore ordinal encoding:\n")
        print(df)
        
        result = ordinal_encoding(df, 'size')
        
        print("\nAfter ordinal encoding:\n")
        print(result)

    def test_binary_encoding(self):
        df = self.data.copy()
        print("\nBefore binary encoding:\n")
        print(df)
        
        result = binary_encoding(df, 'color')
        
        print("\nAfter binary encoding:\n")
        print(result)

    def test_target_encoding(self):
        df = self.data.copy()
        print("\nBefore target encoding:\n")
        print(df)
        
        result = target_encoding(df, 'color', 'price')
        
        print("\nAfter target encoding:\n")
        print(result)

if __name__ == '__main__':
    unittest.main()