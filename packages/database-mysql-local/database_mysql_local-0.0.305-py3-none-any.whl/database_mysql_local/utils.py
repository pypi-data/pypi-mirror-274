import inspect
import os
import re
from functools import lru_cache
from typing import Any, Optional

from python_sdk_remote.utilities import get_environment_name
from url_remote.environment_name_enum import EnvironmentName

from .table_definition import table_definition
from .to_sql_interface import ToSQLInterface


def validate_select_table_name(database_object_name: str, is_test_data: bool = False) -> None:
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not database_object_name.endswith("_view") and not is_test_data):
        raise Exception(
            f"View name must end with '_view' in this environment (got {database_object_name})")


def validate_none_select_table_name(database_object_name: str) -> None:
    if (get_environment_name() not in (EnvironmentName.DVLP1.value, EnvironmentName.PROD1.value)
            and not database_object_name.endswith("_table")):
        raise Exception(
            f"Table name must end with '_table' in this environment  (got {database_object_name})")


def process_insert_data_dict(data_dict: dict or None) -> tuple[str, str, dict]:
    if not data_dict:
        return '', '', {}

    columns = []
    values = []

    for key, value in data_dict.items():
        columns.append(f"`{key}`")
        if isinstance(value, ToSQLInterface):
            values.append(value.to_sql())
        else:
            values.append('%s')

    filtered_data_dict = {key: value for key, value in data_dict.items() if
                          not isinstance(value, ToSQLInterface)}
    return ','.join(columns), ','.join(values), filtered_data_dict


# Please add typing and example of input-output as docstring if possible.
def process_update_data_dict(data_dict: dict or None) -> tuple[str, dict]:
    if not data_dict:
        return '', {}

    set_values = []
    for key, value in data_dict.items():
        if isinstance(value, ToSQLInterface):
            set_values.append(f"`{key}`={value.to_sql()}")
        else:
            set_values.append(f"`{key}`=%s")

    filtered_data_dict = {key: value for key, value in data_dict.items() if
                          not isinstance(value, ToSQLInterface)}
    # + "," because we add updated_timestamp in the update query
    return ', '.join(set_values) + ",", filtered_data_dict


@lru_cache
def detect_if_is_test_data() -> bool:
    """Check if running from a Unit Test file."""
    possible_current_files = [os.path.basename(frame.filename) for frame in inspect.stack()]

    for file_name in possible_current_files:
        if file_name.startswith('test_') or file_name.endswith('_test.py') or "pytest" in file_name:
            return True
    return False


def get_entity_type_by_table_name(table_name: str) -> int or None:
    """Returns the entity_type_id of the table."""
    if table_name in table_definition:
        entity_type_id = table_definition[table_name].get("entity_type_id1")
        return entity_type_id


def generate_view_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        return re.sub(r'(_table)$', '_view', table_name)


def generate_column_name(table_name: Optional[str]) -> Optional[str]:
    if table_name:
        return re.sub(r'(_table)$', '_id', table_name)


def validate_single_clause_value(select_clause_value: str = None) -> None:
    if "," in select_clause_value or select_clause_value == "*":
        raise ValueError("select value requires a single column name")


def get_where_params(column_name: str, column_value: Any) -> tuple:
    # If we use "if column_value:" it will not work for 0, False, etc.
    if column_value is not None:
        where = f"`{column_name}`=%s"
        params = (column_value,)
    else:
        where = f"`{column_name}` IS NULL"
        params = None
    return where, params


def where_skip_null_values(where: str or None, select_clause_value: str,
                           skip_null_values: bool = False) -> str:
    if skip_null_values:
        validate_single_clause_value(select_clause_value)
        where_skip = f"`{select_clause_value}` IS NOT NULL"
        if where:
            where += f" AND {where_skip}"
        else:
            where = where_skip
    return where
