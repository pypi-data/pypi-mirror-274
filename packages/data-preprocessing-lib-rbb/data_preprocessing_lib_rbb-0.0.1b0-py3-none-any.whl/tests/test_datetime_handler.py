import unittest
import pandas as pd
from datetime import datetime

from dataPreprocessing.datetime_handler import DateTimeHandler


class TestDateTimeHandler(unittest.TestCase):
    """
    TestDateTimeHandler is a test class for the DateTimeHandler class, ensuring the correct functionality of date and time manipulations.

    Methods:
        setUp():
            Initializes a sample DataFrame with datetime data for testing.

        test_convert_to_datetime():
            Tests the conversion of a column to datetime objects.

        test_extract_date_component():
            Tests the extraction of specific date components from a datetime column.

        test_calculate_date_difference():
            Tests the calculation of the difference between two datetime columns.

        test_add_to_date():
            Tests the addition of a specified amount of time to a datetime column.
    """

    def setUp(self):
        self.data = pd.DataFrame({
            'date1': ['2023-05-19', '2024-05-19', '2025-05-19'],
            'date2': ['2023-04-19', '2023-05-19', '2023-06-19']
        })
        self.data = DateTimeHandler.convert_to_datetime(self.data, 'date1')
        self.data = DateTimeHandler.convert_to_datetime(self.data, 'date2')

    def test_convert_to_datetime(self):
        df = pd.DataFrame({'date': ['2023-05-19', '2024-05-19', '2025-05-19']})
        df = DateTimeHandler.convert_to_datetime(df, 'date')
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['date']))

    def test_extract_date_component(self):
        df = DateTimeHandler.extract_date_component(self.data, 'date1', 'year')
        self.assertIn('date1_year', df.columns)
        self.assertEqual(df['date1_year'].iloc[0], 2023)

    def test_calculate_date_difference(self):
        df = DateTimeHandler.calculate_date_difference(self.data, 'date1', 'date2')
        self.assertIn('date1_vs_date2_diff', df.columns)
        self.assertEqual(df['date1_vs_date2_diff'].iloc[0], 30)

    def test_add_to_date(self):
        df = DateTimeHandler.add_to_date(self.data, 'date1', 10, 'days')
        self.assertEqual(df['date1'].iloc[0], datetime(2023, 5, 29))

    def test_invalid_date_format(self):
        df = pd.DataFrame({'date': ['invalid', 'also invalid']})
        df = DateTimeHandler.convert_to_datetime(df, 'date')
        self.assertTrue(df['date'].isna().all())

if __name__ == '__main__':
    unittest.main()
