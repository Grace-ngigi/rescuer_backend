#!/usr/bin/env python3
''' Users '''
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship 
from .base_model import BaseModel


class User(BaseModel):
    ''' Users Class '''
    __tablename__= "users"
    email = Column(String(128))
    phone = Column(String(128))
    password = Column(String(128))
    role = Column(String(60))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        