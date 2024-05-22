class MissingValueHandler:
    @staticmethod
    def detect_missing_values(data):

        missing_values = data.isnull().sum()
        return missing_values

    @staticmethod
    def fill_missing_values(data, strategy='mean', value=None):

        if strategy == 'mean':
            filled_data = data.fillna(data.mean())
        elif strategy == 'median':
            filled_data = data.fillna(data.median())
        elif strategy == 'constant':
            if value is None:
                raise ValueError("You must specify a constant value.")
            filled_data = data.fillna(value)
        elif strategy == 'drop':
            filled_data = data.dropna()
        else:
            raise ValueError("Invalid padding strategy!")

        return filled_data

    @staticmethod
    def remove_missing_values(data):

        cleaned_data = data.dropna()
        return cleaned_data
