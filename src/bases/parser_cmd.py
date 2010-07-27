# -*-coding:Utf-8 -*

"""Ce fichier est définit un parser de la ligne de commande.

Le parser analyse la ligne de commande en se basant sur le module getopt
et traite chaque cas indépendemment.

"""

import sys
import getopt

class ParserCMD(dict):
    """Notre parser de la ligne de commande. Il est hérité de la classe
    dict, puisque se présentant sous la forme d'un dictionnaire contenant :
    { nom_option: valeur_convertie }
    
    Pour parser les options de la ligne de commande, on s'appuie sur
    sys.argv et le module getopt.
    
    """
    def interpreter(self):
        """Méthode d'interprétation des options de la ligne de commande.
        Si des options doivent être rajoutées, c'est ici qu'il faut le faire.
        Renseigner également la méthode help() qui doit indiquer les options
        disponibles.
        
        A noter que le corps et les modules primaires sont seuls à pouvoir
        être configuré via la ligne de commande, sauf option générique.
        
        """
        # Syntaxe des options attendues
        # Elle se présente sous la forme de deux variables :
        # - une chaîne de caractères contenant les flags courts des options.
        #   Si le flag attend un argument, préciser : après la lettre du flag.
        # - une liste, contenant les chaînes des options longues.
        #   Les options doivent être entrées dans le même ordre que les flags
        #   courts correspondants. Pour préciser qu'une option longue
        #   attend un argument, il faut préciser un signe = après le nom.
        
        # Liste des options
        # - c (chemin-configuration) : chemin du dossier contenant les fichiers
        #                             de configuration
        # - e (chemin-enregistrement) : chemin du dossier d'enregistrement
        #                              des données sauvegardées
        # - h (help) : l'aide bien entendu
        # - l (chemin-logs) : chemin d'enregistrement des logs
        # - p (port) : port d'écoute du serveur
        flags_courts = "c:e:hl:p:"
        flags_longs = ["chemin-configuration=", "chemin-enregistrement=", \
                "help", "chemin-logs=", "port="]
        
        # Création de l'objet analysant la ligne de commande
        try:
            opts, args = getopt.getopt(sys.argv[1:], flags_courts, flags_longs)
        except getopt.GetoptError as err:
            print(err)
            sys.exit(1)
        
        # Analyse itérative des options
        for nom,val in opts:
            # On test successivement chaque nom
            # Préférer tester chaque option dans l'ordre alphabétique
            if nom in ["-c", "--chemin-configuration"]:
                self["chemin-configuration"] = val
            elif nom in ["-e", "--chemin-enregistrement"]:
                self["chemin-enregistrement"] = val
            elif nom in ["-l", "--chemin-logs"]:
                self["chemin-logs"] = val
            elif nom in ["-h", "--help"]:
                self.help()
                sys.exit(1)
            elif nom in ["-p", "--port"]:
                # On doit tenter de convertir le port
                try:
                    port = int(val)
                except ValueError:
                    print("Le numéro de port entré est invalide.")
                    sys.exit(1)
                else:
                    self["port"] = port


    def help(self):
        """Méthode retournant l'aide. Si des options sont ajoutées dans
        l'interpréteur, les rajouter ici également.
        
        """
        print( \
            "Options disponibles :\n" \
            "\n" \
            "-c, chemin-configuration\n" \
            "-e, chemin-enregistrement\n" \
            "-h, help : affiche ce message d'aide\n" \
            "-l, chemin-logs\n" \
            "-p, port : paramètre le port d'écoute du serveur")
