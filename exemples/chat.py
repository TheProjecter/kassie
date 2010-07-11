# -*-coding:Utf-8 -*

"""Cet exemple met en place un système de chat minimaliste gérant :
- les connexions multiples
- les déconnexions fortuites
- la réception ou l'envoie de messages aux clients

On utilise les fonctions de callback pour paramétrer comment doit
réagir le serveur lors d'une connexion, d'une déconnexion ou d'une
réception d'un message. Consultez le code pour plus d'informations.

"""

from reseau.connexions.serveur import *

fin_ligne = "\r\n"

# Fonctions de callback

def connexion(serveur, client):
    """Que se passe-t-il quand client se connecte ?"""
    print("Connexion du client {0}".format(client))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("$$ {0} se connecte au serveur{1}".format( \
                    client, fin_ligne).encode())

def deconnexion(serveur, client):
    """Que se passe-t-il quand client se déconnecte ?"""
    print("Déconnexion du client {0} : {1}".format(client, client.retour))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("** {0} se déconnecte du serveur{1}".format( \
                    client, fin_ligne).encode())

def reception(serveur, client):
    """Que se passe-t-il quand client envoie un message au serveur ?"""
    msg = client.get_message() # msg contient un type bytes, aps str
    print("J'ai réceptionné en bytes {0}".format(msg))
    for c in serveur.clients.values():
        c.envoyer("<{0}> {1}{2}".format(client.id, msg, fin_ligne).encode())


# Création et paramétrage du serveur

serveur = ConnexionServeur(4000) # test sur le port 4000

# Paramétrage des callbacks
# callback lors de la connexion
serveur.callbacks["connexion"].fonction = connexion
serveur.callbacks["connexion"].parametres = (serveur,)

# callback lors de la déconnexion
serveur.callbacks["deconnexion"].fonction = deconnexion
serveur.callbacks["deconnexion"].parametres = (serveur,)

# callback lors de la réception de message
serveur.callbacks["reception"].fonction = reception
serveur.callbacks["reception"].parametres = (serveur,)

# Fin du paramétrage du serveur

serveur.init() # initialisation, indispensable
while True: # le serveur ne s'arrête pas naturellement
    serveur.verifier_connexions()
    serveur.verifier_receptions()
