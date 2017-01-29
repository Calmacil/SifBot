#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if 'base' not in globals():
    base = declarative_base()

class Item(base):
    """ Classe représentant un objet utilisable dans l’inventaire """

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    description = Column(String(512))
    min_cost = Column(Integer, nullable=False) # money value in copper half-pence (les sous)
    max_cost = Column(Integer, nullable=True) # max money value in copper half-pence.
    weight = Column(Integer, nullable=False, default=0) # weight in pounds - half a kilogram
    is_money = Column(Boolean, default=False)


class Weapon(base):
    """ Well, weapons. """

    __tablename__ = "weapons"

    item_id = Column(Integer, primary_key=True, ForeignKey("items.id"))
    spe_sname = Column(String(3), nullable=False)
    training = Column(Integer, nullable=False) # level needed in the specialty to use weapon accurately
    damage_skill = Column(String(3), nullable=False) # skill short name
    damage_modifier = Column(Integer, nullable=False, default=0)

    item = relationship("Item")
    qualities = relationship("WeaponQuality")

class Quality(base):
    """ Weapon qualities management """

    __tablename__ = "qualities"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    short_name = Column(String(4), nullable=False)
    description = Column(String(512))

class WeaponQuality(base):
    """ Link table """

    __tablename__ = "weapon_qualities"

    weapon_id = Column(Integer, primary_key=True, ForeignKey("weapons.id"))
    quality_id = Column(Integer, primary_key=True, ForeignKey("qualities.id"))
    value = Column(Integer, default=0)


class Armor(base):
    """ Link table """

    __tablename__ = "armors"

    item_id = Column(Integer, primary_key=True, ForeignKey("items.id"))
    value = Column(Integer, nullable=False)
    malus = Column(Integer, nullable=False)
    encumbrance = Column(Integer, nullable=False)

    item = relationship("Item")


class Poison("base")
    """ Poisons. """

    __tablename__ = "poisons"

    item_id = Column(Integer, primary_key=True, ForeignKey("items.id"))
    inoculation = Column(String(32), nullable=False) # 1 - Ingestion, 2 - Contact, 3 - Inhalation
    virulence = Column(Integer, nullable=False)
    frequency = Column(String(32), nullable=False)
    toxicity = Column(Integer, nullable=False)
    diagnostic = Column(Integer, nullable=False)


def populate(dbs):
    pass
