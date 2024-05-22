class OutlierHandler:
    @staticmethod
    def detect_outliers(data, threshold=3):

        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        iqr = q3 - q1
        outliers = ((data < (q1 - 1.5 * iqr)) | (data > (q3 + 1.5 * iqr)))
        return outliers

    @staticmethod
    def handle_outliers(data, method='drop'):

        outliers = OutlierHandler.detect_outliers(data)
        if method == 'drop':
            cleaned_data = data[~outliers.any(axis=1)].dropna()
        elif method == 'replace':
            cleaned_data = data.mask(outliers, data.median())
        else:
            raise ValueError("Invalid outlier handling method!")
        return cleaned_data
