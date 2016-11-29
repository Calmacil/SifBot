#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sifbot import skills

engine = create_engine('sqlite:///bot.db')
base = declarative_base()
base.metadata.create_all(engine)    # bouik

DBSession = sessionmaker(bind=engine)
dbs = DBSession()

skills.populate(dbs)
