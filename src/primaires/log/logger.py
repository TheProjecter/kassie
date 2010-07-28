# -*-coding:Utf-8 -*

"""Ce fichier définit la classe Logger, détaillée plus bas."""

import os
import time

# Constantes prédéfinies
# Niveaux d'erreur
INFO = 0
DBG = DEBUG = 1
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

    """
    def __init__(self, rep_base, nom_fichier, nom_logger, console=True, \
            format=FORMAT, niveau_min=INFO, redirection={}):
        """Constructeur du loger. Seuls les trois premiers paramètres
        sont obligatoires :
        -   le répertoire d'accueil des logs
        -   le nom du fichier de log
            Ces deux informations peuvent contenir des chaînes vides
            si l'on ne souhaite pas enregistrer dans un fichier (déconseillé).
        -   le nom du logger
        -   console (True pour afficher dans la console, False sinon)
        -   le format du message de log enregistré (voir méthode formater)
        -   le niveau minimum pour afficher un message
        -   le dictionnaire de redirection (voir plus haut)
        
        """
        self.nom = nom_logger
        self.rep_base = rep_base
        self.nom_fichier = nom_fichier
        self.fichier = None # on essayera de l'ouvrir au moment du logging
        # On vérifie que le répertoire de base existe
        if not os.path.exists(self.rep_base):
            os.makedirs(self.rep_base)
        self.console = console
        self.format = format
        self.niveau_min = niveau_min
        self.redirection = redirection

    def ouvrir_fichier(self):
        """Méthode chargée d'ouvrir le fichier configuré."""
        if self.rep_base!="" and self.nom_fichier!="":
            rep_base = self.rep_base
            nom_fichier = self.nom_fichier
            # On tente d'ouvrir le fichier
            self.fichier = open(rep_base + os.sep + nom_fichier, "a")
        else:
            self.fichier = None

    def fermer_fichier(self):
        """Méthode chargée de fermer le fichier de log."""
        if self.fichier is not None:
            self.fichier.close()

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
        niveau = niveaux[niveau]
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
        f_message = self.formater(niveau, message)
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

    def info(self, message):
        """Méthode permettant de logger un niveau de message INFO"""
        self.log(INFO, message)

    def debug(self, message):
        """Méthode permettant de logger un niveau de message DEBUG"""
        self.log(DEBUG, message)

    def warning(self, message):
        """Méthode permettant de logger un niveau de message WARNING"""
        self.log(WARNING, message)

    def fatal(self, message):
        """Méthode permettant de logger un niveau de message FATAL"""
        self.log(FATAL, message)

