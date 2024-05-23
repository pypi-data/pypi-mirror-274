import pandas as pd
from pandas.api.types import infer_dtype

# TODO - Replace return types with Gable Types
# from gable.openapi import (
#     FieldModel,
#     GableSchemaBool,
#     GableSchemaFloat,
#     GableSchemaInt,
#     GableSchemaList,
#     GableSchemaNull,
#     GableSchemaString,
#     GableSchemaStruct,
#     GableSchemaType,
#     GableSchemaUnion,
# )


class NativeS3Converter:
    def __init__(self):
        pass

    def to_recap(self, df: pd.DataFrame, has_schema: bool, event_name: str) -> dict:
        """
        Convert a pandas DataFrame to a Recap StructType.
        Args:
            df (pd.DataFrame): The pandas DataFrame to convert.
            event_name (str): The name of the field.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        Returns:
            StructType: The Recap StructType representing the DataFrame.
        """
        schema = self._get_schema(df, has_schema)
        nullable = df.isnull().any()
        fields = []
        for field_name, field_dtypes in schema.items():
            try:
                # Handle column representing nested JSON field
                # ex: customerDetails.technicalContact.email
                if "." in field_name:
                    self._handle_nested_fields(
                        field_name,
                        field_dtypes,
                        nullable,
                        fields,
                        df[field_name],  # type: ignore
                        has_schema,
                    )
                else:
                    gable_type = self._parse_type(
                        field_dtypes, field_name, nullable[field_name], df[field_name], has_schema  # type: ignore
                    )
                    fields.append(gable_type)
            except ValueError as e:
                print(f"Error parsing field {field_name} of type {field_dtypes}: {e}")

        return {"fields": fields, "name": event_name, "type": "struct"}

    def _parse_type(
        self,
        dtypes: list[str],
        field_name: str,
        nullable: bool,
        column: pd.Series,
        has_schema: bool,
    ) -> dict:
        """
        Parse a Dataframe dtype and return the corresponding Gable Type.
        Args:
            dtypes List[str]: List of field types to parse.
            field_name (str): The name of the field.
            nullable (bool): Whether the field is nullable.
            column (pd.Series): The column to parse.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        Returns:
            The Gable Type corresponding to the field type.
        """
        types = []
        null_added = False
        if (
            nullable and column.isnull().all()
        ):  # If we only see null values, return a null type
            return {
                "type": "null",
                "name": field_name,
            }
        for dtype in dtypes:
            if dtype == "string":
                types.append({"type": "string", "name": field_name})
            elif dtype == "Int64":
                types.append({"type": "int", "name": field_name, "bits": 64})
            elif dtype == "Int32":
                types.append({"type": "int", "name": field_name, "bits": 32})
            elif dtype == "Float64":
                types.append({"type": "float", "name": field_name, "bits": 64})
            elif dtype == "boolean":
                types.append({"type": "bool", "name": field_name})
            elif dtype == "object":
                # TODO - figure out what is inside the list
                types.append(
                    {"type": "list", "name": field_name, "values": {"type": "Unknown"}}
                )
            elif dtype.startswith("datetime64[ns") and dtype.endswith("]"):
                types.append(self._parse_datetime_type(column, field_name))
            else:
                raise ValueError(f"Unsupported dtype: {dtype}")

            if not has_schema and nullable:
                if not null_added:
                    types.append({"type": "null"})
                    null_added = True
                # in conversations with Adrian and Suzanne, we determined that it's safe (in the short term)
                # to assume that when a dtype is an object and also nullable, that it's a null type.
                # the above todo for determining list types will need to be tackled in future work and may include a refactoring to replace pandas for JSON parsing/inference
                if dtype == "object":
                    types.append(
                        {
                            "type": "null",
                            "name": field_name,
                        }
                    )

        if len(types) > 1:
            return {"type": "union", "types": types, "name": field_name}
        if len(types) == 1:
            return types[0]
        return {"type": "null", "name": field_name}

        # return type

    def _parse_datetime_type(self, column: pd.Series, field_name: str) -> dict:
        """
        Parse a datetime type and return the corresponding Gable Type.
        Args:
            df (pd.DataFrame): The pandas DataFrame to convert.
            field_name (str): The name of the field.
        Returns:
            The Gable Type corresponding to the field type.
        """
        # If the datetime column has a timezone, assume it's a timestamp
        if column.dt.tz is not None:
            return {
                "type": "int",
                "logical": "build.recap.Timestamp",
                "name": field_name,
                "bits": 64,
            }

        # If all values are midnight, assume it's a date
        is_date = (
            all(column.dt.hour == 0)
            and all(column.dt.minute == 0)
            and all(column.dt.second == 0)
            and all(column.dt.microsecond == 0)
            and all(column.dt.nanosecond == 0)
        )
        if is_date:
            return {
                "type": "int",
                "logical": "build.recap.Date",
                "name": field_name,
                "bits": 64,
            }

        # If we could not determine, assume it's a timestamp
        return {
            "type": "int",
            "logical": "build.recap.Timestamp",  # TODO - improve. Consider a Duration, Time, etc.
            "name": field_name,
            "bits": 64,
        }

    def _handle_nested_fields(
        self,
        field_name: str,
        field_types: list[str],
        nullable,
        current_level_fields: list[dict],
        column: pd.Series,
        has_schema: bool,
    ):
        """
        Handle nested fields in a DataFrame.
        Args:
            field_name (str): The name of the field.
            field_types List[str]: List of field types to parse.
            nullable (pd.Series): Whether the field is nullable.
            current_level_fields (list): The current "level" of fields.
            column (pd.Series): The column to parse.
            has_schema (bool): Whether the DataFrame has a predefined schema. If False, the schema will be inferred based on its contents
        """

        field_name_parts = field_name.split(".")
        # Iterate through each "level" of the nested fields
        for index, subfield_name in enumerate(field_name_parts):
            # Look to see if the subfield has already been added to the current level
            found_recap_type = next(
                (
                    field
                    for field in current_level_fields
                    if field["name"] == subfield_name
                ),
                None,
            )
            if found_recap_type is not None:
                subfield_recap_type = found_recap_type
            else:
                if index == len(field_name_parts) - 1:
                    # Last item in the list is not a StructType
                    subfield_recap_type = self._parse_type(
                        field_types,
                        subfield_name,
                        nullable[field_name],
                        column,
                        has_schema,
                    )
                else:
                    subfield_recap_type = {
                        "fields": [],
                        "name": subfield_name,
                        "type": "struct",
                    }
                current_level_fields.append(subfield_recap_type)

            if subfield_recap_type["type"] == "struct":
                # Update current_level_fields to the next "level"
                current_level_fields = subfield_recap_type["fields"]

    def _get_schema(self, df: pd.DataFrame, has_schema: bool) -> dict[str, list[str]]:
        """
        Infer the schema of the DataFrame by examining the data type of each entry in each column.
        Handles mixed types and assigns the most appropriate type.
        """
        # if it has a schema already, assume it is correct and don't try coercing types down
        if has_schema:
            dtypes_dict = df.convert_dtypes().dtypes.to_dict()
            return {col: [str(dtype)] for col, dtype in dtypes_dict.items()}

        df.columns = df.columns.astype(str)
        type_schema = {col: set() for col in df.columns}
        for col in df.columns:
            for entry in df[col].dropna():
                if isinstance(entry, list):
                    type_schema[col].add("object")
                else:
                    type_detected = self._detect_type(entry, df, col)
                    type_schema[col].add(type_detected)
        value = {
            col: sorted((str(type) for type in types), key=lambda x: x)
            for col, types in type_schema.items()
        }
        return value

    def _detect_type(self, entry, df: pd.DataFrame, col: str):
        """
        Detect the type of an entry, handling numeric, datetime, and other types.
        """
        inferred_dtype = infer_dtype([entry])
        if inferred_dtype == "boolean":
            return pd.BooleanDtype()
        try:
            converted_col_dtype = df[col].convert_dtypes().dtypes
            numeric_entry = pd.to_numeric(entry, errors="raise")
            numeric_dtype = infer_dtype([numeric_entry])
            if (
                converted_col_dtype in [pd.Int64Dtype(), pd.Float64Dtype()]
                and str(converted_col_dtype) != numeric_dtype
            ):
                return converted_col_dtype
            return pd.Int64Dtype() if numeric_dtype == "integer" else pd.Float64Dtype()
        except ValueError:
            try:
                pd.to_datetime(entry, errors="raise")
                df[col] = pd.to_datetime(df[col], errors="raise")
                return pd.Series([entry]).astype("datetime64[ns]").dtype
            except ValueError:
                return (
                    pd.StringDtype()
                    if inferred_dtype == "string"
                    else pd.Series([entry]).dtype
                )
