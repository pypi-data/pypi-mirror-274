import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


class CategoricalEncoder:
    """
    CategoricalEncoder is a class for performing label encoding and one-hot encoding on DataFrame columns.

    Methods:
        label_encode(df, column):
            Performs label encoding on the specified column.

        one_hot_encode(df, column):
            Performs one-hot encoding on the specified column.
    """

    @staticmethod
    def label_encode(df, column):
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        return df, le

    @staticmethod
    def one_hot_encode(df, column):
        ohe = OneHotEncoder(sparse_output=False)
        encoded = ohe.fit_transform(df[[column]])
        encoded_df = pd.DataFrame(encoded, columns=ohe.get_feature_names_out([column]))
        df = pd.concat([df.drop(column, axis=1), encoded_df], axis=1)
        return df, ohe
