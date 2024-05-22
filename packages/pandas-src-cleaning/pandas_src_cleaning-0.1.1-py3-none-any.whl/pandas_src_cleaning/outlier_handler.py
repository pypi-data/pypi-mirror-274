import pandas as pd

class OutlierHandler:
    def __init__(self, df):
        self.df = df

    def iqr_outliers(self, column, threshold=1.5):
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]

    def remove_iqr_outliers(self, column, threshold=1.5):
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        self.df = self.df[(self.df[column] >= lower_bound) & (self.df[column] <= upper_bound)]
        return self.df

    def iqr_outliers_all(self, threshold=1.5):
        outliers = {}
        numeric_columns = self.df.select_dtypes(include=['number']).columns
        for column in numeric_columns:
            outliers[column] = self.iqr_outliers(column, threshold)
        return outliers

    def remove_iqr_outliers_all(self, threshold=1.5):
        numeric_columns = self.df.select_dtypes(include=['number']).columns
        for column in numeric_columns:
            self.remove_iqr_outliers(column, threshold)
        return self.df
