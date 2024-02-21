#!/usr/bin/env python3
''' Rescues '''
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class Rescue(BaseModel):
    ''' Rescues Class '''
    __tablename__ = "rescues"
    species = Column(String(128))
    age = Column(Integer)
    decription = Column(String(255))
    image_url = Column(String(255))
    location = Column(String(128))
    user_id = Column(String(128), ForeignKey('users.id'))

    user = relationship("User", back_populates="rescues")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)