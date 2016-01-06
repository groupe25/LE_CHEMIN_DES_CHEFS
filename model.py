__author__ = 'IENAC15 - groupe 25'
from constantes import *
import numpy as np
from random import randint
import os

# import matplotlib.pyplot as plt

try:
    import networkx as nx
    from networkx import DiGraph
except ImportError:
    print("module networkx non installé pour python 3.")
    print("Pour l'installer si vous avez les droits root faire \
    'pip3 install networkx' ou 'python3 -m install pip networkx' ")
    print("Pour une installation sans droit root : télécharger networx, le copier dans le répertoire du projet,"
          "se placer dans le dossier de networkx ett taper : python3 setup.py install --user")
    print("En cas de problème avec pydot commenter les lignes")
    print(" nx.write_dot(self.g, 'toto.dot")
    print("os.system('dot -Tpng toto.dot -o toto.png')")
    print(" Vous n'aurez le graphe au format png mais le programme devrait s'éxécuter.")


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return self.x + other, self.y + other

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Jeu(object):
    def __init__(self, first_player, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        self.player = first_player
        self.click = 0
        self.info = ""
        self.pos_depart = Position(0, 0)
        self.pos_arrivee = Position(0, 0)
        self.g = DiGraph()  # implémentation d'un arbre n-aire
        self.nivMax = 0

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1

    def posVoisinesChef(self, pos):
        """
        :param pos: position chef
        :return: retourne une liste avec les positions
        voisines qui doivent être sur le chemin des chef
        """
        l = []
        long_chemin = len(CHEMIN)
        i = CHEMIN.index((pos.x, pos.y))
        if i - 1 >= 0: l.append(CHEMIN[i - 1])
        if i + 1 <= long_chemin - 1: l.append(CHEMIN[i + 1])
        return l

    def partieTerminee(self):
        return self.matrice[4, 4] in (11, 12)

    def listePosAdversesVoisines(self, pos):
        """
        donne parmi les positions voisines celles occupées par un pion adverse
        :param pos: position extraite du click de souri
        :return: liste de pions adverses voisins de la position pos
        """
        l = self.posVoisinesPion(pos)
        g = []
        for (i, j) in l:
            if (self.player == 1 and self.matrice_jeu[i, j] == 2) or \
                    (self.player == 2 and self.matrice_jeu[i, j] == 1):
                g.append((i, j))
        return g

    #


    def listePosSuiv(self, pos_depart):
        """
        :param pos: position départ à partir de laquelle il y aura capture de pions adverses
        :return:   renvoie la liste des positions "n+2" (4 maxis) qui capturent un pion à partir de la position pos_depart
        """
        listePosSuivantes = []
        for (i, j) in self.listePosAdversesVoisines(pos_depart):
            pos_prise = Position(2 * i - pos_depart.x,
                                 2 * j - pos_depart.y)  # calcul qui renvoie la position de prise "n+2"
            if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8:  # pos existe car plateau de 9 x 9 position
                if self.matrice_jeu[pos_prise.x, pos_prise.y] == 0:  # pos libre
                    listePosSuivantes.append((pos_prise.x, pos_prise.y))
        return listePosSuivantes

    def existeCaptureObligatoire(self, pos):
        """
        Méthode simple pour améliorer la lisibilité/ré-utilisabilité du code
        :param pos: position du click de souris
        :return: vrai s'il y a des pions adverses voisins capturables
        """
        return len(self.listePosSuiv(pos)) != 0

    def posVoisinesPion(self, pos):
        """
        # on en profite pour empêcher la pos centrale (4,4) interdite aux pions soldats
        :param pos: position du pion avant déplacement
        :return: renvoie une liste de tuples positions
        voisines de la position choisie par le joueur lors de son 1er click
        """
        l = []
        # on ajoute à la "list" l les voisins horizontaux et verticaux
        if pos.x - 1 >= 0: l.append((pos.x - 1, pos.y))
        if pos.y - 1 >= 0: l.append((pos.x, pos.y - 1))
        if pos.x + 1 <= 8: l.append((pos.x + 1, pos.y))
        if pos.y + 1 <= 8: l.append((pos.x, pos.y + 1))
        try:
            l.remove((4, 4))
        except ValueError:
            pass
        return l

    def capturePion(self, pos_init, pos_finale):
        """
        renvoie la pos du pion à capturer, connaissance la pos init et la pos finale du pions captureur
        C'est une simple moyenne arithmétique
        """
        return Position((pos_finale.x + pos_finale.x) / 2, (pos_finale.y + pos_finale.y) / 2)


    def construireArbre(self, listeOfNodes, niv,pos):
        """
        fonction récursive qui construit un arbre des positions successives nécessaires pour capturer
        les pions.
        calcule aussi le niveau max nivMax tel que nivMax.
        Le nombre de pions capturé est = nivMax-1
        :param listeOfNodes: liste de noeud de l'arbre
        :param niv: niveau dans l'arbre i.e 0 pour la racine, 1, 2, 3 etc pour les niveaux suivants
        :param pos: position pos du click 1
        :return: none :
        """
        listeOfNodes1 = []
        if len(listeOfNodes)!=0 and len(listeOfNodes1)!=0 or self.nivMax==5 : return
        for (i, j) in listeOfNodes:
            for (m, n) in self.listePosSuiv(Position(i, j)):
                if not self.g.has_edge((m, n), (i, j)):
                    self.g.add_edge((i, j), (m, n))
                    listeOfNodes1.append((m, n))
                    self.g.add_node((m, n), niveau=niv)
                    if self.nivMax < niv: self.nivMax = niv
        self.construireArbre(listeOfNodes1, niv+1,pos)

    def firstClickValide(self, pos):
        """
        :param pos: position pos du premier click du joueur
        :return: bouléen = True si le click 1 est valide
        """
        # on crée un nouvel arbre avec une racine dont le noeud est nommé avec le num du joueur courant
        self.g.clear()
        niv = 0
        # création du noeud avec l'attribut niv=0 cf. networkx documentation
        self.g.add_node(self.player, niveau=niv)
        niv = 1
        listeOfNodes = []
        # Pour tous les positions du jeu, on recherche les pions du joueur courant
        # qui sont à même de capturer des pions adverses
        for i in range(N):
            for j in range(N):
                if self.matrice_jeu[i, j] == self.player and self.existeCaptureObligatoire(Position(i, j)):
                    self.g.add_edge(self.player, (i, j))
                    listeOfNodes.append((i, j))
                    self.g.add_node((i, j), niveau=niv)
        # Préciser le niveau dans les attribut du noeud permettra de sélectionner les branches de
        # de longueur max = nivMax pour avoir les positions licites car prise max obligatoire

        self.construireArbre(listeOfNodes, 2, pos)
        # décommenter cette ligne pour obtenir le dessin du graphe au format png
        nx.write_dot(self.g, 'toto.dot')
        os.system('dot -Tpng toto.dot -o toto.png')

        boule = False
        l = []
        for m in range(N):
            for n in range(N):
                if (self.player == 1 and self.matrice_jeu[m, n] in (1, 11)) or \
                        (self.player == 2 and self.matrice_jeu[m, n] in (2, 12)):
                    l.append((m, n))  # contient les pos des pions du joueur courant
        self.listePriseMax = [(i, j) for (i, j) in l if self.matrice_jeu[i, j] not in (11, 12)
                              and self.existeCaptureObligatoire(Position(i, j))]
        if (pos.x, pos.y) not in l:  # click hors pions joueur courant
            boule = False
        # à partir d'ici l'ensemble des positions  valides est donc ds
        # la liste l = l'ensemble des pions du joueur courant
        # elif len(listePosPionsQuiDoiventCapturer) == 0 or (pos.x, pos.y) in listePosPionsQuiDoiventCapturer:
        elif len(self.listePriseMax) == 0 or (pos.x, pos.y) in self.listePriseMax:
            # s'il n'existe pas de capture obligatoire les pos valides
            # sont dans la liste l
            boule = True
        return boule

    def secondClickValide(self, pos_depart, pos_arrivee):
        boule = self.posLibre(pos_arrivee)
        if self.matrice_jeu[pos_depart.x, pos_depart.y] in (1, 2):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesPion(self.pos_depart)
            # print("pos voisines de la pos click1: ", self.posVoisinesPion(self.pos_depart))
        # ici on traite le cas du déplacement des chefs
        # nb : les chemins imposés resp. aux chefs sont voisins d'où la nécessité
        # de séparer les deux chemins : utilisation d'un dictionnaire CHEF_PATH de type dict() pour associer
        # le chemin 1 au chef1 et le chemin 2 au chef2
        else:  # cas où les pions sont des chefs  self.matrice_jeu[pos_depart.x, pos_depart.y] in (11, 12):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesChef(self.pos_depart)
        return boule

    def jouer(self, i, j):
        pos = Position(i, j)
        self.info = ""
        if self.click == 0 and self.firstClickValide(pos):  # 1er click du joueur qui a la main
            self.click = 1
            self.pos_depart = Position(i, j)
        elif self.click == 1:  # nb : (i, j) est la position arrivee car second click de l'utilisateur
            self.pos_arrivee = Position(i, j)  # affectation ajoutée pour rendre le code plus lisible
            self.click = 0
            if self.secondClickValide(self.pos_depart, self.pos_arrivee):
                self.Play(self.pos_depart, self.pos_arrivee)
                self.switch_player()
        elif self.centralPosOk(self.pos_depart, self.pos_arrivee):
            self.info = "CLICK INVALIDE OU REGLE DE LA PRISE MAX OBLIGATOIRE NON RESPECTEE ! "
        if not self.centralPosOk(self.pos_depart, self.pos_arrivee):
            self.info = "POSITION CENTRALE INTERDITE AUX SOLDATS ! "

    def posLibre(self, pos):
        return self.matrice_jeu[pos.x, pos.y] == 0

    def Play(self, pos_init, pos_finale, l=[]):
        """
        :param l: liste de positions à capturer
        :return:
        """
        if len(l) == 0:
            self.matrice_jeu[pos_finale.x, pos_finale.y] = self.matrice_jeu[pos_init.x, pos_init.y]
            self.matrice_jeu[pos_init.x, pos_init.y] = 0
        else:
            for pos in l:
                if not self.matrice_jeu[pos.x, pos.y] in (11, 12):
                    self.matrice_jeu[pos.x, pos.y] = 0
            self.matrice_jeu[pos_init.x, pos_init.y] = 0
            self.matrice_jeu[pos_finale.x, pos_finale.y] = self.player

    def centralPosOk(self, pos_depart, pos_arrivee):
        """
        :param pos_depart: position 1er click
        :param pos_arrivee: position 2nd click
        :return: renvoie False si le joueur veut déplacer un soldat en position centrale (4,4)
        """
        boule = True
        if pos_arrivee == Position(4, 4) and self.matrice_jeu[pos_depart.x, pos_depart.y] in (1, 2):
            boule = False
        return boule

    def save_jeu(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.player) + "\n")
            for i in range(N):
                for j in range(N):
                    if self.matrice_jeu[i, j] != 0:
                        f.write(str(i) + " " + str(j) + " " + str(self.matrice_jeu[i, j]) + "\n")


