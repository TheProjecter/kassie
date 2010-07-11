# -*-coding:Utf-8 -*

"""Ce fichier définit la classe Fonction, détaillée plus bas."""

class Fonction:
    """Cette classe définit une fonction possédant une liste
    de paramètres, que l'on peut ainsi appeler à tout moment.
    """
    def __init__(self, fonction, *parametres):
        """Créée  un objet Fonction gardant la fonction et les paramètres
        à appeler. Pour exécuter cette fonction, on utilise la méthode d'objet
        exec().

        A noter que la méthode exec() peut prendre des paramètres
        supplémentaires. Ils seront ajoutés à la liste des paramètres
        précisés lors de la construction de l'objet.

        """
        self.fonction = fonction
        self.parametres = parametres # sous la forme d'un tuple

    def exec(self, *params_sup):
        """Cette méthode permet d'exécuter la fonction contenue dans
        self.fonction en lui passant en paramètre :
        - les paramètres contenus dans self.parametres
        - les paramètres contenus dans params_sup

        """
        if self.fonction is not None:
            parametres = self.parametres + params_sup
            self.fonction(*parametres)
