#!/usr/bin/env python3
''' Rescues '''
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from enum import Enum

class RescueStatus(Enum):
    RESCUED = 'RESCUED'
    READY = 'READY'
    IN_PROGRESS = 'IN_PROGRESS'
    ADOPTED = 'ADOPTED'

class Rescue(BaseModel):
    ''' Rescues Class '''
    __tablename__ = "rescues"
    species = Column(String(128))
    age = Column(Integer)
    decription = Column(String(255))
    image_url = Column(Text)
    gender = Column(String(60))
    color = Column(String(60))
    location = Column(String(128))
    vet_evaluation = Column(String(255))
    status = Column(String(128))
    
    user_id = Column(String(128), ForeignKey('users.id'))

    user = relationship("User", back_populates="rescues")
    adopt = relationship("Adopt", back_populates='rescue')

    def __init__(self, status, *args, **kwargs):
        if status not in RescueStatus.__members__:
            raise ValueError(f"Invalid status: {status}. Must be one of {', '.join(RescueStatus.__members__.keys())}")
        self.status = status
        super().__init__(*args, **kwargs)
        