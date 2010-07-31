# -*-coding:Utf-8 -*

"""Ce package contient l'ensemble des modules primaires du projet.

Chaque module primaire possède son propre package.

Les modules primaires ayant des relations d'inter-dépendance entre eux, un
ordre d'instanciation est défini dans ce fichier. Tout ce qui n'est pas dans
l'ordre d'instanciation sera instancié par la suite, après les modules définis.

Règles d'interdépendance :
- un module primaire peut faire appel aux autres modules primaires
- un module primaire ne peut faire appel à un module secondaire, sauf
  si il utilise des méthodes génériques aux modules servant à modifier
  son état, ou à l'interprétation de commandes

Pour obtenir une aide sur chaque module primaire, consulter le fichier
__init__.py du package concerné.

NOTE: les modules primaires et secondaires ne doivent pas porter de noms
identiques.

"""
