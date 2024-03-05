#!/usr/bin/env python3
''' Users '''
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship 
from .base_model import BaseModel


class User(BaseModel):
    ''' Users Class '''
    __tablename__= "users"
    email = Column(String(128), nullable=False, unique=True)
    phone = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    role = Column(String(60), default="USER")

    rescues = relationship("Rescue", back_populates="user")
    adopt = relationship("Adopt", back_populates='user')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        