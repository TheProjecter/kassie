# -*-coding:Utf-8 -*

"""Ce package contient l'ensemble des modules secondaires du projet.

Chaque module secondaire se trouve dans un sous-package.

Les modules secondaires n'ayant aucune relation d'inter-dépendance entre eux,
aucun ordre d'instanciation n'est défini. On peut les charger dans le désordre,
ou même ne pas en charger certains.

Règles d'inter-dépendance :
-  les modules secondaires peuvent appeler des modules primaires
-  les modules secondaires ne peuvent s'appeler entre eux

Pour obtenir de l'aide sur un module en particulier, consulter le fichier
__init__.py du package concerné.

"""
