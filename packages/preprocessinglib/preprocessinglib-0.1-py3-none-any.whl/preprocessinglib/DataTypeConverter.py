import pandas as pd


class DataTypeConverter:
    @staticmethod
    def convert_to_numeric(data, columns):
        for column in columns:
            if not pd.api.types.is_numeric_dtype(data[column]):
                data[column] = pd.to_numeric(data[column], errors='coerce')
        return data

    @staticmethod
    def convert_to_categorical(data, columns):

        data[columns] = data[columns].astype('category')
        return data
