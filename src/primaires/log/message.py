# -*-coding:Utf-8 -*

"""Ce fichier contient la classe Message, définie plus bas."""

class Message:
    """Cette classe représente un message de log stockée par la fil
    d'attente du Logger.
    
    """
    def __init__(self, niveau, message, formate):
        """Un message de log contient :
        -   un niveau d'erreur (int)
        -   un message informatif (str)
        -   le message formaté
        
        On conserve le message formaté afin de garder la date réelle de
        l'enregistrement du message. Le message est enregistré après coup,
        mais la date est celle de l'ajout dans la fil, non celle de
        l'enregistrement.
        
        """
        self.niveau = niveau
        self.message = message
        self.message_formate = formate
    
