# -*-coding:Utf-8 -*

"""Ce fichier définit la classe Logger, détaillée plus bas."""

import os
import time

from primaires.log.message import Message

# Constantes prédéfinies
# Niveaux d'erreur
DBG = DEBUG = 0
INFO = 1
WARN = WARNING = 2
FATAL = ERROR = EXCEPTION = 3

# Dictionnaire des niveaux
niveaux = {
    INFO: "info",
    WARNING: "warning",
    DEBUG: "debug",
    FATAL: "fatal",
}

# Format (voir méthode formater de la classe Logger)
FORMAT = "%date% %heurems% [%niveau%] : %message%"

class Logger:
    """Cette classe représente des loggers.
    Ce sont des objets permettant d'enregistrer différentes informations.
    Une instance d'un logger est créée à chaque fois qu'on souhaite obtenir
    une information indépendante des autres. Par exemple, chaque module
    primaire ou secondaire doit posséder son propre logger. Le corps
    également.
    
    Chaque logger possède :
    -   un fichier de log qui peut être à None
    -   un flag concernant l'affichage des messages dans la console
    -   un format d'enregistrement des messages
    -   un niveau minimum pour afficher le message. A noter que tous les
        messages sont enregistrés dans le fichier. Mais on peut par exemple
        demander que seuls les informations critiques soient affichées
        dans la console
    -   un dictionnaire de redirection permettant de spécifier que
        tel niveau d'erreur doit être enregistré et envoyé ver sun autre
        logger
    
    NOTE IMPORTANTE: le logger doit s'abstenir de logger des messages
    pendant un certain lapse de temps. Les messages à logger sont alors
    stockées dans une fil d'attente et enregistrées après coup.
    C'est le module 'log' lui-même qui change l'information d'état
    et autorise le logger à écrire en temps réel ses messages.

    """
    def __init__(self, rep_base, sous_rep, nom_fichier, nom_logger, \
            console=True, format=FORMAT, niveau_min=INFO, redirection={}):
        """Constructeur du loger. Seuls les quatre premiers paramètres
        sont obligatoires :
        -   le répertoire de base (probablement constant d'un logger à l'autre)
        -   le sous-répertoire
        -   le nom du fichier de log
            Ces trois informations peuvent contenir des chaînes vides
            si l'on ne souhaite pas enregistrer dans un fichier (déconseillé).
        -   le nom du logger
        -   console (True pour afficher dans la console, False sinon)
        -   le format du message de log enregistré (voir méthode formater)
        -   le niveau minimum pour afficher un message
        -   le dictionnaire de redirection (voir plus haut)
        
        """
        self.nom = nom_logger
        self.en_fil = True # par défaut, on stock en fil d'attente
        self.fil_attente = [] # liste des messages en attente d'être écrits
        self.rep_base = rep_base
        self.sous_rep = sous_rep
        self.nom_fichier = nom_fichier
        self.fichier = None # on essayera de l'ouvrir au moment du logging
        self.console = console
        self.format = format
        self.niveau_min = niveau_min
        self.redirection = redirection

    def _get_rep_complet(self):
        """Cette méthode retourne le répertoire complet rep_base et sous_rep.
        Si sous_rep est vide on s'assure que le chemin reste cohérent.
        
        """
        rep_base = self.rep_base
        sous_rep = self.sous_rep
        if sous_rep == "":
            rep_complet = rep_base
        else:
            rep_complet = rep_base + os.sep + sous_rep

        return rep_complet

    rep_complet = property(_get_rep_complet)

    def verif_rep(self):
        """Cette méthode vérifie si le répertoire de log existe.
        Si ce n'est pas le cas, on le créée.

        """
        rep = self.rep_complet
        if not os.path.exists(rep):
            os.makedirs(rep)

    def ouvrir_fichier(self):
        """Méthode chargée d'ouvrir le fichier configuré."""
        rep = self.rep_complet
        nom_fichier = rep + os.sep + self.nom_fichier
        try:
            # On tente d'ouvrir le fichier
            self.fichier = open(nom_fichier, "a")
        except IOError:
            print("Impossible d'ouvrir le fichier de log {0}".format( \
                    nom_fichier))
            self.fichier = None

    def fermer_fichier(self):
        """Méthode chargée de fermer le fichier de log."""
        if self.fichier is not None:
            self.fichier.close()
            self.fichier = None

    def formater(self, niveau, message):
        """Méthode retournant la chaîne formattée.
        
        Si des formats spécifiques sont ajoutés, les définir ici.
        On définit un format spécifique comme une partie de chaîne entourée
        de deux signes %.
        Par exemple, %date% sera remplacé par la date actuel dans le message.

        """
        sdate = time.struct_time(time.localtime())
        ms = "{0:f}".format(time.time()).split(".")[1][:3]
        date = "{0}-{1:02}-{2:02}".format(sdate.tm_year, sdate.tm_mon, \
                sdate.tm_mday)
        heure = "{0:02}:{1:02}:{2:02}".format(sdate.tm_hour, \
                sdate.tm_min, sdate.tm_sec)
        heurems = "{0:02}:{1:02}:{2:02},{3}".format(sdate.tm_hour, \
                sdate.tm_min, sdate.tm_sec, ms)
        chaine = self.format
        chaine = chaine.replace("%date%", date)
        chaine = chaine.replace("%heure%", heure)
        chaine = chaine.replace("%heurems%", heurems)
        chaine = chaine.replace("%niveau%", niveau)
        chaine = chaine.replace("%message%", message)
        return chaine

    def doit_afficher(self, niveau):
        """Retourne True si le logger doit afficher le message de ce
        niveau, False sinon.
        
        """
        return (self.console is True and self.niveau_min<=niveau) \
                or self.fichier is None

    def log(self, niveau, message):
        """Méthode permettant de logger un message.
        Les méthodes info, debug, warning et fatal redirigent dessus.
        
        """
        s_niveau = niveaux[niveau]
        f_message = self.formater(s_niveau, message)
        if self.en_fil:
            self.fil_attente.append(Message(s_niveau, message, f_message))
            if self.doit_afficher(niveau):
                print(message)
        else:
            self.ouvrir_fichier()
            if self.fichier is not None:
                # On essaye d'écrire dans le fichier
                try:
                    self.fichier.write(f_message + "\n")
                except IOError:
                    pass
            self.fermer_fichier()
        
            if self.doit_afficher(niveau):
                print(message)

    def enregistrer_fil_attente(self):
        """Cette méthode ne doit être appelée qu'une fois.
        Elle permet d'enregistrer la fil d'attente du logger.
        Cette fil d'attente s'est remplie pendant que le module 'log' se
        configurait. Dès son initialisation, le module demande à cette méthode
        que la fil d'attente de chaque logger créé soit enregistrée.
        
        """
        for message in self.fil_attente:
            self.ouvrir_fichier()
            if self.fichier is not None:
                # On essaye d'écrire dans le fichier
                try:
                    self.fichier.write(message.message_formate + "\n")
                except IOError:
                    pass
            self.fermer_fichier()

    def debug(self, message):
        """Méthode permettant de logger un niveau de message DEBUG"""
        self.log(DEBUG, message)

    def info(self, message):
        """Méthode permettant de logger un niveau de message INFO"""
        self.log(INFO, message)

    def warning(self, message):
        """Méthode permettant de logger un niveau de message WARNING"""
        self.log(WARNING, message)

    def fatal(self, message):
        """Méthode permettant de logger un niveau de message FATAL"""
        self.log(FATAL, message)