def load_jeu(filename):
    """
    :param filename: nom du fichier txt à charger par exemple init_jeu.txt
    qui représente la matrice qui modélise la répartition des pions. cf. ./ressources/init_jeu.txt
    structure des données :
    la première ligne  commence par 0,  1,  ou 2 correspondant au joueur
     qui commence la partie : 0 correspond au cas où le 1er joueur est choisi au hasard
    ensuite la structure du fichier est :  i j code_pion
    i : indice de colonne = abscisse quantifiée de gauche à droite du plateau de jeu
    j : indice de ligne = ordonnée selon axe vertical décroissant.
    l'origine du plateau (i, j) == (0, 0) est située "top-left"
    donc convention inverse de celle retenue pour les matrices en math.
    choix fait pour n'avoir qu'une seule convention dans le modèle et dans la vue
    image_pion = {1 : "pion1.png", 2 : "pion2.png", 11 : "chef1.png", 12 : "chef2.png", 0: ""}
    le fichier ne contient pas les valeurs 0 asscociées à l'absence de pion dans une case
    pour ne pas alourdir le fichier.

    :return:matrice du jeu et le numéro de joueur
    """
    matrice_jeu = np.zeros((9, 9), dtype=int)
    try:
        with open(filename, 'r') as f:
            player = int(f.readline())
            if player == 0: player = randint(1, 2)  #
            for line in f:
                w = line.strip().split()
                matrice_jeu[int(w[0]), int(w[1])] = int(w[2])
    except Exception:
        print("Problème ouverture ou lecture fichier : vérifier le nom et le path.")
    return matrice_jeu, player

