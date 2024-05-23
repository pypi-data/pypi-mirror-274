# labneura/ml/linear_regression.py
import mlcpp

class LinearRegression:
    def __init__(self):
        self.model = mlcpp.LinearRegression()

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)