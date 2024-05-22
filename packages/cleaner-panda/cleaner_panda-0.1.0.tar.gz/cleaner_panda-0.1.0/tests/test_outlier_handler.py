import unittest
import pandas as pd
import numpy as np
from cleaner_panda.outlier_handler import OutlierHandler, identify_outliers_zscore, handle_outliers_zscore, winsorize_data

class TestOutlierHandler(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 100],  # Outlier at 100
            'B': [10, 20, 30, 40, 50, 60],
            'C': [100, 200, 300, 400, 500, 600]
        })
        self.handler = OutlierHandler()

    def test_identify_outliers_iqr(self):
        print("Before identify outliers using IQR:\n")
        print(self.data)
        
        result = self.handler.identify_outliers_iqr(self.data, 'A')
        
        print("\nAfter identify outliers using IQR:\n")
        print(result)

    def test_handle_outliers_iqr_remove(self):
        print("\nBefore handling outliers using IQR (remove):\n")
        print(self.data)
        
        result = self.handler.handle_outliers_iqr(self.data, 'A')
        
        print("\nAfter handling outliers using IQR (remove):\n")
        print(result)

    def test_handle_outliers_iqr_replace(self):
        print("\nBefore handling outliers using IQR (replace):\n")
        print(self.data)
        
        result = self.handler.handle_outliers_iqr(self.data, 'A', replacement='median')
        
        print("\nAfter handling outliers using IQR (replace):\n")
        print(result)

    def test_identify_outliers_zscore(self):
        print("\nBefore identify outliers using Z-score:\n")
        print(self.data['A'])
        
        result = identify_outliers_zscore(self.data['A'])
        
        print("\nAfter identify outliers using Z-score:\n")
        print(result)

    def test_handle_outliers_zscore_remove(self):
        print("\nBefore handling outliers using Z-score (remove):\n")
        print(self.data['A'])
        
        result = handle_outliers_zscore(self.data['A'])
        
        print("\nAfter handling outliers using Z-score (remove):\n")
        print(result)

    def test_handle_outliers_zscore_replace(self):
        print("\nBefore handling outliers using Z-score (replace):\n")
        print(self.data['A'])
        
        result = handle_outliers_zscore(self.data['A'], replacement='median')
        
        print("\nAfter handling outliers using Z-score (replace):\n")
        print(result)

    def test_winsorize_data(self):
        print("\nBefore winsorizing the data:\n")
        print(self.data['A'])
        
        result = winsorize_data(self.data['A'])
        
        print("\nAfter winsorizing the data:\n")
        print(result)

if __name__ == '__main__':
    unittest.main()