#!/usr/bin/env python3
''' Adopts '''
from sqlalchemy import Column, String, Integer
from base_model import BaseModel


class Adopt(BaseModel):
    ''' Adopts Class '''
    __tablename__ = "adopts"
    animal_id = Column(String(128))
    user_id = Column(String(128))
    status = Column(String(128))