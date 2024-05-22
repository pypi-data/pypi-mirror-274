class FeatureEngineer:
    @staticmethod
    def create_new_features(data, column1='CurrentColumn1', column2='CurrentColumn2'):
        data['NewFeature'] = data[column1] + data[column2]
        return data
