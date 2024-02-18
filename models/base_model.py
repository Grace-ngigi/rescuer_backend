#!/usr/bin/env python3
''' Base Model '''
from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel(Base):
    ''' Base Model Class '''
    __abstract__ = True
    id = Column(String(128), primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    created_by = Column(String(255))
    updated_by = Column(String(255))
    deleted_by = Column(String(255))

    def __init__(self, *args, **kwargs):
        ''' initialize base model fields '''
        if kwargs:
            self.update_fields(kwargs)

    def update_fields(self, kwargs):
        ''' Update fields based on kwargs '''
        # init object attrs from dict inorin __class__
        for k, v in kwargs.items():
            if k != "__class__":
                setattr(self, k, v)
        #update id
        self.id = kwargs.get('id', self.id) or str(uuid.uuid4())
        # update time fields
        self.created_at = self.parse_date(kwargs.get('created_at', None)) or self.created_at
        self.updated_at = self.parse_date(kwargs.get('updated_at', None)) or self.updated_at
        self.deleted_at = self.parse_date(kwargs.get('deleted_at', None)) or self.deleted_at
        # update user fields
        self.created_by = kwargs.get('created_by', self.created_by)
        self.updated_by = kwargs.get('updated_by', self.updated_by)
        self.deleted_by = kwargs.get('deleted_by', self.deleted_by)

    def parse_date(self, date_str):
        ''' parse datetime string '''
        if date_str and isinstance(date_str, str):
            return datetime.strptime(date_str, time)
        return None    

    def __str__(self):
        ''' return a string representation of the class '''
        custom_dict = self.__custom_dict__()
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, custom_dict['id'], custom_dict) 
       
    def __custom_dict__(self, save_fs=None):
        ''' return dict representation of the class '''
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__

        if "created_at" in new_dict:
            new_dict["created_at"] = self.parse_date(new_dict["created_at"])
        if "updated_at" in new_dict:
            new_dict["updated_at"] = self.parse_date(new_dict["updated_at"])
        if "deleted_at" in new_dict:
            new_dict["deleted_at"] = self.parse_date(new_dict["deleted_at"])
        if "created_by" in new_dict:
            new_dict["created_by"] = new_dict["created_by"]
        if "updated_by" in new_dict:
            new_dict["updated_by"] = new_dict["updated_by"]  
        if "deleted_by" in new_dict:
            new_dict["deleted_by"] = new_dict["deleted_by"]  

        # Remove sqlachemy key, not needed for serialization 
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        # Remove password before serialization to ensure security
        # if save_fs is None:
        if "password" in new_dict:
                del new_dict["password"] 
        return new_dict