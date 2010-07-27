# -*-coding:Utf-8 -*

"""Ce fichier définit la classe Module, détaillée plus bas."""

# Statuts
INSTANCIE = 0

# Dictionnaire permettant de faire correspondre un statut à une chaîne
statuts = {
    INSTANCIE:"instancié",
}

class Module:
    """Cette classe est une classe abstraite définissant un module, primaire
    ou secondaire.
    
    Chacun des modules primaires ou secondaires devra hériter de cette classe.
    Elle reprend les trois méthodes d'un module, appelée dans l'ordre :
    -   config : configuration du module
    -   init : initialisation du module (ne pas confondre avec le constructeur)
    -   destroy : destruction du module, appelée lors du déchargement
    
    L'initialisation est la phase la plus importante. Elle se charge,
    en fonction de la configuration définie et instanciée dans config,
    de "lancer" un module. Si des actions différées doivent être mises en
    place pendant l'appel au module, elles doivent être créées dans cette
    méthode.

    La méthode destroy doit éviter de se charger de l'enregistrement des
    données. Il est préférable que cette opération se fasse en temps réel,
    quand cela est nécessaire (c'est-à-dire quand un objet a été modifié).
    En cas de crash, il se peut très bien que la méthode destroy ne soit pas
    appelée, le garder à l'esprit.
    
    On passe en paramètre du module l'importeur. Cela permet, pour un module,
    d'avoir accès à tous les autres modules chargés. Mais de ce fait,
    il est fortement déconseillé de faire référence à d'autres modules lors
    de la construction du module (méthode __init__).

    """
    def __init__(self, importeur, nom, type="inconnu"):
        """Constructeur d'un module.
        Par défaut, on lui attribue surtout un nom IDENTIFIANT, sans accents
        ni espaces, qui sera le nom du package même.

        Le type du module est soit primaire soit secondaire.

        """
        self.importeur = importeur
        self.nom = nom
        self.type = type
        self.statut = INSTANCIE

    def __str__(self):
        """Retourne le nom, le type et le statut du module."""
        return "{0} (type {1}), {2}".format(self.nom, self.type, \
                statuts[self.statut])
    def config(self):
        """Méthode de configuration.
        On charge ici la configuration.
        """
        raise NotImplementedError

    def init(self):
        """Méthode d'initialisation.
        Dans cette méthode, on se charge, en fonction de la configuration
        (éventuelle), de "lancer" le module. Tout ce qui est lancé dans
        cette méthode doit s'interrompre dans la méthode destroy.
        
        """
        raise NotImplementedError

    def destroy(self):
        """Méthode d'arrêt ou de déchargement du module.
        On l'appelle avant l'arrêt du MUD (en cas de reboot total) ou
        si l'on souhaite décharger ou recharger complètement un module.
        """
        raise NotImplementedError

