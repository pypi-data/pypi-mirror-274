import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler


class Scaler:

    @staticmethod
    def standardize_data(data):

        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)

    @staticmethod
    def normalize_data(data):

        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data)
        return pd.DataFrame(scaled_data, columns=data.columns)
