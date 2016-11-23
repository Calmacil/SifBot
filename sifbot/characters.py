# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if 'base' not in globals():
    base = declarative_base()

class Character(base):
    """ Personnage """

    __tablename__ = "characters"

    id = Column(Integer, primary_key = True)
    discord_userid = Column(String(40), nullable = True)
    name = Column(String(64), nullable = False)
    description = Column(String(2000), nullable = True)
    age = Column(Integer, nullable = True)
    xp = Column(Integer, nullable = False)
    destiny = Column(Integer, nullable = False)

    # skills
    # specialties
    # advantages
    # drawbacks
    # +inventory
    # +computed stats (combat & intrigue)
