#!/usr/bin/env python3
''' Users '''
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship 
from .base_model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    ''' Users Class '''
    __tablename__= "users"
    email = Column(String(128))
    phone = Column(String(128))
    password = Column(String(128))
    role = Column(String(60))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_password(self, password):
        ''' hash password''' 
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ check if password is correct"""
        return check_password_hash(self.password, password)  