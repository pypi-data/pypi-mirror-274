
class FeatureEngineer:
    """
    FeatureEngineer is a class for creating new features from existing DataFrame columns.

    Methods:
        add_difference(df, col1, col2, new_col_name):
            Adds a new column to the DataFrame which is the difference between col1 and col2.

        add_product(df, col1, col2, new_col_name):
            Adds a new column to the DataFrame which is the product of col1 and col2.

        add_sum(df, col1, col2, new_col_name):
            Adds a new column to the DataFrame which is the sum of col1 and col2.

        add_square(df, col, new_col_name):
            Adds a new column to the DataFrame which is the square of the values in col.
    """

    @staticmethod
    def add_difference(df, col1, col2, new_col_name):
        df[new_col_name] = df[col1] - df[col2]
        return df

    @staticmethod
    def add_product(df, col1, col2, new_col_name):
        df[new_col_name] = df[col1] * df[col2]
        return df

    @staticmethod
    def add_sum(df, col1, col2, new_col_name):
        df[new_col_name] = df[col1] + df[col2]
        return df

    @staticmethod
    def add_square(df, col, new_col_name):
        df[new_col_name] = df[col] ** 2
        return df
