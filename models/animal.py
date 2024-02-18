#!/usr/bin/env python3
''' Animal '''
from sqlalchemy import Column, String, Integer
from base_model import BaseModel


class Animal(BaseModel):
    ''' Animal Class '''
    rescue_id = Column(String(128))
    vet_evaluation = Column(String(255))
    status = Column(String(128))