# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property

from sifbot.skills import Ability, Specialty
from sifbot.edges import Edge

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
    injuries = Column(Integer, nullable = False, default=0)
    wounds = Column(Integer, nullable=False, default=0)
    current_composure = Column(Integer, nullable = False) # Sang-froid
    current_health = Column(Integer, nullable = False)

    abilities = relationship("CharacterAbility")
    edges = relationship("CharacterEdge")

    @hybrid_property
    def intrigue_defense(self):
        """ SD à battre pour atteindre le personnage en intrigue """
        return self.ab_awa + self.ab_cun + self.ab_sta

    @hybrid_property
    def composure(self):
        """ Sang-froid; santé d’intrigue """
        return self.ab_wil * 3

    @hybrid_property
    def combat_defense(self):
        """ SD à battre pour toucher le personnage au combat """
        # TODO: ajouter Malus d’Armure et propriétés Défensives des armes et boucliers
        return self.ab_agi + self.ab_ath + self.ab_awa

    @hybrid_property
    def health(self):
        return self.ab_end * 3

    # +inventory
    # +computed stats (combat & intrigue)

    def __getattr__(self, key):
        skey = key.split("_")

        if skey[0] == "ab":
            return abilities.filter(CharacterAbility.ability_id == skey[1])
        elif skey[0] == "ed":
            return edges.filter(CharacterEdge.edge_id == skey[1])


class CharacterAbility(base):
    """ Link table between Character and Ability """

    __tablename__ = "character_abilities"

    character_id = Column(Integer, primary_key = True, ForeignKey = "characters.id")
    ability_id = Column(Integer, primary_key = True, ForeignKey = "abilities.id")
    value = Column(Integer, nullable = False, default = 2)

    specialties = relationship("CharacterAbility")

    def __getattr__(self, key):
        """ poum """
        return specialties.filter(Specialty.short == key)


class CharacterAbilitySpecialty(base):
    """ Link table between CharacterAbility and Specialty """

    __tablename__ = "character_ability_specialties"

    character_id = Column(Integer, primary_key = True, ForeignKey = "character_abilities.character_id")
    ability_id = Column(Integer, primary_key = True, ForeignKey = "character_abilities.ability_id")
    speciality_id = Column(Integer, primary_key = True, ForeignKey = "abilities.id")
    value = Column(Integer, nullable = False, default = 0)


class CharacterEdge(base):
    """ Link table for characters and edges"""

    __tablename__ = "character_edges"

    character_id = Column(Integer, primary_key = True, ForeignKey = "character.id")
    edge_id = Column(Integer, primary_key = True, ForeignKey = "edge.id")

    edge = relationship("Edge")
