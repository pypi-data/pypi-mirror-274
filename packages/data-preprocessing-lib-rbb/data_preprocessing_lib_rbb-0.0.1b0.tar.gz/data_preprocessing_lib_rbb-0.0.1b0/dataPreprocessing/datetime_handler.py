import pandas as pd
from datetime import datetime, timedelta


class DateTimeHandler:
    """
    DateTimeHandler is a class for performing date and time manipulations on DataFrame columns.

    Methods:
        convert_to_datetime(df, column, format):
            Converts a column in the DataFrame to datetime objects based on the provided format.

        extract_date_component(df, column, component):
            Extracts a specific component (year, month, day, hour, minute, second) from a datetime column.

        calculate_date_difference(df, column1, column2, unit):
            Calculates the difference between two datetime columns in the specified unit (days, seconds).

        add_to_date(df, column, amount, unit):
            Adds a specified amount of time (days, weeks, months, years) to a datetime column.
    """

    @staticmethod
    def convert_to_datetime(df, column, format=None):
        df[column] = pd.to_datetime(df[column], format=format)
        return df

    @staticmethod
    def extract_date_component(df, column, component):
        if component == 'year':
            df[f'{column}_year'] = df[column].dt.year
        elif component == 'month':
            df[f'{column}_month'] = df[column].dt.month
        elif component == 'day':
            df[f'{column}_day'] = df[column].dt.day
        elif component == 'hour':
            df[f'{column}_hour'] = df[column].dt.hour
        elif component == 'minute':
            df[f'{column}_minute'] = df[column].dt.minute
        elif component == 'second':
            df[f'{column}_second'] = df[column].dt.second
        return df

    @staticmethod
    def calculate_date_difference(df, column1, column2, unit='days'):
        diff = df[column1] - df[column2]
        if unit == 'days':
            df[f'{column1}_vs_{column2}_diff'] = diff.dt.days
        elif unit == 'seconds':
            df[f'{column1}_vs_{column2}_diff'] = diff.dt.total_seconds()
        return df

    @staticmethod
    def add_to_date(df, column, amount, unit='days'):
        if unit == 'days':
            df[column] = df[column] + timedelta(days=amount)
        elif unit == 'weeks':
            df[column] = df[column] + timedelta(weeks=amount)
        elif unit == 'months':
            df[column] = df[column] + pd.DateOffset(months=amount)
        elif unit == 'years':
            df[column] = df[column] + pd.DateOffset(years=amount)
        return df
