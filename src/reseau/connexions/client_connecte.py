# -*-coding:Utf-8 -*

"""Ce fichier définit la classe ClientConnecte, détaillée plus bas."""

import socket

class ClientConnecte:
    """Cette classe est une classe envelope d'un socket.
    Elle reprend les méthodes utiles à la manipulation des sockets et possède
    quelques attributs et méthodes implémentées pour faciliter son insertion dans
    un serveur TCP.
    
    Cette classe est appelée pour héberger un client connecté, c'est-à-dire
    dont la demande de connexion a été validée par le serveur.
    
    On définit pour chaque connexion instanciée un numéro d'identification
    nommé 'id'. L'id courant sera contenu comme variable statique de cette classe.

    """
    id_courant = 0

    def __init__(self, socket_connecte, infos):
        """"Constructeur standard.
        
        On donne à la connexion créée une ID qui lui sera propre.
        Les paramètres à entrer sont :
        - le socket retourné par la méthode accept()
        - les infos de connexion, un tuple contenant :
            - l'adresse IP du client
            - le port sortant du client
        """
        self.id = Connexion.id_courant
        Connexion.id_courant += 1

        # Notre socket connecté
        self.socket = socket_connecte

        # Informations de connexion
        self.adresse_ip = infos[0]
        self.port = infos[1] # le port sortant du client pour se connecter
        
        # Statut de connexion
        self.connecte = True
        
        # Message en cours (il contient la chaîne que le client
        # est en train d'écrire, dans le cas d'un client qui envoie
        # au fur et à mesure les caractères entrés)
        self.message = ""
    
   def deconnecte(self, message):
        self.connecte = False
        print("Déconnexion du client {0}: {1}.".format(self.id, message))
