# tests/test_scaler.py

import unittest
import pandas as pd

from dataPreprocessing.scaler import Scaler


class TestScaler(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50]
        })

    def test_minmax_scaler(self):
        scaler = Scaler(method="minmax")
        transformed = scaler.fit_transform(self.data)
        expected = pd.DataFrame({
            'A': [0.0, 0.25, 0.5, 0.75, 1.0],
            'B': [0.0, 0.25, 0.5, 0.75, 1.0]
        })
        pd.testing.assert_frame_equal(pd.DataFrame(transformed, columns=self.data.columns), expected)

    def test_standard_scaler(self):
        scaler = Scaler(method="standard")
        transformed = scaler.fit_transform(self.data)
        expected = pd.DataFrame({
            'A': [-1.414214, -0.707107, 0.000000, 0.707107, 1.414214],
            'B': [-1.414214, -0.707107, 0.000000, 0.707107, 1.414214]
        })
        pd.testing.assert_frame_equal(
            pd.DataFrame(transformed, columns=self.data.columns),
            expected,
            check_dtype=False, # Skipping the "checking for given data type"
            atol=1e-5 # Mutlak tolerans
        )

    def test_invalid_method(self):
        with self.assertRaises(ValueError):
            Scaler(method="invalid_method")

if __name__ == '__main__':
    unittest.main()
