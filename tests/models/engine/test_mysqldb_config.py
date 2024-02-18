#!/user/bin/env pyton3
''' test mysql connection '''
from sqlalchemy import inspect
from models.engine.mysqldb_config import MysqlConfig


def test_db_connection():
    mysql = MysqlConfig()
    assert mysql is not None
    assert mysql._MysqlConfig__engine is not None

    mysql.reload()
    inspector = inspect(mysql._MysqlConfig__engine)
    assert 'users' in inspector.get_table_names() 