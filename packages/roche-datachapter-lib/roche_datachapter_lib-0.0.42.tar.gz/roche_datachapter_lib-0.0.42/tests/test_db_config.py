"""Tests for db config module"""
from roche_datachapter_lib.db_config import DB_CONFIG
print(DB_CONFIG.execute_custom_select_query("", ""))

for bind in DB_CONFIG.SQLALCHEMY_BINDS:
    print(f"Testing bind '{bind}'")
    RESULT = DB_CONFIG.test_bind_connection(bind)
    print(f"Bind '{bind}' test finished {'OK' if RESULT else 'with ERROR'}")
