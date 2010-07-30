# -*-coding:Utf-8 -*

"""Ce fichier contient la classe Log, définissant le module primaire
du même nom.

"""

import os
import time

from abstraits.module import *
from primaires.log.logger import *

# Dossier d'enregistrement des fichiers de log
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
rep_logs = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "logs"

class Log(Module):
    """Classe du module 'log'.
    
    Ce module permet d'enregistrer et gérer les fichiers de log.
    
    Chaque module primaire ou secondaire ayant besoin de logger des
    informations (c'est-à-dire la majorité sinon la totalité)
    devra passer par ce module.
    
    On conserve une trace des loggers créés.

    NOTE IMPORTANTE: ce module ne pourra pas travailler avant d'être
    initialisé. Si des messages de log doivent être envoyés avant
    l'initialisation, ils seront mis dans une fil d'attente et enregistrés
    lors de l'initialisation.
    
    Voir primaires/log/logger.py
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "log", "primaire")
        self.loggers = {} # {nom_logger:logger}

    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers de log a été défini.
        
        """
        global rep_logs
        if "chemin-logs" in self.parser_cmd.keys():
            rep_logs = self.parser_cmd["chemin-logs"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(rep_logs):
            os.makedirs(rep_logs)
        
        # On met à jour le rep_base de chaque logger
        for logger in self.loggers.values():
            logger.rep_base = rep_logs
            logger.verif_rep()

        Module.config(self)

    def init(self):
        """Redéfinition de l'initialisation.
        On va passer le statut de tous les loggers pour qu'ils puissent
        écrire en temps réel leur message. On va aussi leur demander
        d'enregistrer toute leur fil d'attente.
        
        """
        for logger in self.loggers.values():
            logger.en_fil = False
            logger.verif_rep()
            logger.enregistrer_fil_attente()
        
        Module.init(self)

    def creer_logger(self, sous_rep, nom_logger, nom_fichier=""):
        """Retourne un nouveau logger.
        Si le nom de fichier n'est pas spécifié, on s'appuie sur le nom
        du logger .log.
        On se base dans tous les cas sur rep_base lié au sous_rep pour
        créer l'architecture d'enregistrement des logs.

        """
        global rep_logs
        if nom_fichier=="":
            nom_fichier = "{0}.log".format(nom_logger)

        logger = Logger(rep_logs, sous_rep, nom_fichier, nom_logger)
        if self.statut == INITIALISE:
            logger.en_fil = False
            logger.verif_rep()
        self.loggers[nom_logger] = logger
        return logger
