from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd


class CategoricalEncoder:
    @staticmethod
    def one_hot_encode(data, columns):

        encoder = OneHotEncoder(drop='first', sparse_output=False)
        encoded_data = pd.DataFrame(encoder.fit_transform(data[columns]))
        data = data.drop(columns, axis=1)
        encoded_data.columns = encoder.get_feature_names_out(columns)
        return pd.concat([data, encoded_data], axis=1)

    @staticmethod
    def label_encode(data, column):

        encoder = LabelEncoder()
        data[column] = encoder.fit_transform(data[column])
        return data
