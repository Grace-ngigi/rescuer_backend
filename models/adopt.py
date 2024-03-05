#!/usr/bin/env python3
''' Adopts '''
from sqlalchemy import Column, String, ForeignKey
from enum import Enum
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


class AdoptStatus(Enum):
    INIT = 'INIT'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPETED = 'COMPLETED'


class Adopt(BaseModel):
    ''' Adopts Class '''
    __tablename__ = "adopts"
    rescue_id = Column(String(128), ForeignKey("rescues.id"), unique=True)
    user_id = Column(String(128), ForeignKey("users.id"))
    status = Column(String(128))

    rescue = relationship("Rescue", back_populates='adopt')
    user = relationship("User", back_populates='adopt')

    def __init__(self, status, *args, **kwargs):
        if status not in AdoptStatus.__members__:
            raise ValueError(f"Invalid status: {status}. Must be one of {', '.join(AdoptStatus.__members__.keys())}")
        self.status = status
        super().__init__(*args, **kwargs)
