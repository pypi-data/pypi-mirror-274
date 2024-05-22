from typing import Union
import pandas as pd
from scipy import stats
import numpy as np
class OutlierHandler:
    def __init__(self) -> None:
        pass
    
    def identify_outliers_iqr(self, dataframe: pd.DataFrame, column: str, threshold: float = 1.5) -> pd.DataFrame:
        if column not in dataframe.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        Q1 = dataframe[column].quantile(0.25)
        Q3 = dataframe[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        outliers = dataframe[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound)]
        return outliers
    
    def handle_outliers_iqr(self, dataframe: pd.DataFrame, column: str, threshold: float = 1.5, replacement: Union[None, float, int, str] = None) -> pd.DataFrame:
        if column not in dataframe.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame.")
        
        Q1 = dataframe[column].quantile(0.25)
        Q3 = dataframe[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        if replacement is None:
            dataframe = dataframe[(dataframe[column] >= lower_bound) & (dataframe[column] <= upper_bound)]
        else:
            dataframe.loc[(dataframe[column] < lower_bound) | (dataframe[column] > upper_bound), column] = replacement
        
        return dataframe
    

    # Identify outliers using Z-score method
def identify_outliers_zscore(data, threshold=3):
    z_scores = np.abs(stats.zscore(data))
    outliers = z_scores > threshold
    return outliers

# Handle outliers using Z-score method
def handle_outliers_zscore(data, threshold=3, replacement=None):
    outliers = identify_outliers_zscore(data, threshold)
    if replacement is None:
        # Remove outliers
        data_cleaned = data[~outliers]
    else:
        if replacement == 'median':
            replacement_value = data.median()
        elif replacement == 'mean':
            replacement_value = data.mean()
        else:
            replacement_value = replacement
        
        # Replace outliers with replacement value
        data_cleaned = data.copy()
        data_cleaned[outliers] = replacement_value

    return data_cleaned

# Winsorize data
def winsorize_data(data, limits=(0.05, 0.05)):
    from scipy.stats.mstats import winsorize
    winsorized_data = winsorize(data, limits=limits)
    return pd.Series(winsorized_data)
