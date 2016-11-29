# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if 'base' not in globals():
    base = declarative_base()


class Edge(base):
    """ Table gérant les avantages et les défauts """

    __tablename__ = "edges"

    id = Column(Integer, primary_key = True)
    flaw = Column(Integer, nullable = False, default = 0) # set to 1 if it is a flaw
    name = Column(String(32), nullable = False)
    short_desc = String(128)
    conditions = relationship("EdgeCondition")


class EdgeCondition(base):
    """ Conditions to buy an Edge.

    Types:
        0 - None
        1 - Character creation only
        2 - Ability
        3 - Specialty
        4 - Custom -> will be precised in the description
    """

    __tablename__ = "edge_conditions"

    id = Column(Integer, primary_key = True)
    edge_id = Column(Integer, nullable = False, ForeignKey = "edges.id"
    type = Column(Integer, nullable = False)
    foreign_id = Column(Integer, nullable = True) # no foreign key, queries have to be Custom
    value = Column(Integer, nullable = True, default = None)
