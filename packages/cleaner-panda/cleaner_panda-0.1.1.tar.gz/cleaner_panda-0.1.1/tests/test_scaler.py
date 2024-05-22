import unittest
import pandas as pd
import numpy as np

# Import the functions from your module
from cleaner_panda.scaler import (
    log_transform_data,
    maxabs_scale_data,
    normalize_data,
    normalize_vectors,
    power_transform_data,
    robust_scale_data,
    standardize_data
)

class TestDataScaling(unittest.TestCase):
    
    def setUp(self):
        # Create a sample dataframe for testing
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': [100, 200, 300, 400, 500]
        })
    
    def test_log_transform_data(self):
        print("\nBefore log transforming the data:\n")
        print(self.data)
        
        result = log_transform_data(self.data)
        
        print("\nAfter log transforming the data:\n")
        print(result)
        
        expected = np.log1p(self.data)
        self.assertTrue(np.allclose(result, expected))
    
    def test_maxabs_scale_data(self):
     print("\nBefore maxabs scaling the data:\n")
     print(self.data)
    
     result = maxabs_scale_data(self.data)
    
     print("\nAfter maxabs scaling the data:\n")
     print(result)
    
    # Calculate the expected minimum values for each feature after scaling
     expected_min = self.data.min() / self.data.abs().max()
    
     self.assertTrue(np.allclose(result.max(), 1))
     self.assertTrue(np.allclose(result.min(), expected_min))

    def test_normalize_data(self):
        print("\nBefore normalizing the data:\n")
        print(self.data)
        
        result = normalize_data(self.data)
        
        print("\nAfter normalizing the data:\n")
        print(result)
        
        self.assertTrue(np.allclose(result.min(), 0))
        self.assertTrue(np.allclose(result.max(), 1))
        
    def test_normalize_vectors(self):
        print("\nBefore normalizing vectors:\n")
        print(self.data)
        
        result = normalize_vectors(self.data)
        
        print("\nAfter normalizing vectors:\n")
        print(result)
        
        norms = np.linalg.norm(self.data, axis=1)
        expected = self.data.div(norms, axis=0)
        self.assertTrue(np.allclose(result, expected))

    def test_power_transform_data(self):
        print("\nBefore power transforming the data:\n")
        print(self.data)
        
        result = power_transform_data(self.data)
        
        print("\nAfter power transforming the data:\n")
        print(result)
        
        self.assertTrue(result.shape, self.data.shape)  # Ensure shape is the same
        # For specific numerical checks, more detailed checks might be required

    def test_robust_scale_data(self):
        print("\nBefore robust scaling the data:\n")
        print(self.data)
        
        result = robust_scale_data(self.data)
        
        print("\nAfter robust scaling the data:\n")
        print(result)
        
        median = self.data.median()
        iqr = self.data.quantile(0.75) - self.data.quantile(0.25)
        scaled_median = (self.data - median) / iqr
        self.assertTrue(np.allclose(result.median(), scaled_median.median()))

    def test_standardize_data(self):
        print("\nBefore standardizing the data:\n")
        print(self.data)
        
        result = standardize_data(self.data)
        
        print("\nAfter standardizing the data:\n")
        print(result)
        
        self.assertTrue(np.allclose(result.mean(), 0, atol=1e-7))
        self.assertTrue(np.allclose(result.std(), 1, atol=1e-7))

if __name__ == '__main__':
    unittest.main()