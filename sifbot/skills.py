# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if 'base' not in globals():
    base = declarative_base()


class Skill(base):
    """ Compétence """

    __tablename__ = "skills"

    id = Column(Integer, primary_key = True)
    name = Column(String(16), nullable = False)
    short = Column(String(34), nullable = False)

    specialties = relationship("Specialty", back_populates="skill")

class Specialty(base):
    """ Spécialisations """

    __tablename__ = "specialties"

    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    short = Column(String(4), nullable = False)
    skill_id = Column(Integer, ForeignKey("skills.id"))

    skill = relationship("Skill", back_populates="specialties")
