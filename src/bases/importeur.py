# -*-coding:Utf-8 -*

"""Ce fichier définit un objet 'importeur', chargé de contrôler le mécanisme
d'importation, initialisation, configuration, déroulement et arrêt
des modules primaires et secondaires.

On parcourt les sous-dossiers définis dans les variables :
- rep_primaires : répertoire des modules primaires
- rep_secondaires : répertoire des modules secondaires

Il est possible de changer ces variables mais dans ce cas, une réorganisation
du projet s'impose.

Dans chaque module, on s'occupera de charger l'objet le représentant.
Par exemple, le module anaconf se définit comme suit :
*   un package anaconf contenu dans rep_primaires
    *   un fichier __init__.py
        *   une classe Anaconf

On créée un objet chargé de représenter le module. C'est cet objet qui possède
les méthodes génériques chargées d'initialiser, configurer, lancer et arrêter
un module. Les autres fichiers du module sont une boîte noir inconnu pour
l'importeur.

"""

import os
import sys

rep_primaires = "primaires"
rep_secondaires = "secondaires"

class Importeur:
    """Classe chargée de créer un objet Importeur. Il contient sous la forme
    d'attributs les modules primaires et secondaires chargés. Les modules
    primaires et secondaires ne sont pas distingués.
    
    On ne doit créer qu'un seul objet Importeur.

    """
    nb_importeurs = 0

    def __init__(self):
        """Constructeur de l'importeur. Il vérifie surtout
        qu'un seul est créé.
        
        """
        Importeur.nb_importeurs += 1
        if Importeur.nb_importeurs>1:
            raise RuntimeError("{0} importeurs ont été créés".format( \
                Importeur.nb_importeurs))

    def __str__(self):
        """Retourne sous ue forme un peu plus lisible les modules importés."""
        ret = []
        for nom_module in self.__dict__.keys():
            ret.append("{0}: {1}".format(nom_module, getattr(self, \
                    nom_module)))
        ret.sort()
        return "\n".join(ret)

    def charger(self):
        """Méthode appelée pour charger les modules primaires et secondaires.
        Par défaut, on importe tout mais on ne créée rien.

        """
        # On commence par parcourir les modules primaires
        for nom_package in os.listdir(os.getcwd() + "/" + rep_primaires):
            if not nom_package.startswith("__"):
                package = __import__(rep_primaires + "." + nom_package)
                module = getattr(getattr(package, nom_package), \
                        nom_package.capitalize())
                setattr(self, nom_package, module)
        # On fait de même avec les modules secondaires
        for nom_package in os.listdir(os.getcwd() + "/" + rep_secondaires):
            if not nom_package.startswith("__"):
                package = __import__(rep_secondaires + "." + nom_package)
                module = getattr(getattr(package, nom_package), \
                        nom_package.capitalize())
                setattr(self, nom_package, module)

    def instancier(self):
        """Cette méthode permet d'instancier les modules chargés auparavant.
        On se base sur le type du module (classe ou objet)
        pour le créer ou non.
        
        En effet, cette méthode doit pouvoir être appelée quand certains
        modules sont instanciés, et d'autres non.

        NOTE IMPORTANTE: on passe au constructeur de chaque module
        self, c'est-à-dire l'importeur. Les modules en ont en effet
        besoin pour interragir entre eux.

        """
        for nom_module,module in self.__dict__.items():
            if type(module) is type: # on doit l'instancier
                setattr(self, nom_module, module(self))
