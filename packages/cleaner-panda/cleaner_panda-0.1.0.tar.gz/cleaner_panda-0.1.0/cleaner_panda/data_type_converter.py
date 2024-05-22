import pandas as pd

class DataTypeConverter:
    def __init__(self) -> None:
        '''Initialize DataTypeConverter.'''
        pass

    def convert_to_numeric(self, dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
        '''Convert the specified column to a numeric type.'''
        dataframe[column] = pd.to_numeric(dataframe[column], errors='coerce')
        return dataframe

    def convert_to_categorical(self, dataframe: pd.DataFrame, column: str) -> pd.DataFrame:
        '''Convert the specified column to a categorical type.'''
        dataframe[column] = dataframe[column].astype('category')
        return dataframe