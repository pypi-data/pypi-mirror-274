from sklearn.preprocessing import StandardScaler, MinMaxScaler

class Scaler:
    def __init__(self, method="standard"):
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        else:
            raise ValueError("Invalid method: choose 'standard' or 'minmax'")
        self.columns = None

    def fit(self, X):
        numeric_cols = X.select_dtypes(include=['number'])
        self.columns = numeric_cols.columns
        self.scaler.fit(numeric_cols)
        return self

    def transform(self, X):
        X_copy = X.copy()
        X_copy[self.columns] = self.scaler.transform(X_copy[self.columns])
        return X_copy

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
