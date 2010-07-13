# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du projet.

Vous pouvez le renommer en fonction du nom choisi de votre projet.

"""

from reseau.connexions.serveur import *
from reseau.fonctions.callbacks import *

# Changez ici le port par défaut
# Le port par défaut peut être modifié par des options de la ligne
# de commande, mais vous pouvez aussi le changer ici sans avoir besoin
# de le spécifier à chaque lancement du programme.
# Utiliser un port différent précisé dans la ligne de commande a surtout
# été mis en place pour créer de multiples essions de test du MUD
port = 4000

# Vous pouvez changer les paramètres du serveur, telles que spécifiées dans le
# constructeur de ServeurConnexion (voir reseau/connexions/serveur.py)
# Par défaut, on précise simplement son port d'écoute.

serveur = ConnexionServeur(port)
serveur.init() # Initialisation, le socket serveur se met en écoute

# Configuration des fonctions de callback
# Note: si vous souhaitez modifier le comportement en cas de connexion
# au serveur, déconnexion ou réception d'un message client,
# modifiez directement les fonctions de callback dans :
# reseau/fonctions/callbacks.py

# Fonction de callback appelée lors de la connexion d'un client
serveur.callbacks["connexion"].fonction = cb_connexion
serveur.callbacks["connexion"].parametres = (serveur, )

# Fonction de callback appelée lors de la déconnexion d'un client
serveur.callbacks["deconnexion"].fonction = cb_deconnexion
serveur.callbacks["deconnexion"].parametres = (serveur, )

# Fonction de callback appelée lors de la réception d'un message d'un client
serveur.callbacks["reception"].fonction = cb_reception
serveur.callbacks["reception"].parametres = (serveur, )

# Lancement de la boucle synchro
# Note: tout se déroule ici, dans une boucle temps réelle qui se répète
# jusqu'à l'arrêt du MUD. De cette manière, on garde le contrôle total
# sur le flux d'instructions.

while True:
    serveur.verifier_connexions()
    serveur.verifier_receptions()
