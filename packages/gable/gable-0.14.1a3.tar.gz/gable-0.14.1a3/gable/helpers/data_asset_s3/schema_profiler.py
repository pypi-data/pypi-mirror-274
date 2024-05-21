from typing import Optional

import pandas as pd
from gable.helpers.data_asset_s3.logger import log_error
from gable.openapi import (
    DataProfile,
    DataProfileBoolean,
    DataProfileFieldsMapping,
    DataProfileNumber,
    DataProfileOther,
    DataProfileString,
    DataProfileTemporal,
    DataProfileUnion,
    DataProfileUUID,
)
from loguru import logger


def get_data_profile_for_data_asset(
    recap_schema: dict, dfs: list[pd.DataFrame], event_name: str
) -> Optional[DataProfileFieldsMapping]:
    """
    given a mapping of column name to pandas dataframe, return a mapping of column name to data profile
    """
    logger.debug(f"Attempting to compute data profiles for data asset: {event_name}")

    try:
        df = pd.concat(dfs)
        result: dict[str, DataProfile] = {}

        column_name_to_schema: dict[str, dict] = {}
        _populate_column_schemas(recap_schema, column_name_to_schema)
        for column_name, column_schema in column_name_to_schema.items():
            if column_name not in df.columns:
                log_error(
                    f"column {column_name} not found in data - skipping in data profile"
                )
            elif profile := _get_data_profile_for_column(column_schema, df[column_name]):  # type: ignore
                result[column_name] = profile

        return DataProfileFieldsMapping(__root__=result)
    except Exception as e:
        log_error(f"Error computing data profiles for data asset: {event_name}")


def _populate_column_schemas(
    recap_schema: dict, map: dict[str, dict], prefix: str = ""
):
    for column_schema in recap_schema["fields"]:
        column_name = column_schema["name"]
        if "fields" in column_schema:
            # If the schema is a struct type, we need to go into the nested level
            _populate_column_schemas(column_schema, map, prefix + column_name + ".")
        else:
            map[prefix + column_name] = column_schema


def _get_data_profile_for_column(
    schema: dict, column: pd.Series, nullable: bool = False
) -> DataProfile:
    """
    given a column name and a pandas series, return a data profile
    """
    res = None
    null_count = None
    sampled_records_count = column.count()
    if schema["type"] == "union":
        non_null_schemas = [
            field for field in schema["types"] if field["type"] != "null"
        ]
        if (
            len(non_null_schemas) == 1
        ):  # it not a proper union, it's just representing a nullable field
            nullable = True
            schema = non_null_schemas[0]
        else:
            non_null_profiles: list[DataProfile] = [
                _get_data_profile_for_column(schema, column, nullable)
                for schema in non_null_schemas
            ]
            res = DataProfileUnion(
                profileType="union",
                sampledRecordsCount=sampled_records_count,
                nullable=False,
                profiles=non_null_profiles,
            )

    null_count = column.isnull().sum() if nullable else None
    if schema["type"] == "boolean":
        res = DataProfileBoolean(
            profileType="boolean",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
            trueCount=column.sum(),
            falseCount=sampled_records_count - column.sum(),
        )
    elif schema["type"] in ("int", "float"):
        if schema["type"] == "int" and any(
            [
                schema.get("logical", None) == logical
                for logical in ["build.recap.Timestamp", "build.recap.Date"]
            ]
        ):
            res = DataProfileTemporal(
                profileType="temporal",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                min=column.min(),
                max=column.max(),
                format="",  # TODO: revisit how to support with MM, DD, YY notation
            )
        else:
            res = DataProfileNumber(
                profileType="number",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                uniqueCount=column.nunique(),
                min=column.min(),
                max=column.max(),
            )
    elif schema["type"] == "string":
        for version, regex in [
            (1, uuid_regex_v1),
            (3, uuid_regex_v3),
            (4, uuid_regex_v4),
            (5, uuid_regex_v5),
        ]:
            if column.str.fullmatch(regex, case=False).all():
                res = DataProfileUUID(
                    profileType="uuid",
                    sampledRecordsCount=sampled_records_count,
                    nullable=nullable,
                    nullCount=null_count,
                    uuidVersion=version,
                    emptyCount=column.isna().sum(),
                    uniqueCount=column.nunique(),
                    maxLength=column.str.len().max(),
                    minLength=column.str.len().min(),
                    # TODO - add format
                )
                break
        if res is None:
            res = DataProfileString(
                profileType="string",
                sampledRecordsCount=sampled_records_count,
                nullable=nullable,
                nullCount=null_count,
                emptyCount=column.isna().sum(),
                uniqueCount=column.nunique(),
                maxLength=column.str.len().max(),
                minLength=column.str.len().min(),
            )
    else:
        res = DataProfileOther(
            profileType="other",
            sampledRecordsCount=sampled_records_count,
            nullable=nullable,
            nullCount=null_count,
        )
    return DataProfile(__root__=res)


# Time-based
uuid_regex_v1 = r"^[0-9a-f]{8}-[0-9a-f]{4}-1[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
# Name-based using MD5 hashing
uuid_regex_v3 = r"^[0-9a-f]{8}-[0-9a-f]{4}-3[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
# Randomly generated
uuid_regex_v4 = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
# Name-based using SHA-1 hashing
uuid_regex_v5 = r"^[0-9a-f]{8}-[0-9a-f]{4}-5[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
