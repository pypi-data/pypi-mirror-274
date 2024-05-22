import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder
import category_encoders as ce

class CategoricalEncoder:
    def __init__(self) -> None:
        pass

# Label encoding
def label_encoding(dataframe, column):
    encoder = LabelEncoder()
    dataframe[column] = encoder.fit_transform(dataframe[column])
    return dataframe

# One-hot encoding
def one_hot_encoding(dataframe, column):
    one_hot_encoded = pd.get_dummies(dataframe[column], prefix=column)
    dataframe = dataframe.drop(column, axis=1)
    dataframe = dataframe.join(one_hot_encoded)
    return dataframe

# Ordinal encoding
def ordinal_encoding(dataframe, column):
    encoder = OrdinalEncoder()
    dataframe[column] = encoder.fit_transform(dataframe[[column]])
    return dataframe

# Binary encoding
def binary_encoding(dataframe, column):
    encoder = ce.BinaryEncoder(cols=[column])
    dataframe = encoder.fit_transform(dataframe)
    return dataframe

# Target encoding
def target_encoding(dataframe, column, target):
    encoder = ce.TargetEncoder(cols=[column])
    encoded_data = encoder.fit_transform(dataframe[column], dataframe[target])
    dataframe[column] = encoded_data
    return dataframe