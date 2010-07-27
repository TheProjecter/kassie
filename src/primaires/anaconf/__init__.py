# -*-coding:Utf-8 -*

"""Ce fichier contient la classe Anaconf, définissant le module primaire
du même nom.

"""

from abstraits.module import *
from primaires.anaconf.analyseur import Analyseur

class Anaconf(Module):
    """Classe du module 'anaconf'.
    
    Ce module gère la lecture, l'écriture et l'interprétation de fichiers de
    configuration.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        Module.__init__(self, importeur, "anaconf", "primaire")

    def charger_config(self, nom_fichier, defauts):
        """Cette méthode permet de charger une configuration contenue dans
        le fichier passé en paramètre. Le paramètre defauts est un
        dictionnaire contenant les données par défaut.
        Si certaines données ne sont pas trouvées, on les met à jour grâce
        à ce dictionnaire.
        
        """
        return Analyseur(nom_fichier, defauts)

