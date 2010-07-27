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

from abstraits.module import *

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

    def tout_charger(self):
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

    def tout_instancier(self):
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

    def tout_configurer(self):
        """Méthode permettant de configurer tous les modules qui en ont besoin.
        Les modules qui doivent être configuré sont ceux instanciés.
        
        Attention: les modules non encore instanciés sont à l'état de classe.
        Tous les modules doivent donc être instanciés au minimum avant
        que cette méthode ne soit appelée. Autrement dit, la méthode
        tout_instancier doit être appelée auparavant.
        
        """
        for module in self.__dict__.values():
            if module.statut == INSTANCIE:
                module.config()

    def tout_initialiser(self):
        """Méthode permettant d'initialiser tous les modules qui en ont besoin.
        Les modules à initialiser sont ceux configuré.
        
        """
        for module in self.__dict__.values():
            if module.statut == CONFIGURE:
                module.init()

    def tout_detruire(self):
        """Méthode permettant de détruire tous les modules qui en ont besoin.
        Les modules à détruire sont ceux initialisés.
        
        """
        for module in self.__dict__.values():
            if module.statut == INITIALISE:
                module.detruire()

    def module_est_charge(self, nom):
        """Retourne True si le module est déjà chargé, False sinon.
        On n'a pas besoin du type du module, les modules primaires
        et secondaires étant stockés de la même façon.

        Attention: un module peut être chargé sans être instancié,
        configuré ou initialisé.
        
        """
        return nom in self.__dict__.keys()

    def charger_module(self, type, nom):
        """Méthode permettant de charger un module en fonction de son type et de
        son nom.
        
        Si le module est déjà chargé, on ne fait rien.

        Note: à la différence de tout_charger, cette méthode créée directement
        l'objet gérant le module.
        
        """
        if type == "primaire":
            rep = rep_primaires
        elif type == "secondaire":
            rep = rep_secondaires
        else:
            raise ValueError("le type {0} n'est ni primaire ni secondaire" \
                    .format(type))

        if self.module_est_charge(nom):
            print("Le module {0} est déjà chargé.".format(nom))
        else:
            package = __import__(rep + "." + nom)
            module = getattr(getattr(package, nom), \
                    nom.capitalize())
            setattr(self, nom, module(self))

    def decharger_module(self, type, nom):
        """Méthode permettant de décharger un module.
        
        Elle se charge :
        -   d'appeler la méthode detruire du module
        -   de supprimer le module des modules dans sys.modules
        -   de supprimer l'instance du module dans self

        """
        if type == "primaire":
            rep = rep_primaires
        elif type == "secondaire":
            rep = rep_secondaires
        else:
            raise ValueError("le type {0} n'est ni primaire ni secondaire" \
                    .format(type))

        nom_complet = rep + "." + nom
        if nom_complet in sys.modules.keys():
            del sys.modules[nom_complet]
        else:
            print("{0} n'est pas dans sys.modules".format(nom_complet))

        if self.module_est_charge(nom):
            getattr(self, nom).detuire()
            delattr(self, nom)
        else:
            print("{0} n'est pas dans les attributs de l'importeur".format(nom))

    def recharger_module(self, type, nom):
        """Cette méthode permet de recharger un module. Elle passe par :
        -   decharger_module
        -   charger_module
        
        """
        self.decharger_module(type, nom)
        self.charger_module(type, nom)

    def config_module(self, nom):
        """Méthode chargée de configurer ou reconfigurer un module."""
        if self.module_est_charge(nom):
            getattr(self, nom).config()
        else:
            print("{0} n'existe pas ou n'est pas chargé.".format(nom))

    def init_module(self, nom):
        """Méthode chargée d'initialiser un module."""
        if self.module_est_charge(nom) and getattr(self, nom).statut == \
                CONFIGURE:
            getattr(self, nom).init()
        else:
            print("{0} n'existe pas ou n'est pas configuré.".format(nom))

