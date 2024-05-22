import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, PowerTransformer
import numpy as np

class Scaler:
    def __init__(self) -> None:
        pass

# Standardize the data
def standardize_data(dataframe):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(dataframe)
    return pd.DataFrame(scaled_data, columns=dataframe.columns)

# Normalize the data
def normalize_data(dataframe):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(dataframe)
    return pd.DataFrame(scaled_data, columns=dataframe.columns)

# Robust scaling
def robust_scale_data(dataframe):
    scaler = RobustScaler()
    scaled_data = scaler.fit_transform(dataframe)
    return pd.DataFrame(scaled_data, columns=dataframe.columns)

# Normalize vectors
def normalize_vectors(dataframe):
    norm = np.linalg.norm(dataframe, axis=1)
    normalized_data = dataframe.div(norm, axis=0)
    return pd.DataFrame(normalized_data, columns=dataframe.columns)

# Log transform data
def log_transform_data(dataframe):
    log_data = np.log1p(dataframe)
    return pd.DataFrame(log_data, columns=dataframe.columns)

# MaxAbsScaler
def maxabs_scale_data(dataframe):
    scaler = MaxAbsScaler()
    scaled_data = scaler.fit_transform(dataframe)
    return pd.DataFrame(scaled_data, columns=dataframe.columns)

# PowerTransformer
def power_transform_data(dataframe, method='yeo-johnson'):
    transformer = PowerTransformer(method=method)
    transformed_data = transformer.fit_transform(dataframe)
    return pd.DataFrame(transformed_data, columns=dataframe.columns)
        
    