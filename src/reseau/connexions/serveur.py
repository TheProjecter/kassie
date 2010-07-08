# -*-coding:Utf-8 -*

"""Ce fichier définit la classe ConnexionServeur détaillée plus bas."""

import sys
import socket
import select

from reseau.connexions.client_connecte import ClientConnecte

class ConnexionServeur:
    """Cette classe représente le socket en écoute sur le port choisit
    dont le rôle est d'ajouter de nouveaux clients et de gérer leurs messages.
    
    Sur une architecture réseau simple, elle n'a besoin d'être instanciée
    qu'une unique fois.
    
    Après son instanciation, on doit appeler dans une boucle la méthode ''
    chargée de vérifier les connexions en attente, d'accepter les clients
    éventuels puis d'interroger chaque client pour savoir si des messages
    sont à récupérer.
    
    """
    
    def __init__(self, port, nb_clients_attente=5, nb_max_connectes=-1, \
            attente_connexion=0.05, attente_reception=0.05):
        """Créée un socket en écoute sur le port spécifié.
        - port : le port surlequel on écoute (>1024)
        - nb_clients_attente : le nombre maximum de clients en attente de
          connexion. Ce nombre est passé à la méthode listen du socket
        - nb_max_connectes : le nombre maximum de clients connectés
          Ce peut être utile pour éviter la surcharge du serveur.
          Si ce nombre est dépassé, on accepte puis déconnecte immédiatement
          le client ajouté. On précise
          -1 si on ne veut aucune limite au nombre de clients
        - attente_connexion : temps pendant lequel on attend de nouvelles
          connexions. C'est en fait le Time Out passé à select.select
          quand il s'agit de surveiller les clients qui souhaitent se
          connecter. Ce temps est précisé en seconde (0.05 s = 50 ms)
          Si on souhaite un Time Out infini mettre cette variable à None.
        - attente_reception : temps indiquant pendant combien de temps
          on attend un message à réceptionner sur les clients déjà connectés.
          Ce nombre est passé comme Time Out de select.select quand il s'agit
          de surveiller les sockets connectés. Ce temps est précisé en seconde
          (0.05 s = 50 ms)
          Si on souhaite un Time Out infini mettre cette variable à None.
        
        Petite précision sur l'utilité de select.select :
            On utilise cette fonction pour surveiller un certain nombre
            de sockets. La fonction s'interrompt à la fin du Time Out spécifié
            ou dès qu'un changement est survenu sur les sockets observés.
        
            Ainsi, si on surveille les clients connectés en attendant
            des messages à réceptionner, dès qu'un client aura envoyé un
            nouveau message, la fonction s'interrompera et nous laissera le
            soin de récupérer les messages des clients retournés.
            Si à l'issue du temps d'attente aucun message n'a été réceptionné,
            la fonction s'interrompt et on peut reprendre la main.
        
        """
        self.port = port # port sur lequel on va écouter
        self.nb_clients_attente = nb_clients_attente
        self.nb_max_connectes = nb_max_connectes
        self.attente_connexion = attente_connexion
        self.attente_reception = attente_reception

        self.clients = {} # un dictionnaire {id_client:client}

        # Socket serveur
        self.socket  = None

    def init(self):
        """Cette méthode doit être appelée après l'appel au constructeur.
        Elle se charge d'initialiser le socket serveur et, en somme,
        de le mettre en écoute sur le port spécifié.
        """
        # Initialisation du socket serveur
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # On paramètre le socket
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # On essaye de se mettre en écoute sur le port précisé
        # Si ça ne marche pas, on affiche l'erreur et on quitte immédiatement
        try:
            self.socket.bind(('', self.port))
        except socket.error as erreur:
            print("Le socket serveur n'a pu être connecté: {0}".format(erreur))
            sys.exit(1)

        # On met en écoute le socket serveur
        self.socket.listen(self.nb_clients_attente)

    def verifier_connexions(self):
        """Cette méthode vérifie si des clients ne sont pas en attente
        de connexion. Elle a un comportement bloquant pendant le temps
        attente_connexion spécifié dans le constructeur de l'objet.
        Elle se charge d'ajouter les clients connectés à la liste
        des clients si le nombre maximum de connecté n'est pas excédé.
        Dans le cas contraire, on envoie au client un message par défaut
        et on le déconnecte du serveur.
        """
        # On attend avec select.select qu'une connexion se présente
        # Si aucune connexion ne se présente, au bout du temps indiqué
        # dans self.attente_connexion, select.select s'arrête
        # en levant une exception select.error
        try:
            connexions, none, none = select.select(
                [self.socket], [], [], self.attente_connexion)
        except select.error:
            pass

        # On parcourt la boucle des connexions en attente
        # En toute logique, elle ne possède qu'un client puisque select.select
        # s'interrompt dès qu'elle reçoit une demande de connexion
        for connexion in connexions:
            # On tente d'accepter la connexion
            try:
                socket, infos = connexion.accept()
            except socket.error:
                pass
            else:
                # On vérifie qu'on peut ajouter un nouveau client
                if self.nb_max_connectes>=0 \
                        and len(self.clients) >= self.nb_max_connectes:
                    # On refuse la connexion
                    socket.send("Ce serveur ne peut accueillir de connexions " \
                        "supplementaires.".encode())
                    socket.close()
                else:
                    # On créée notre client avec les infos dont on dispose
                    client = ClientConnecte(socket, infos)
                    # On l'ajoute dans le dictionnaire des clients
                    self.clients[client.id] = client
                    print("Connexion du client {0}.".format(client))
