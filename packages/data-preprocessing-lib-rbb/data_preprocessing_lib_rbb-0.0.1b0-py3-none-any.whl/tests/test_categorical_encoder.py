import unittest
import pandas as pd
from dataPreprocessing.categorical_encoder import CategoricalEncoder


class TestCategoricalEncoder(unittest.TestCase):
    """
    TestCategoricalEncoder is a test class for the CategoricalEncoder class, ensuring the correct functionality of categorical encoding.

    Methods:
        setUp():
            Initializes a sample DataFrame for testing.

        test_label_encode():
            Tests the label encoding of a column.

        test_one_hot_encode():
            Tests the one-hot encoding of a column.
    """

    def setUp(self):
        self.data = pd.DataFrame({
            'category': ['A', 'B', 'A', 'C', 'B', 'C']
        })

    def test_label_encode(self):
        df, le = CategoricalEncoder.label_encode(self.data.copy(), 'category')
        self.assertTrue(pd.api.types.is_integer_dtype(df['category']))
        self.assertListEqual(list(df['category']), [0, 1, 0, 2, 1, 2])

    def test_one_hot_encode(self):
        df, ohe = CategoricalEncoder.one_hot_encode(self.data.copy(), 'category')
        self.assertTrue(all(col in df.columns for col in ['category_A', 'category_B', 'category_C']))
        self.assertEqual(df['category_A'].iloc[0], 1.0)
        self.assertEqual(df['category_B'].iloc[1], 1.0)
        self.assertEqual(df['category_C'].iloc[3], 1.0)

    def test_empty_column(self):
        df = pd.DataFrame({'category': []})
        df, le = CategoricalEncoder.label_encode(df, 'category')
        self.assertTrue(df.empty)

    def test_single_value(self):
        df = pd.DataFrame({'category': ['A', 'A', 'A']})
        df, le = CategoricalEncoder.label_encode(df, 'category')
        self.assertListEqual(list(df['category']), [0, 0, 0])


if __name__ == '__main__':
    unittest.main()
