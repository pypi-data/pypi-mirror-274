class DataAssetResource:

    def __init__(self, client):
        self.client = client
        self._dataframe = None

    @property
    def dataframe(self):
        if self._dataframe is None:
            from gable.integrations.dataframe import DataFrameDataAssetIntegration

            self._dataframe = DataFrameDataAssetIntegration(self.client)
        return self._dataframe
