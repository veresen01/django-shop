from django.apps import apps
from django.db import connection


def check_model(app_label: str, model_name: str) -> bool:
    return apps.get_model(app_label, model_name) is not None


def db_table_exists(table_name):
    return table_name in connection.introspection.table_names()
