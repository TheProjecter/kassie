# -*-coding:Utf-8 -*

"""Ce package définit différentes connexions, clients et serveur.

Selon l'architecture réseau usuelle nous avons :
-   un socket (connexion serveur) écoutant sur un port précis, en attente
    de connexion
-   De multiples sockets (clients connectés) qui représentent les clients
    connectés au serveur

C'est au serveur de gérer la connexion de chaque client, ainsi que la
réception des messages.

"""
