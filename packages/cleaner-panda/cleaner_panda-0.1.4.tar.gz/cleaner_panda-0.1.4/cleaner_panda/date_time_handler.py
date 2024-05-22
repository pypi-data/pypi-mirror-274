import pandas as pd
import pytz
from datetime import datetime, timedelta


class DateTimeHandler:
    def __init__(self) -> None:
        '''Initialize DateTimeHandler with any required setup.'''
        pass
    
    def convert_date_to_strings(self, dataframe: pd.DataFrame, column=0) -> pd.DataFrame:
        '''Convert datetime objects in the specified column to strings.'''
        dataframe.iloc[:, column] = dataframe.iloc[:, column].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else x)
        return dataframe
    
    def extract_components(self, dataframe: pd.DataFrame, column=0) -> pd.DataFrame:
        '''Extract date components (year, month, day, hour, minute, second) into separate columns.'''
        dataframe['year'] = dataframe.iloc[:, column].dt.year
        dataframe['month'] = dataframe.iloc[:, column].dt.month
        dataframe['day'] = dataframe.iloc[:, column].dt.day
        dataframe['hour'] = dataframe.iloc[:, column].dt.hour
        dataframe['minute'] = dataframe.iloc[:, column].dt.minute
        dataframe['second'] = dataframe.iloc[:, column].dt.second
        return dataframe
    
    def reformat_date(self, dataframe: pd.DataFrame, column=0) -> pd.DataFrame:
        '''Reformat the datetime objects in the specified column to a different string format.'''
        dataframe.iloc[:, column] = dataframe.iloc[:, column].apply(lambda x: x.strftime('%d-%m-%Y %H:%M:%S') if pd.notnull(x) else x)
        return dataframe
    
    def calculate_datetime_differences(self, dataframe: pd.DataFrame, column=0) -> pd.DataFrame:
        '''Calculate the difference between consecutive datetime entries in the specified column.'''
        dataframe['time_diff'] = dataframe.iloc[:, column].diff().dt.total_seconds()
        return dataframe

    def convert_datetime_to_different_timezones(self, dataframe: pd.DataFrame, column=0, from_tz='UTC', to_tz='America/New_York') -> pd.DataFrame:
        '''Convert datetime objects from one timezone to another.'''
        from_zone = pytz.timezone(from_tz)
        to_zone = pytz.timezone(to_tz)

        def convert_timezone(dt):
            if pd.notnull(dt):
                dt = from_zone.localize(dt) if dt.tzinfo is None else dt
                return dt.astimezone(to_zone)
            return dt

        dataframe.iloc[:, column] = dataframe.iloc[:, column].apply(convert_timezone)
        return dataframe

    def shift_time(self, dataframe: pd.DataFrame, column=0, shift_value=1, unit='days') -> pd.DataFrame:
        '''Shift the datetime values in the specified column by a given amount.'''
        shift_kwargs = {unit: shift_value}
        dataframe.iloc[:, column] = dataframe.iloc[:, column] + pd.to_timedelta(shift_value, unit=unit)
        return dataframe

    def handle_irregular_time_intervals(self, dataframe: pd.DataFrame, column=0) -> pd.DataFrame:
        '''Handle irregular time intervals in the datetime column, e.g., forward fill missing datetimes.'''
        date_column = dataframe.columns[column]
        dataframe = dataframe.dropna(subset=[date_column])  # Remove rows where date_column is NaT
        dataframe = dataframe.set_index(date_column)
        dataframe = dataframe.sort_index()  # Ensure the index is sorted
        dataframe = dataframe.asfreq('D', method='ffill')
        dataframe = dataframe.reset_index()
        return dataframe