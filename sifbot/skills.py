# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

if 'base' not in globals():
    base = declarative_base()


class Ability(base):
    """ Compétence """

    __tablename__ = "abilities"

    id = Column(Integer, primary_key = True)
    name = Column(String(16), nullable = False)
    short = Column(String(3), nullable = False)

    specialties = relationship("Specialty", back_populates="skill")

class Specialty(base):
    """ Spécialisations """

    __tablename__ = "specialties"

    id = Column(Integer, primary_key = True)
    name = Column(String(20), nullable = False)
    short = Column(String(4), nullable = False)
    skill_id = Column(Integer, ForeignKey("abilities.id"))

    skill = relationship("Ability", back_populates="specialties")


def populate(dbs):
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///bot.db")
    base.metadata.create_all(engine)

    _abilities = [
        {'id': 1, 'name': 'Agilité', 'short': 'agi'},
        {'id': 2, 'name': 'Art Militaire', 'short': 'war'},
        {'id': 3, 'name': 'Athlétisme', 'short': 'ath'},
        {'id': 4, 'name': 'Connaissance', 'short': 'kno'},
        {'id': 5, 'name': 'Corps à Corps', 'short': 'fig'},
        {'id': 6, 'name': 'Discrétion', 'short': 'ste'},
        {'id': 7, 'name': 'Dressage', 'short': 'ani'},
        {'id': 8, 'name': 'Duperie', 'short': 'dec'},
        {'id': 9, 'name': 'Endurance', 'short': 'end'},
        {'id': 10, 'name': 'Ingéniosité', 'short': 'cun'},
        {'id': 11, 'name': 'Langue', 'short': 'lan'},
        {'id': 12, 'name': 'Larcin', 'short': 'thi'},
        {'id': 13, 'name': 'Persuasion', 'short': 'per'},
        {'id': 14, 'name': 'Soins', 'short': 'hea'},
        {'id': 15, 'name': 'Statut', 'short': 'sta'},
        {'id': 16, 'name': 'Survie', 'short': 'sur'},
        {'id': 17, 'name': 'Tir', 'short': 'mar'},
        {'id': 18, 'name': 'Vigilance', 'short': 'awa'},
        {'id': 19, 'name': 'Volonté', 'short': 'wil'}
    ]

    _specialties = [
        {'id': 1, 'name': 'Acrobaties', 'short': 'acr', 'skill_id': 1},
        {'id': 2, 'name': 'Équilibre', 'short': 'bal', 'skill_id': 1},
        {'id': 3, 'name': 'Contorsions', 'short': 'con', 'skill_id': 1},
        {'id': 4, 'name': 'Esquive', 'short': 'dod', 'skill_id': 1},
        {'id': 5, 'name': 'Vivacité', 'short': 'viv', 'skill_id': 1},
        {'id': 6, 'name': 'Commandement', 'short': 'com', 'skill_id': 2},
        {'id': 7, 'name': 'Stratégie', 'short': 'stg', 'skill_id': 2},
        {'id': 8, 'name': 'Tactique', 'short': 'tac', 'skill_id': 2},
        {'id': 9, 'name': 'Escalade', 'short': 'cli', 'skill_id': 3},
        {'id': 10, 'name': 'Saut', 'short': 'jum', 'skill_id': 3},
        {'id': 11, 'name': 'Course', 'short': 'run', 'skill_id': 3},
        {'id': 12, 'name': 'Force', 'short': 'str', 'skill_id': 3},
        {'id': 13, 'name': 'Natation', 'short': 'swi', 'skill_id': 3},
        {'id': 14, 'name': 'Jet', 'short': 'thr', 'skill_id': 3},
        {'id': 15, 'name': 'Éducation', 'short': 'edu', 'skill_id': 4},
        {'id': 16, 'name': 'Recherches', 'short': 'res', 'skill_id': 4},
        {'id': 17, 'name': 'Connaissance de la rue', 'short': 'stt', 'skill_id': 4},
        {'id': 18, 'name': 'Haches', 'short': 'axe', 'skill_id': 5},
        {'id': 19, 'name': 'Casse-têtes', 'short': 'blu', 'skill_id': 5},
        {'id': 20, 'name': 'Rixe', 'short': 'stu', 'skill_id': 5},
        {'id': 21, 'name': 'Escrime', 'short': 'fen', 'skill_id': 5},
        {'id': 22, 'name': 'Lames longues', 'short': 'lbl', 'skill_id': 5},
        {'id': 23, 'name': 'Armes d’Hast', 'short': 'pol', 'skill_id': 5},
        {'id': 24, 'name': 'Lames courtes', 'short': 'sbl', 'skill_id': 5},
        {'id': 25, 'name': 'Lances', 'short': 'spe', 'skill_id': 5},
        {'id': 26, 'name': 'Boucliers', 'short': 'shd', 'skill_id': 5},
        {'id': 27, 'name': 'Caméléon', 'short': 'cam', 'skill_id': 6},
        {'id': 28, 'name': 'Furtivité', 'short': 'fur', 'skill_id': 6},
        {'id': 29, 'name': 'Charme', 'short': 'cha', 'skill_id': 7},
        {'id': 30, 'name': 'Conduite', 'short': 'dri', 'skill_id': 7},
        {'id': 31, 'name': 'Équitation', 'short': 'rid', 'skill_id': 7},
        {'id': 32, 'name': 'Exercices', 'short': 'exc', 'skill_id': 7},
        {'id': 33, 'name': 'Comédie', 'short': 'cod', 'skill_id': 8},
        {'id': 34, 'name': 'Bluff', 'short': 'blf', 'skill_id': 8},
        {'id': 35, 'name': 'Triche', 'short': 'che', 'skill_id': 8},
        {'id': 36, 'name': 'Déguisement', 'short': 'dis', 'skill_id': 8},
        {'id': 37, 'name': 'Résilience', 'short': 'rsl', 'skill_id': 9},
        {'id': 38, 'name': 'Vigueur', 'short': 'vig', 'skill_id': 9},
        {'id': 39, 'name': 'Décryptage', 'short': 'unc', 'skill_id': 10},
        {'id': 40, 'name': 'Logique', 'short': 'log', 'skill_id': 10},
        {'id': 41, 'name': 'Mémoire', 'short': 'mem', 'skill_id': 10},
        {'id': 42, 'name': 'Crochetage', 'short': 'lpk', 'skill_id': 12},
        {'id': 43, 'name': 'Passe-passe', 'short': 'trk', 'skill_id': 12},
        {'id': 44, 'name': 'Vol', 'short': 'stl', 'skill_id': 12},
        {'id': 45, 'name': 'Marchander', 'short': 'bar', 'skill_id': 13},
        {'id': 46, 'name': 'Charmer', 'short': 'cha', 'skill_id': 13},
        {'id': 47, 'name': 'Convaincre', 'short': 'cnv', 'skill_id': 13},
        {'id': 48, 'name': 'Inciter', 'short': 'inc', 'skill_id': 13},
        {'id': 49, 'name': 'Intimider', 'short': 'int', 'skill_id': 13},
        {'id': 50, 'name': 'Séduire', 'short': 'sed', 'skill_id': 13},
        {'id': 51, 'name': 'Persifler', 'short': 'jer', 'skill_id': 13},
        {'id': 52, 'name': 'Diagnostic', 'short': 'dia', 'skill_id': 14},
        {'id': 53, 'name': 'Infections', 'short': 'inf', 'skill_id': 14},
        {'id': 54, 'name': 'Blessures', 'short': 'inj', 'skill_id': 14},
        {'id': 55, 'name': 'Fourrageur', 'short': 'for', 'skill_id': 16},
        {'id': 56, 'name': 'Chasse', 'short': 'hun', 'skill_id': 16},
        {'id': 57, 'name': 'Orientation', 'short': 'ori', 'skill_id': 16},
        {'id': 58, 'name': 'Pistage', 'short': 'tra', 'skill_id': 16},
        {'id': 59, 'name': 'Arcs', 'short': 'bow', 'skill_id': 17},
        {'id': 60, 'name': 'Arbalètes', 'short': 'crs', 'skill_id': 17},
        {'id': 61, 'name': 'Siège', 'short': 'sig', 'skill_id': 17},
        {'id': 62, 'name': 'Jet', 'short': 'thw', 'skill_id': 17},
        {'id': 63, 'name': 'Empathie', 'short': 'emp', 'skill_id': 18},
        {'id': 64, 'name': 'Observation', 'short': 'obs', 'skill_id': 18},
        {'id': 65, 'name': 'Courage', 'short': 'crg', 'skill_id': 19},
        {'id': 66, 'name': 'Coordination', 'short': 'crd', 'skill_id': 19},
        {'id': 67, 'name': 'Dévouement', 'short': 'dev', 'skill_id': 19},
        {'id': 68, 'name': 'Bienséance', 'short': 'pro', 'skill_id': 15},
        {'id': 69, 'name': 'Réputation', 'short': 'rep', 'skill_id': 15},
        {'id': 70, 'name': 'Intendance', 'short': 'mng', 'skill_id': 15},
        {'id': 71, 'name': 'Tournois', 'short': 'trn', 'skill_id': 15}
    ]

    for ab in _abilities:
        the_ability = Ability(**ab)
        dbs.add(the_ability)

    for spe in _specialties:
        the_specialty = Specialty(**spe)
        dbs.add(the_specialty)

    return dbs.commit()
