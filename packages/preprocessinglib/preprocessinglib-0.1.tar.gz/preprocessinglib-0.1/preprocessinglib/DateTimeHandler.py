import pandas as pd


class DateTimeHandler:
    @staticmethod
    def extract_date_features(data, column):

        data[column] = pd.to_datetime(data[column])
        data['Year'] = data[column].dt.year
        data['Month'] = data[column].dt.month
        data['Day'] = data[column].dt.day
        data['DayOfWeek'] = data[column].dt.dayofweek
        return data
