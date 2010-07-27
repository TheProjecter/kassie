# -*-coding:Utf-8 -*

"""Ce fichier contient la classe Anaconf, définissant le module primaire
du même nom.

"""

import os

from abstraits.module import *
from primaires.anaconf.analyseur import Analyseur

# Dossier d'enregistrement des fichiers de configuration
# Vous pouvez changer cette variable, ou bien spécifier l'option en
# ligne de commande
rep_config = os.path.expanduser("~") + os.sep + "kassie" + os.sep + "config"

class Anaconf(Module):
    """Classe du module 'anaconf'.
    
    Ce module gère la lecture, l'écriture et l'interprétation de fichiers de
    configuration.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    
    """
    def __init__(self, importeur, parser_cmd):
        """Constructeur du module"""
        Module.__init__(self, importeur, parser_cmd, "anaconf", "primaire")

    def config(self):
        """Méthode de configuration. On se base sur
        parser_cmd pour savoir si un dossier d'enregistrement
        des fichiers de configuration a été défini.
        
        """
        global rep_config
        if "chemin-configuration" in self.parser_cmd.keys():
            rep_config = self.parser_cmd["chemin-configuration"]
        
        # On construit le répertoire si il n'existe pas
        if not os.path.exists(rep_config):
            os.makedirs(rep_config)


    def charger_config(self, chemin, defauts):
        """Cette méthode permet de charger une configuration contenue dans
        le fichier passé en paramètre. Le paramètre defauts est un
        dictionnaire contenant les données par défaut.
        Si certaines données ne sont pas trouvées, on les met à jour grâce
        à ce dictionnaire.
        
        """
        global rep_config
        chemin = rep_config + os.sep + chemin
        # On construit le répertoire si il n'existe pas
        rep = os.path.split(chemin)[0]
        if not os.path.exists(rep):
            os.makedirs(rep)
        return Analyseur(chemin, defauts)

