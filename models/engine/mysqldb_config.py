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

    def all(self, cls=None):
        'return all records in a certain class'
        new_dict  ={}
        for i in classes:
            if cls is None or cls is classes[i] or cls is i:
                objs = self.__session.query(classes[i]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict
    
    def new(self, obj):
        ''' add object to current session '''
        self.__session.add(obj)

    def save(self):
        ''' commit changes to current session '''
        self.__session.commit()

    def delete(self, obj=None):
        ''' delete '''
        if obj is not None:
            self.__session.delete(obj)

    def close(self):
        self.__session.remove()  

    def find_one(self, model, condition):
        ''' find one by condition '''  
        return self.__session.query(model).filter(condition).first() 

    def find_many(self, model, condition):
        return self.__session.query(model).filter(condition)

    def get(self, cls, id):
        ''' return object based on class name and id '''
        if cls not in classes.values():
            return None
        
        all_classes = self.all(cls)
        for value in all_classes.values():
            if value.id == id:
                return value
        return None

    def get_session(self):
        return self.__session