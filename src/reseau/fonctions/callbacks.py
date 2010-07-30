# -*-coding:Utf-8 -*

"""Ce fichier définit les fonctions de callback, appelées dans le cadre
d'évènements serveur (connexion d'un client, déconnexion, réception
d'un message...)

Elles prennent toutes le préfixe cb_ (callback)

"""

fin_ligne = "\r\n"

def cb_connexion(serveur, importeur, logger, client):
    """Que se passe-t-il quand client se connecte ?"""
    logger.info("Connexion du client {0}".format(client))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("$$ {0} se connecte au serveur{1}".format( \
                    client, fin_ligne).encode())

def cb_deconnexion(serveur, importeur, logger, client):
    """Que se passe-t-il quand client se déconnecte ?"""
    logger.info("Déconnexion du client {0} : {1}".format(client, client.retour))
    for c in serveur.clients.values():
        if c is not client:
            c.envoyer("** {0} se déconnecte du serveur{1}".format( \
                    client, fin_ligne).encode())

def cb_reception(serveur, importeur, logger, client):
    """Que se passe-t-il quand client envoie un message au serveur ?"""
    msg = client.get_message_decode()
    #print("J'ai réceptionné {0}".format(msg))
    for c in serveur.clients.values():
        c.envoyer("<{0}> {1}{2}".format(client.id, msg, fin_ligne).encode())

