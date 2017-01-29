#!/usr/bin/env python
# -*- coding: utf-8 -*-

# macros manager

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if "base" not in globals():
    base = declarative_base()


class Macro(base):
    __tablename__ = 'macro'

    id = Column(Integer, primary_key=True)
    discord_userid = Column(String(40), nullable=False)
    name = Column(String(24), nullable=False)
    roll = Column(String(600), nullable=False)
    comment = Column(String(600), nullable=True)

if __name__ == '__main__':
    from sqlalchemy import create_engine

    engine = create_engine('sqlite:///bot.db')
    base.metadata.create_all(engine)
