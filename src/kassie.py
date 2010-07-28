# -*-coding:Utf-8 -*

"""Ce fichier contient le code principal du projet.

Vous pouvez le renommer en fonction du nom choisi de votre projet.

"""

from reseau.connexions.serveur import *
from reseau.fonctions.callbacks import *
from bases.importeur import Importeur
from bases.parser_cmd import ParserCMD

# Changez ici le port par défaut
# Le port par défaut peut être modifié par des options de la ligne
# de commande, mais vous pouvez aussi le changer ici sans avoir besoin
# de le spécifier à chaque lancement du programme.
# Utiliser un port différent précisé dans la ligne de commande a surtout
# été mis en place pour créer de multiples essions de test du MUD
port = 4000

# On créée un analyseur de la ligne de commande
parser_cmd = ParserCMD()
parser_cmd.interpreter()

# Si le port est spécifié dans la ligne de commande, on le change
if "port" in parser_cmd.keys():
    port = parser_cmd["port"]

# On créée l'importeur et on lance le processus d'instanciation des modules.
importeur = Importeur()
importeur.tout_charger()
importeur.tout_instancier(parser_cmd)
importeur.tout_configurer()
importeur.tout_initialiser()

# On se créée un logger
log = importeur.log.creer_logger("", "sup", "kassie.log")

# Vous pouvez changer les paramètres du serveur, telles que spécifiées dans le
# constructeur de ServeurConnexion (voir reseau/connexions/serveur.py)
# Par défaut, on précise simplement son port d'écoute.

serveur = ConnexionServeur(port)
serveur.init() # Initialisation, le socket serveur se met en écoute
log.info("Le serveur est à présent en écoute sur le port {0}".format(port))

# Configuration des fonctions de callback
# Note: si vous souhaitez modifier le comportement en cas de connexion
# au serveur, déconnexion ou réception d'un message client,
# modifiez directement les fonctions de callback dans :
# reseau/fonctions/callbacks.py

# Fonction de callback appelée lors de la connexion d'un client
serveur.callbacks["connexion"].fonction = cb_connexion
serveur.callbacks["connexion"].parametres = (serveur, log)

# Fonction de callback appelée lors de la déconnexion d'un client
serveur.callbacks["deconnexion"].fonction = cb_deconnexion
serveur.callbacks["deconnexion"].parametres = (serveur, log)

# Fonction de callback appelée lors de la réception d'un message d'un client
serveur.callbacks["reception"].fonction = cb_reception
serveur.callbacks["reception"].parametres = (serveur, log)

# Lancement de la boucle synchro
# Note: tout se déroule ici, dans une boucle temps réelle qui se répète
# jusqu'à l'arrêt du MUD. De cette manière, on garde le contrôle total
# sur le flux d'instructions.

while True:
    serveur.verifier_connexions()
    serveur.verifier_receptions()
