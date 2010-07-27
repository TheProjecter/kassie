# -*-coding:Utf-8 -*

"""Ce fichier contient la classe Anaconf, définissant le module primaire
du même nom.

"""

from abstraits.module import *

class Anaconf(Module):
    """Classe du module 'anaconf'.
    
    Ce module gère la lecture,
    l'écriture et l'interprétation de fichiers de configuration.
    
    Chaque module primaire ou secondaire ayant besoin d'enregistrer des
    informations de configuration devra passer par anaconf.
    
    """
    def __init__(self, importeur):
        """Constructeur du module"""
        Module.__init__(self, importeur, "anaconf", "primaire")
