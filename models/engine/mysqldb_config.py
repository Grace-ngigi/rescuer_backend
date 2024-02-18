#!/usr/bin/python3
''' MySQL DB configuration '''
from models.user import User
from models.base_model import Base
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"User": User}


class MysqlConfig:
    # private class variables
    __engine = None
    __session = None

    def __init__(self) -> None:
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_name = os.getenv('DB_NAME')
        self.__engine = create_engine("mysql+mysqldb://root:Saisa#Root@localhost/rescuer")
        print("Initializing MySQL DB Engine...")

    def reload(self):
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session
        print("tables created...")

    def get_session(self):
        return self.__session