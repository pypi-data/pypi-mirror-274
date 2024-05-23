from typing import List, Union

import pandas as pd
from gable.client import (
    CheckDataAssetCommentMarkdownResponse,
    CheckDataAssetDetailedResponseUnion,
)
from gable.helpers.data_asset_s3.native_s3_converter import NativeS3Converter
from gable.integrations.base_integration import BaseDataAssetIntegration
from gable.openapi import (
    CheckComplianceDataAssetsDataFrameRequest,
    CheckDataAssetDetailedResponse,
    DataFrameAsset,
    ErrorResponse,
    RegisterDataAssetDataFrameRequest,
    Violation,
)


class DataFrameDataAssetIntegration(BaseDataAssetIntegration):

    def _convert_dataframe_to_recap(self, path: str, dataframe: pd.DataFrame) -> dict:
        return NativeS3Converter().to_recap(
            dataframe, has_schema=False, event_name=path
        )

    def _get_breaking_violations(
        self,
        response: Union[
            ErrorResponse,
            CheckDataAssetCommentMarkdownResponse,
            list[CheckDataAssetDetailedResponseUnion],
        ],
    ) -> List[Violation]:
        violations = []

        if isinstance(response, list):
            for detailed_response in response:
                if isinstance(detailed_response, CheckDataAssetDetailedResponse):
                    if detailed_response.violations:
                        violations.extend(detailed_response.violations)
        return violations

    def register(self, domain: str, path: str, dataframe: pd.DataFrame):  # type: ignore[override]
        """
        Convert a pandas DataFrame to a Recap StructType and register it as a data asset
        """
        # Convert the DataFrame to a Recap StructType
        recap_schema = self._convert_dataframe_to_recap(path, dataframe)

        # Create the RegisterDataAssetDataFrameRequest
        request = RegisterDataAssetDataFrameRequest(
            assets=[
                DataFrameAsset(
                    schema=recap_schema,
                    domain=domain,
                    path=path,
                )
            ]
        )

        # Make the request
        response = self.client.post_data_asset_register_dataframe(request)

        return response

    def check(self, domain: str, path: str, dataframe: pd.DataFrame):  # type: ignore[override]
        """
        Convert a pandas DataFrame to a Recap StructType and check it against the data asset
        """
        # Convert the DataFrame to a Recap StructType
        recap_schema = self._convert_dataframe_to_recap(path, dataframe)

        # Create the CheckComplianceDataAssetsDataFrameRequest
        request = CheckComplianceDataAssetsDataFrameRequest(
            assets=[
                DataFrameAsset(
                    schema=recap_schema,
                    domain=domain,
                    path=path,
                )
            ],
            responseType="DETAILED",
        )

        # Make the request
        response = self.client.post_check_compliance_data_assets_dataframe(request)

        # Raise an error if there are violations
        violations = self._get_breaking_violations(response)
        if violations:
            violation_messages = "\n".join(
                [violation.message for violation in violations]
            )
            raise ValueError(f"Contract violations found:\n{violation_messages}")

        return response

    def check_and_register(self, domain: str, path: str, dataframe: pd.DataFrame):  # type: ignore[override]
        # Check for contract violations
        self.check(domain, path, dataframe.copy(deep=True))

        # Register
        return self.register(domain, path, dataframe.copy(deep=True))
