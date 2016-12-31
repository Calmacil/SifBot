# -*- coding: utf-8 -*-

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
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
    multiple = Column(Boolean, nullable = False, default = False)
    conditions = relationship("EdgeCondition")


class EdgeCondition(base):
    """ Conditions to buy an Edge.

    Types:
        0 - None
        1 - Character creation only
        2 - Ability
        3 - Specialty
        4 - Edge
        5 - Custom -> will be precised in the description
    """

    __tablename__ = "edge_conditions"

    id = Column(Integer, primary_key = True)
    edge_id = Column(Integer, ForeignKey("edges.id"), nullable = False)
    type = Column(Integer, nullable = False)
    foreign_id = Column(Integer, nullable = True) # no foreign key, queries have to be Custom
    value = Column(Integer, nullable = True, default = None)


def populate(dbs):
    from sqlalchemy import create_engine
    engine = create_engine("sqlite:///bot.db")
    base.metadata.create_all(engine)

    #_edges = [
    #    {'id': 1, 'flaw': 0, 'name': 'some name', 'short_desc': 'some desc'},
    #]
    _edges = []
    _conditions = []

    """ Ability Edges """
    _edges.append({'id': 1, 'name': 'Adroit', 'short_desc': 'Relancez les 1 lors des tests d’Agilité'})
    _conditions.append({'edge_id': 1, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 2, 'name': 'Ami des bêtes', 'short_desc': '+1D aux tests de Dressage utilisés avec les spécialités Charmer et Exercices'})
    _conditions.append({'edge_id': 2, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 3, 'name': 'Amuseur', 'short_desc': 'Vous pouvez divertir un public.'}) # todo preciser
    _conditions.append({'edge_id': 3, 'type': 2, 'foreign_id': 13, 'value': 3})

    _edges.append({'id': 4, 'name': 'Artiste', 'short_desc': 'Vous créez des œuvres d’art'}) # todo préciser
    _conditions.append({'edge_id': 4, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 5, 'name': 'Athlète-né', 'short_desc': 'Convertissez la moité de vos dés de bonus en dés de test pour la spé choisie', 'multiple': True})
    _conditions.append({'edge_id': 5, 'type': 2, 'foreign_id': 3, 'value': 4})

    _edges.append({'id': 6, 'name': 'Connaissances précises: alchimie', 'short_desc': 'Convertissez la moitié de vos dés de bonus en dés de test pour la spé choisie', 'multiple': True})
    _conditions.append({'edge_id': 6, 'type': 2, 'foreign_id': 4, 'value': 4})

    _edges.append({'id': 7, 'name': 'Évaluation', 'short_desc': 'Test d’Ingéniosité pour avoir des informations sur un objet'})
    _conditions.append({'edge_id': 7, 'type': 2, 'foreign_id': 4, 'value': 3})

    _edges.append({'id': 8, 'name': 'Expertise', 'short_desc': 'Gagnez +1D dans une spécialité', 'multiple': True})
    _conditions.append({'edge_id': 8, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 9, 'name': 'Faiseur de miracles', 'short_desc': 'Diagnostiquez vos patients pour gagner des bonus'}) # todo préciser
    _conditions.append({'edge_id': 9, 'type': 2, 'foreign_id': 14, 'value': 4})

    _edges.append({'id': 10, 'name': 'Fin gestionnaire', 'short_desc': 'Ajoutez votre Ingéniosité au résultat du test de Statut lors des événements de maison et relancez les 1 lors des tests de Statut générant de l’argent'})
    _conditions.append({'edge_id': 10, 'type': 2, 'foreign_id': 15, 'value': 3})
    _conditions.append({'edge_id': 10, 'type': 3, 'foreign_id': 70, 'value': 1})

    _edges.append({'id': 11, 'name': 'Furtif', 'short_desc': 'Relancez les 1 lors des tests de Furtivité et ajoutez votre rang d’Agilité au résultat'})
    _conditions.append({'edge_id': 11, 'type': 2, 'foreign_id': 6, 'value': 4})
    _conditions.append({'edge_id': 11, 'type': 3, 'foreign_id': 28, 'value': 1})

    _edges.append({'id': 12, 'name': 'Grand chasseur', 'short_desc': 'Bonus lorsque vous combattez, chassez et traquez des animaux'}) # todo préciser
    _conditions.append({'edge_id': 12, 'type': 2, 'foreign_id': 16, 'value': 4})

    _edges.append({'id': 13, 'name': 'Mémoire eidétique', 'short_desc': 'Les dés de bonus de Mémoire se transforment en dés de test.'})
    _conditions.append({'edge_id': 13, 'type': 2, 'foreign_id': 10, 'value': 2})
    _conditions.append({'edge_id': 13, 'type': 3, 'foreign_id': 41, 'value': 1})

    _edges.append({'id': 14, 'name': 'Métier', 'short_desc': 'Vous apprenez un métier.'})
    _conditions.append({'edge_id': 14, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 15, 'name': 'Pédagogue', 'short_desc': 'Confère des dés de bonus aux élèves'})
    _conditions.append({'edge_id': 15, 'type': 2, 'foreign_id': 4, 'value': 4})
    _conditions.append({'edge_id': 15, 'type': 2, 'foreign_id': 13, 'value': 3})

    _edges.append({'id': 16, 'name': 'Polyglotte', 'short_desc': 'Vous apprenez facilement les langues étrangères'})
    _conditions.append({'edge_id': 16, 'type': 2, 'foreign_id': 10, 'value': 4})
    _conditions.append({'edge_id': 16, 'type': 3, 'foreign_id': 39, 'value': 1})

    _edges.append({'id': 17, 'name': 'Réseau', 'short_desc': '+1D aux tests de Connaissance dans la zone choisie', 'multiple': True})
    _conditions.append({'edge_id': 17, 'type': 3, 'foreign_id': 17, 'value': 1})

    _edges.append({'id': 18, 'name': 'Robuste', 'short_desc': 'Ignorez -1 ou -1D aux tests d’Endurance destinés à récupérer des lésions et blessures'})
    _conditions.append({'edge_id': 18, 'type': 2, 'foreign_id': 9, 'value': 3})
    _conditions.append({'edge_id': 18, 'type': 3, 'foreign_id': 38, 'value': 1})

    _edges.append({'id': 19, 'name': 'Se fondre dans la foule', 'short_desc': 'Utilisez Caméléon en tant qu’action franche et ajoutez votre rang d’Ingéniosité au résultat des tests de Caméléon'})
    _conditions.append({'edge_id': 19, 'type': 2, 'foreign_id': 6, 'value': 3})
    _conditions.append({'edge_id': 19, 'type': 3, 'foreign_id': 27, 'value': 1})

    _edges.append({'id': 20, 'name': 'Sens aiguisés', 'short_desc': 'Relancez les 1 lors des tests de Vigilance et ajoutez votre rang d’Ingéniosité à votre Vigilance passive'})
    _conditions.append({'edge_id': 20, 'type': 2, 'foreign_id': 18, 'value': 4})

    _edges.append({'id': 21, 'name': 'Sinistre', 'short_desc': 'Vous avez une aura menaçante'}) # todo préciser
    _conditions.append({'edge_id': 21, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 22, 'name': 'Spécialiste de terrain', 'short_desc': 'Ajoutez votre rang d’Éducation au résultat des tests de Survie sur le terrain choisi', 'multiple': True})
    _conditions.append({'edge_id': 22, 'type': 2, 'foreign_id': 16, 'value': 4})

    _edges.append({'id': 23, 'name': 'Talentueux', 'short_desc': 'Ajoutez +1 aux résultats des tests de la compétence choisie', 'multiple': True})
    _conditions.append({'edge_id': 23, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 24, 'name': 'Voyou', 'short_desc': 'Relancez les 1 lors des tests de Larcin'})
    _conditions.append({'edge_id': 24, 'type': 0, 'foreign_id': None})


    """ Fate Edges """

    _edges.append({'id': 25, 'name': 'Célèbre', 'short_desc': 'Votre célébrité vous avantage lors des intrigues'}) # todo préciser
    _conditions.append({'edge_id': 25, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 26, 'name': 'Chanceux', 'short_desc': 'Rejouez un test par jour et conservez le meilleur résultat'})
    _conditions.append({'edge_id': 26, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 27, 'name': 'Chef de famille', 'short_desc': 'Vous êtes le membre de plus haut rang de votre maison'})
    _conditions.append({'edge_id': 27, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 28, 'name': 'Compagnon', 'short_desc': 'Gagnez les services d’un allié dévoué'})
    _conditions.append({'edge_id': 28, 'type': 2, 'foreign_id': 15, 'value': 3})

    _edges.append({'id': 29, 'name': 'Mécène', 'short_desc': 'Gagnez un puissant allié'})
    _conditions.append({'edge_id': 29, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 30, 'name': 'Fief', 'short_desc': 'Vous gagnez des terres et des biens'})
    _conditions.append({'edge_id': 30, 'type': 4, 'foreign_id': 29})

    _edges.append({'id': 31, 'name': 'Frère de la Garde de Nuit', 'short_desc': 'Vous êtes membre de la Garde de Nuit'})
    _conditions.append({'edge_id': 31, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 32, 'name': 'Héritier', 'short_desc': 'Un jour, vous hériterez des terres et des biens de votre famille'})
    _conditions.append({'edge_id': 32, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 33, 'name': 'Héritage', 'short_desc': 'Vous gagnez une arme d’acier valyrien'})
    _conditions.append({'edge_id': 33, 'type': 4, 'foreign_id': 27})
    _conditions.append({'edge_id': 34, 'type': 4, 'foreign_id': 32})

    _edges.append({'id': 34, 'name': 'Maître des corbeaux', 'short_desc': 'Envoyez des corbeaux porter vos messages'})
    _conditions.append({'edge_id': 34, 'type': 2, 'foreign_id': 7, 'value': 3})

    _edges.append({'id': 35, 'name': 'Membre de la Garde Royale', 'short_desc': 'Vous êtes chargé de la protection de la famille royale'})
    _conditions.append({'edge_id': 35, 'type': 4, 'foreign_id': 29})

    _edges.append({'id': 36, 'name': 'Mestre', 'short_desc': 'Vous êtes un mestre de la Citadelle'})
    _conditions.append({'edge_id': 36, 'type': 2, 'foreign_id': 10, 'value': 3})
    _conditions.append({'edge_id': 36, 'type': 4, 'foreign_id': 6})

    _edges.append({'id': 37, 'name': 'Nyctalope', 'short_desc': 'Vous voyez dans le noir'})
    _conditions.append({'edge_id': 37, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 38, 'name': 'Pieux', 'short_desc': 'Gagnez +1D une fois par jour'})
    _conditions.append({'edge_id': 38, 'type': 2, 'foreign_id': 19, 'value': 3})
    _conditions.append({'edge_id': 38, 'type': 3, 'foreign_id': 67, 'value': 1})

    _edges.append({'id': 39, 'name': 'Compagnon animal', 'short_desc': 'Gagnez les services d’un animal dévoué'})
    _conditions.append({'edge_id': 39, 'type': 2, 'foreign_id': 7, 'value': 3})
    _conditions.append({'edge_id': 39, 'type': 3, 'foreign_id': 32, 'value': 1})

    _edges.append({'id': 40, 'name': 'Rêves de loup', 'short_desc': 'Vous rêvez parfois par les yeux de votre compagnon animal'})
    _conditions.append({'edge_id': 40, 'type': 2, 'foreign_id': 19, 'value': 4})
    _conditions.append({'edge_id': 40, 'type': 3, 'foreign_id': 67, 'value': 1})
    _conditions.append({'edge_id': 40, 'type': 4, 'foreign_id': 39})

    _edges.append({'id': 41, 'name': 'Riche', 'short_desc': 'Vos coffres se remplissent chaque mois'})
    _conditions.append({'edge_id': 41, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 42, 'name': 'Unité', 'short_desc': 'Vous avez une escouade de vétérans à vos côtés'})
    _conditions.append({'edge_id': 42, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 43, 'name': 'Vervue', 'short_desc': 'Vous faites des rêves qui se réalisent'})
    _conditions.append({'edge_id': 43, 'type': 2, 'foreign_id': 19, 'value': 5})

    _edges.append({'id': 44, 'name': 'Zoman mineur', 'short_desc': 'Entrez dans la peau de votre compagnon animal'})
    _conditions.append({'edge_id': 44, 'type': 2, 'foreign_id': 19, 'value': 5})
    _conditions.append({'edge_id': 44, 'type': 3, 'foreign_id': 67, 'value': 2})
    _conditions.append({'edge_id': 44, 'type': 4, 'foreign_id': 40})

    _edges.append({'id': 45, 'name': 'Zoman', 'short_desc': 'Vous pouvez entrer dans la peau d’autres animaux que votre compagnon'})
    _conditions.append({'edge_id': 45, 'type': 4, 'foreign_id': 44})


    """ Inherited Edges """
    _edges.append({'id': 46, 'name': 'Immense', 'short_desc': 'Vous êtes d’une taille hors du commun'})
    _conditions.append({'edge_id': 46, 'type': 2, 'foreign_id': 9, 'value': 5})
    _conditions.append({'edge_id': 46, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 47, 'name': 'Sang de Valyria', 'short_desc': 'Les gens vous trouvent convaincant'}) # todo préciser
    _conditions.append({'edge_id': 47, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 48, 'name': 'Sang des Andals', 'short_desc': 'Vous avez une chance hors du commun'}) # todo préciser
    _conditions.append({'edge_id': 48, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 49, 'name': 'Sang des Fer-nés', 'short_desc': 'Vous avez de l’eau salée dans les veines'}) # todo préciser
    _conditions.append({'edge_id': 49, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 50, 'name': 'Sang des Héros', 'short_desc': 'Une de vos compétences peut dépasser le rang 7'})
    _conditions.append({'edge_id': 50, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 51, 'name': 'Sang des Premiers Hommes', 'short_desc': 'Votre héritage vous rend robuste et résistant'}) # todo préciser
    _conditions.append({'edge_id': 51, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 52, 'name': 'Sang du Rhoynar', 'short_desc': 'Vous êtes agile et insaisissable'}) # todo préciser
    _conditions.append({'edge_id': 52, 'type': 1, 'foreign_id': None})

    _edges.append({'id': 53, 'name': 'Sang des sauvageons', 'short_desc': 'Vous êtes né libre de la tyrannie de Westeros'}) # todo préciser
    _conditions.append({'edge_id': 53, 'type': 1, 'foreign_id': None})


    """ Martial edges """
    _edges.append({'id': 54, 'name': 'Coriace', 'short_desc': 'Azoutez votre Résilience à votre Santé'})
    _conditions.append({'edge_id': 54, 'type': 3, 'foreign_id': 37, 'value': 1})

    _edges.append({'id': 55, 'name': 'Danseur d’eau', 'short_desc': 'Ajoutez votre rang de Corps à corps au résultat des tests de Vigilance'})
    _conditions.append({'edge_id': 55, 'type': 2, 'foreign_id': 5, 'value': 3})

    _edges.append({'id': 56, 'name': 'Danseur d’eau 2', 'short_desc': 'Ajoutez votre rang de Corps à corps au résultat de vos tests d’Agilité'})
    _conditions.append({'edge_id': 56, 'type': 4, 'foreign_id': 55})

    _edges.append({'id': 57, 'name': 'Danseur d’eau 3', 'short_desc': 'Ajoutez votre Escrime à votre défense de combat'})
    _conditions.append({'edge_id': 57, 'type': 4, 'foreign_id': 56})

    _edges.append({'id': 58, 'name': 'Défense acrobatique', 'short_desc': 'Utilisez une action mineure pour ajouter le double de votre Acrobatie à votre Défense de combat' })
    _conditions.append({'edge_id': 58, 'type': 2, 'foreign_id': 1, 'value': 4})
    _conditions.append({'edge_id': 58, 'type': 3, 'foreign_id': 1, 'value': 1})

    _edges.append({'id': 59, 'name': 'Exaltant', 'short_desc': 'Gagnez un ordre supplémentaire, et sacrifiez un ordre pour rejouer un test'})
    _conditions.append({'edge_id': 59, 'type': 2, 'foreign_id': 2, 'value': 4})

    _edges.append({'id': 60, 'name': 'Fou de guerre', 'short_desc': 'Effectuez une attaque gratuite à chaque lésion ou blessure; combattez au-delà de la mort'})
    _conditions.append({'edge_id': 60, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 61, 'name': 'Fureur', 'short_desc': 'Subissez un malus de -2D pour obtenir +4 aux dégâts'})
    _conditions.append({'edge_id': 61, 'type': 2, 'foreign_id': 3, 'value': 4})
    _conditions.append({'edge_id': 61, 'type': 3, 'foreign_id': 12, 'value': 2})

    _edges.append({'id': 62, 'name': 'Grêle d’acier', 'short_desc': 'Les armes de Jet bénéficient tde la qualité Rapide entre vos mains'})
    _conditions.append({'edge_id': 62, 'type': 2, 'foreign_id': 17, 'value': 4})
    _conditions.append({'edge_id': 62, 'type': 3, 'foreign_id': 62, 'value': 2})

    _edges.append({'id': 63, 'name': 'Lutteur', 'short_desc': 'Vos poings deviennent des armes Rapides qui infligent des dégâts supplémentaires'}) # todo préciser
    _conditions.append({'edge_id': 63, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 63, 'type': 3, 'foreign_id': 20, 'value': 1})

    _edges.append({'id': 64, 'name': 'Lutteur 2', 'short_desc': 'Vos poings deviennent des armes Puissantes et vous ajoutez votre rang d’Athlétisme aux résultats des tests de CàC'})
    _conditions.append({'edge_id': 64, 'type': 3, 'foreign_id': 20, 'value': 3})
    _conditions.append({'edge_id': 64, 'type': 4, 'foreign_id': 63})

    _edges.append({'id': 65, 'name': 'Lutteur 3', 'short_desc': 'Vous pouvez assomer vos adversaires à mains nues'})
    _conditions.append({'edge_id': 65, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 65, 'type': 3, 'foreign_id': 20, 'value': 5})
    _conditions.append({'edge_id': 65, 'type': 4, 'foreign_id': 64})

    _edges.append({'id': 66, 'name': 'Maître Braavien', 'short_desc': 'Augmente de 1 le Bonus défensif'})
    _conditions.append({'edge_id': 66, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 66, 'type': 3, 'foreign_id': 21, 'value': 1})

    _edges.append({'id': 67, 'name': 'Maître Braavien 2', 'short_desc': 'Améliore votre Défense de combat'})
    _conditions.append({'edge_id': 67, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 67, 'type': 3, 'foreign_id': 21, 'value': 2})
    _conditions.append({'edge_id': 67, 'type': 4, 'foreign_id': 66})

    _edges.append({'id': 68, 'name': 'Maître Braavien 3', 'short_desc': 'Bénéficiez d’une attaque gratuite quand l’ennemi vous rate'})
    _conditions.append({'edge_id': 68, 'type': 2, 'foreign_id': 5, 'value': 6})
    _conditions.append({'edge_id': 68, 'type': 3, 'foreign_id': 21, 'value': 3})
    _conditions.append({'edge_id': 68, 'type': 4, 'foreign_id': 67})

    _edges.append({'id': 69, 'name': 'Maître d’armes inné', 'short_desc': 'Ignorez les conditions requises pour le maniement des armes et les malus associés'})
    _conditions.append({'edge_id': 69, 'type': 2, 'foreign_id': 1, 'value': 4})
    _conditions.append({'edge_id': 69, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 69, 'type': 2, 'foreign_id': 10, 'value': 4})

    _edges.append({'id': 70, 'name': 'Maître des armes d’Hast', 'short_desc': 'Balayez vos ennemis pour les jeter à terre'})
    _conditions.append({'edge_id': 70, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 70, 'type': 3, 'foreign_id': 23, 'value': 2})

    _edges.append({'id': 71, 'name': 'Maître des armes d’Hast 2', 'short_desc': 'Vos dés de bonus deviennent des dés de test pour jeter à terre les cavaliers'})
    _conditions.append({'edge_id': 71, 'type': 4, 'foreign_id': 70})

    _edges.append({'id': 72, 'name': 'Maître des armes d’Hast 3', 'short_desc': 'Immobilisez vos adversaires à l’aide de votre arme'})
    _conditions.append({'edge_id': 72, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 72, 'type': 4, 'foreign_id': 71})

    _edges.append({'id': 73, 'name': 'Maître des Casse-têtes', 'short_desc': 'L’arme que vous maniez gagne la qualité Fracassante ou l’augmente de 1'})
    _conditions.append({'edge_id': 73, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 73, 'type': 3, 'foreign_id': 19, 'value': 2})

    _edges.append({'id': 74, 'name': 'Maître des Casse-têtes 2', 'short_desc': 'Votre adversaire est réduit à 1 action mineure et subit -1 aux tests si vous le touchez'})
    _conditions.append({'edge_id': 74, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 74, 'type': 3, 'foreign_id': 19, 'value': 3})
    _conditions.append({'edge_id': 74, 'type': 4, 'foreign_id': 73})

    _edges.append({'id': 75, 'name': 'Maître des Casse-têtes 3', 'short_desc': 'Votre adversaire subit une blessure, tombe à terre et perd ses actions.'})
    _conditions.append({'edge_id': 75, 'type': 2, 'foreign_id': 5, 'value': 6})
    _conditions.append({'edge_id': 75, 'type': 3, 'foreign_id': 19, 'value': 4})
    _conditions.append({'edge_id': 75, 'type': 4, 'foreign_id': 74})

    _edges.append({'id': 76, 'name': 'Maître des Haches', 'short_desc': 'Sacrifiez des dés de bonus pour infliger des dégâts supplémentaires.'})
    _conditions.append({'edge_id': 76, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 76, 'type': 3, 'foreign_id': 18, 'value': 2})

    _edges.append({'id': 77, 'name': 'Maître des Haches 2', 'short_desc': 'Sacrifiez des dés de bonus pour infliger une blessure.'})
    _conditions.append({'edge_id': 77, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 77, 'type': 3, 'foreign_id': 18, 'value': 3})
    _conditions.append({'edge_id': 77, 'type': 4, 'foreign_id': 76})

    _edges.append({'id': 78, 'name': 'Maître des Haches 3', 'short_desc': 'Sacrifiez des dés de bonus pour infliger une blessure et l’attribut Mutilé.'})
    _conditions.append({'edge_id': 78, 'type': 2, 'foreign_id': 5, 'value': 6})
    _conditions.append({'edge_id': 78, 'type': 3, 'foreign_id': 18, 'value': 4})
    _conditions.append({'edge_id': 78, 'type': 4, 'foreign_id': 77})

    _edges.append({'id': 79, 'name': 'Maître des lames courtes', 'short_desc': 'Les lames courtes deviennent Perforantes entre vos mains.'})
    _conditions.append({'edge_id': 79, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 79, 'type': 3, 'foreign_id': 24, 'value': 1})

    _edges.append({'id': 80, 'name': 'Maître des lames courtes 2', 'short_desc': 'Dégainez au moyen d’une action franche, obtenez un bonus au résultat des tests.'})
    _conditions.append({'edge_id': 80, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 80, 'type': 4, 'foreign_id': 79})

    _edges.append({'id': 81, 'name': 'Maître des lames courtes 3', 'short_desc': 'Le nombre de vos dés de bonus s’ajoute aux dégâts.'})
    _conditions.append({'edge_id': 81, 'type': 2, 'foreign_id': 5, 'value': 6})
    _conditions.append({'edge_id': 81, 'type': 4, 'foreign_id': 80})

    _edges.append({'id': 82, 'name': 'Maître des lames longues', 'short_desc': 'Sacrifiez des dés de bonus pour obtenir un degré de réussite gratuite.'})
    _conditions.append({'edge_id': 82, 'type': 2, 'foreign_id': 5, 'value': 4})
    _conditions.append({'edge_id': 82, 'type': 3, 'foreign_id': 22, 'value': 2})

    _edges.append({'id': 83, 'name': 'Maître des lames longues 2', 'short_desc': 'Sacrifiez des dés de bonus pour déplacer la cible que vous frappez.'})
    _conditions.append({'edge_id': 83, 'type': 2, 'foreign_id': 5, 'value': 5})
    _conditions.append({'edge_id': 83, 'type': 4, 'foreign_id': 82})

    _edges.append({'id': 84, 'name': 'Maître des lames longues 3', 'short_desc': 'Sacrifiez des dés de bonus pour Mutiler un adversaire.'})
    _conditions.append({'edge_id': 84, 'type': 2, 'foreign_id': 5, 'value': 6})
    _conditions.append({'edge_id': 84, 'type': 4, 'foreign_id': 83})

    _edges.append({'id': 85, 'name': 'Maître des Lances', 'short_desc': 'Attaquez de nouveau après avoir raté'})
    _conditions.append({'edge_id': 85, 'type': 2, 'foreign_id': 5, 'value': 3})
    _conditions.append({'edge_id': 85, 'type': 3, 'foreign_id': 25, 'value': 1})

    _edges.append({'id': 86, 'name': 'Maître des Lances 2', 'short_desc': '+1D aux tentatives de Renversement; attaquez des adversaires situés à 1m de plus que d’ordinaire.'})
    _conditions.append({'edge_id': 86, 'type': 4, 'foreign_id': 85})

    _edges.append({'id': 87, 'name': 'Maître des Lances 3', 'short_desc': 'Les lances deviennent Perforantes 2 entre vos mains.'})
    _conditions.append({'edge_id': 87, 'type': 2, 'foreign_id': 3, 'value': 5})
    _conditions.append({'edge_id': 87, 'type': 4, 'foreign_id': 86})

    _edges.append({'id': 88, 'name': 'Maîtrise des armes', 'short_desc': 'Les dégâts des armes augmentent de 1.'})
    _conditions.append({'edge_id': 88, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 89, 'name': 'Maîtrise des armures', 'short_desc': 'Bonus à l’armure: +1 à la VA, Encombrante -1.'})
    _conditions.append({'edge_id': 89, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 90, 'name': 'Maîtrise des Boucliers', 'short_desc': 'Augmente votre Bonus défensif de 1 avec les boucliers.'})
    _conditions.append({'edge_id': 90, 'type': 2, 'foreign_id': 5, 'value': 3})
    _conditions.append({'edge_id': 90, 'type': 3, 'foreign_id': 26, 'value': 1})

    _edges.append({'id': 91, 'name': 'Maîtrise supérieure des armes', 'short_desc': 'Les dégâts des armes augmentent de 1.'})
    _conditions.append({'edge_id': 91, 'type': 4, 'foreign_id': 88})

    _edges.append({'id': 92, 'name': 'Maîtrise supérieure des armures', 'short_desc': 'La VA des armures aumente de 1, pour un total de +2.'})
    _conditions.append({'edge_id': 92, 'type': 4, 'foreign_id': 89})

    _edges.append({'id': 93, 'name': 'Meneur d’hommes', 'short_desc': 'Réorganisez ou ralliez automatiquement une unité.'})
    _conditions.append({'edge_id': 93, 'type': 2, 'foreign_id': 2, 'value': 4})
    _conditions.append({'edge_id': 93, 'type': 3, 'foreign_id': 6, 'value': 1})

    _edges.append({'id': 94, 'name': 'Oint', 'short_desc': '+2 aux tests de Statut, 1/jour: gagnez +5 à toutes les Défenses.'})
    _conditions.append({'edge_id': 94, 'type': 4, 'foreign_id': 29})

    _edges.append({'id': 95, 'name': 'Précis', 'short_desc': '+1D contre les adversaires disposant d’une couverture.'})
    _conditions.append({'edge_id': 95, 'type': 2, 'foreign_id': 17, 'value': 4})

    _edges.append({'id': 96, 'name': 'Rapide', 'short_desc': 'Votre déplacement augmente de 1m, et vous courez à 5x votre Déplacement.'})
    _conditions.append({'edge_id': 96, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 97, 'name': 'Rechargement rapide', 'short_desc': 'Réduit le temps de rechargement des armes.'})
    _conditions.append({'edge_id': 97, 'type': 2, 'foreign_id': 1, 'value': 4})

    _edges.append({'id': 98, 'name': 'Sixième sens', 'short_desc': 'Relancez les 1 lors des tests d’initiative, et annulez le bonus de +1D dont bénéficient ceux qui vous attaquent par surprise.'})
    _conditions.append({'edge_id': 98, 'type': 2, 'foreign_id': 18, 'value': 4})

    _edges.append({'id': 99, 'name': 'Tir double', 'short_desc': 'Tirez simultanément deux flèches.'})
    _conditions.append({'edge_id': 99, 'type': 2, 'foreign_id': 17, 'value': 5})
    _conditions.append({'edge_id': 99, 'type': 3, 'foreign_id': 59, 'value': 3})

    _edges.append({'id': 100, 'name': 'Tir triple', 'short_desc': 'Tirez trois flèches en même temps.'})
    _conditions.append({'edge_id': 100, 'type': 2, 'foreign_id': 17, 'value': 7})
    _conditions.append({'edge_id': 100, 'type': 3, 'foreign_id': 59, 'value': 5})
    _conditions.append({'edge_id': 100, 'type': 4, 'foreign_id': 99})

    _edges.append({'id': 101, 'name': 'Tireur d’élite', 'short_desc': 'Les arcs et les arbalètes bénéficient des qualités Perforante 1 et Hargneuse entre vos mains.'})
    _conditions.append({'edge_id': 101, 'type': 2, 'foreign_id': 17, 'value': 5})

    _edges.append({'id': 102, 'name': 'Vétéran des tournois', 'short_desc': 'Ajoutez votre nombre de dés de bonus au résultat des tests de Corps à corps et de Dressage pendant les joutes.'})
    _conditions.append({'edge_id': 102, 'type': 2, 'foreign_id': 5, 'value': 3})
    _conditions.append({'edge_id': 102, 'type': 2, 'foreign_id': 15, 'value': 3})
    _conditions.append({'edge_id': 102, 'type': 3, 'foreign_id': 25, 'value': 1})
    _conditions.append({'edge_id': 102, 'type': 3, 'foreign_id': 71, 'value': 1})

    """ Social edges """
    _edges.append({'id': 103, 'name': 'Apprécié par le peuple', 'short_desc': '+1B aux tests de Persuasion contre les personnages dont le Statut est inférieur ou égal à 3.'})
    _conditions.append({'edge_id': 103, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 104, 'name': 'Apprécié par les nobles', 'short_desc': '+1B aux tests de Persuasion contre les personnages dont le Statut est supérieur ou égal à 4.'})
    _conditions.append({'edge_id': 104, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 105, 'name': 'Autorité', 'short_desc': 'Réduisez de 2 les malus dus à l’humeur affectant la Persuasion.'})
    _conditions.append({'edge_id': 105, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 106, 'name': 'Charismatique', 'short_desc': 'Ajoutez 2 au résultat des tests de Persuasion.', 'multiple': True})
    _conditions.append({'edge_id': 106, 'type': 2, 'foreign_id': 13, 'value': 3})

    _edges.append({'id': 107, 'name': 'Convaincant', 'short_desc': 'Votre Influence avec une spécialité augmente de 1.', 'multiple': True})
    _conditions.append({'edge_id': 107, 'type': 4, 'foreign_id': 106})

    _edges.append({'id': 108, 'name': 'Courtois', 'short_desc': 'Vos manières sont irréprochables.'})
    _conditions.append({'edge_id': 108, 'type': 2, 'foreign_id': 13, 'value': 3})

    _edges.append({'id': 109, 'name': 'Dévoué', 'short_desc': 'Votre loyauté est inébranlable.'})
    _conditions.append({'edge_id': 109, 'type': 2, 'foreign_id': 19, 'value': 4})

    _edges.append({'id': 110, 'name': 'Diplomate avisé', 'short_desc': 'Conservez tous les dés de bonus de l’action Réfléchir pendant les intrigues.'})
    _conditions.append({'edge_id': 110, 'type': 2, 'foreign_id': 18, 'value': 4})
    _conditions.append({'edge_id': 110, 'type': 3, 'foreign_id': 63, 'value': 2})

    _edges.append({'id': 111, 'name': 'Éloquent', 'short_desc': 'Vous jouez automatiquement en premier lors d’une intrigue.'})
    _conditions.append({'edge_id': 111, 'type': 2, 'foreign_id': 11, 'value': 4})
    _conditions.append({'edge_id': 111, 'type': 2, 'foreign_id': 13, 'value': 4})

    _edges.append({'id': 112, 'name': 'Fascinant', 'short_desc': 'Obtenez de meilleurs résultats quand vous tentez de Charmer.'})
    _conditions.append({'edge_id': 112, 'type': 4, 'foreign_id': 106})

    _edges.append({'id': 113, 'name': 'Maître négociateur', 'short_desc': 'Votre humeur ne suscite pas de malus.'})
    _conditions.append({'edge_id': 113, 'type': 2, 'foreign_id': 8, 'value': 3})

    _edges.append({'id': 114, 'name': 'Obstiné', 'short_desc': 'Ajoutez votre Dévouement à votre Sang-froid.'})
    _conditions.append({'edge_id': 114, 'type': 2, 'foreign_id': 19, 'value': 3})
    _conditions.append({'edge_id': 114, 'type': 3, 'foreign_id': 67, 'value': 1})

    _edges.append({'id': 115, 'name': 'Perfide', 'short_desc': 'Ajoutez votre rang d’Ingéniosité au résultat des tests de Duperie.'})
    _conditions.append({'edge_id': 115, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 116, 'name': 'Respecté', 'short_desc': 'Vos accomplissements et votre réputation inspirent le respect.'})
    _conditions.append({'edge_id': 116, 'type': 3, 'foreign_id': 69, 'value': 2})

    _edges.append({'id': 117, 'name': 'Séduisant', 'short_desc': 'Relancez les 1 lors des tests de Persuasion.'})
    _conditions.append({'edge_id': 117, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 118, 'name': 'Sociable', 'short_desc': '+2B aux tests de Persuasion contre des personnages issus de pays étrangers à Westeros.'})
    _conditions.append({'edge_id': 118, 'type': 0, 'foreign_id': None})

    """ Flaws """
    _edges.append({'id': 119, 'flaw': True, 'name': 'Arrogant', 'short_desc': 'Vous êtes aveuglé par la haute opinion que vous vous faites de votre statut.'})
    _conditions.append({'edge_id': 119, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 120, 'flaw': True, 'name': 'Banni', 'short_desc': 'Statut réduit de 2.'})
    _conditions.append({'edge_id': 120, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 121, 'flaw': True, 'name': 'Bâtard', 'short_desc': 'Perte du nom de famille, -1D aux tests de Persuasion contre les personnages de Statut supérieur.'})
    _conditions.append({'edge_id': 121, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 122, 'flaw': True, 'name': 'Démence cruelle', 'short_desc': 'Vous n’æppréhendez pas les conséquences de vos actes.'})
    _conditions.append({'edge_id': 122, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 123, 'flaw': True, 'name': 'Dette', 'short_desc': 'Les achats coûtent le double du prix normal.'})
    _conditions.append({'edge_id': 123, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 124, 'flaw': True, 'name': 'Distrait', 'short_desc': 'Relancez tous les 6 lors des tests d’Ingéniosité.'})
    _conditions.append({'edge_id': 124, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 125, 'flaw': True, 'name': 'Ennemi juré', 'short_desc': 'Vous avez un ennemi redoutable.'})
    _conditions.append({'edge_id': 125, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 126, 'flaw': True, 'name': 'Esclave de la bouteille', 'short_desc': 'Addiction malsaine à l’alcool.'})
    _conditions.append({'edge_id': 126, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 127, 'flaw': True, 'name': 'Estropié', 'short_desc': 'Déplacement réduit de 2m.'})
    _conditions.append({'edge_id': 127, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 128, 'flaw': True, 'name': 'Eunuque', 'short_desc': 'On vous a castré.'})
    _conditions.append({'edge_id': 128, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 129, 'flaw': True, 'name': 'Faiblesse', 'short_desc': '-1D à tous les tests effectués avec une compétence particulière.', 'multiple': True})
    _conditions.append({'edge_id': 129, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 130, 'flaw': True, 'name': 'Habitude gênante', 'short_desc': 'Compulsion peu ordinaire.'})
    _conditions.append({'edge_id': 130, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 131, 'flaw': True, 'name': 'Handicap sensoriel', 'short_desc': 'Tous les tests liés au sens manquant sont ratés; -1m en Déplacement.'})
    _conditions.append({'edge_id': 131, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 132, 'flaw': True, 'name': 'Hautain', 'short_desc': 'Votre sens de la décence l’emporte sur votre compassion.'})
    _conditions.append({'edge_id': 132, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 133, 'flaw': True, 'name': 'Honni', 'short_desc': 'Tout le monde vous méprise.'})
    _conditions.append({'edge_id': 133, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 134, 'flaw': True, 'name': 'Honorable', 'short_desc': 'Vous vous sente obligé de dire la vérité.'})
    _conditions.append({'edge_id': 134, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 135, 'flaw': True, 'name': 'Irascible', 'short_desc': 'Votre premier test de Persuasion lors d’une instrigue doit être destiné à Intimider, -2D aux tentatives destinées à Séduire.'})
    _conditions.append({'edge_id': 135, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 136, 'flaw': True, 'name': 'Lâche', 'short_desc': '-1D à tous les tests lors des combats et intruigues.'})
    _conditions.append({'edge_id': 136, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 137, 'flaw': True, 'name': 'Lourdaud', 'short_desc': 'Relancez les 6 lors des tests d’Agilité.'})
    _conditions.append({'edge_id': 137, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 138, 'flaw': True, 'name': 'Lubrique', 'short_desc': 'Votre premier test de Persuasion lors d’une intrigue doit être destiné à Séduire, -2D aux tentatives destinées à Charmer.'})
    _conditions.append({'edge_id': 138, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 139, 'flaw': True, 'name': 'Maladie infantile', 'short_desc': 'Santé réduite de -2.'})
    _conditions.append({'edge_id': 139, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 140, 'flaw': True, 'name': 'Maladif', 'short_desc': '-2D aux tests d’Endurance destinés à résister aux périls naturels et aux maladies.'})
    _conditions.append({'edge_id': 140, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 141, 'flaw': True, 'name': 'Marqué', 'short_desc': 'Relancez les 6 lors des tests de Persuasion.'})
    _conditions.append({'edge_id': 141, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 142, 'flaw': True, 'name': 'Maudit', 'short_desc': 'Risque d’annuler l’effet des Points de Destinée.'})
    _conditions.append({'edge_id': 142, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 143, 'flaw': True, 'name': 'Mauvaise santé', 'short_desc': 'Résultat des tests d’Endurance réduits de 3.'})
    _conditions.append({'edge_id': 143, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 144, 'flaw': True, 'name': 'Menaçant', 'short_desc': 'Vous rendez tout le monde nerveux.'})
    _conditions.append({'edge_id': 144, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 145, 'flaw': True, 'name': 'Muet', 'short_desc': 'Vous êtes incapable de parler.'})
    _conditions.append({'edge_id': 145, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 146, 'flaw': True, 'name': 'Mutilé', 'short_desc': 'Vous avez perdu un membre.'})
    _conditions.append({'edge_id': 146, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 147, 'flaw': True, 'name': 'Naïf', 'short_desc': 'Vous êtes facile à duper.'})
    _conditions.append({'edge_id': 147, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 148, 'flaw': True, 'name': 'Nain', 'short_desc': '-1m en Déplacement, -1D aux tests de Persuasion pour Charmer ou Séduire.'})
    _conditions.append({'edge_id': 148, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 149, 'flaw': True, 'name': 'Perclus', 'short_desc': 'Votre âge avancé vous handicape.'})
    _conditions.append({'edge_id': 149, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 150, 'flaw': True, 'name': 'Phobie', 'short_desc': 'Vous avez peur de quelque-chose'})
    _conditions.append({'edge_id': 150, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 151, 'flaw': True, 'name': 'Pupille', 'short_desc': '-1D aux tests de Persuasion face aux deux familles (parents et tuteurs).'})
    _conditions.append({'edge_id': 151, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 152, 'flaw': True, 'name': 'Tourmenté', 'short_desc': 'Vous êtes hanté par le passé.'})
    _conditions.append({'edge_id': 152, 'type': 0, 'foreign_id': None})

    _edges.append({'id': 153, 'flaw': True, 'name': 'Vil', 'short_desc': '-1D aux tests de Persuasion et de Statut.'})
    _conditions.append({'edge_id': 153, 'type': 0, 'foreign_id': None})

    for edge in _edges:
        the_edge = Edge(**edge)
        dbs.add(the_edge)

    for cond in _conditions:
        the_condition = EdgeCondition(**cond)
        dbs.add(the_condition)

    return dbs.commit()
