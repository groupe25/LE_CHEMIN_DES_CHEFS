__author__ = 'IENAC15 - groupe 25'
import numpy as np
import collections
from random import randint

N = 9  # 9 intersections  donc 8 cases

CHEMIN = [(4, 0), (5, 1), (5, 2), (5, 3), (6, 4), (7, 3), (7, 4),
          (8, 4), (7, 5), (8, 6), (7, 6), (7, 7), (6, 6),
          (5, 7), (5, 6), (4, 6), (5, 5), (4, 4), (3, 3),
          (4, 2), (3, 2), (3, 1), (2, 2), (1, 1), (1, 2),
          (0, 2), (1, 3), (0, 4), (1, 4), (1, 5), (2, 4),
          (3, 5), (3, 6), (3, 7), (4, 8)]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Jeu(object):
    def __init__(self, first_player, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        # self.player = randint(1, 2)
        self.player = first_player
        self.click = 0
        self.pos_depart = Position(0, 0)

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1

    def firstClickOk(self, i, j):
        """
        contrôle de la validité du 1er clic du joueur
        :param i:
        :param j:
        :return:
        """
        boule = False
        if self.player == 1 and self.matrice_jeu[i][j] in (1, 11): boule = True
        if self.player == 2 and self.matrice_jeu[i][j] in (2, 12): boule = True
        return boule

    def posLibre(self, pos):
        return self.matrice_jeu[pos.x][pos.y] == 0

    def secondClickOk(self, pos_depart, pos_arrivee):
        boule = self.posLibre(pos_arrivee)
        if self.matrice_jeu[pos_depart.x, pos_depart.y] in (1, 2):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesPion(self.pos_depart)
        # ici on traite le cas du déplacement des chefs
        # nb : les chemins imposés resp. aux chefs sont voisins d'où la nécessité
        # de séparer les deux chemins : utilisation d'un dictionnaire CHEF_PATH de type dict() pour associer
        # le chemin 1 au chef1 et le chemin 2 au chef2
        else:  # cas où les pions sont des chefs  self.matrice_jeu[pos_depart.x, pos_depart.y] in (11, 12):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesChef(self.pos_depart)
        return boule

    def movePion(self, pos_depart, pos_arrivee):
        self.matrice_jeu[pos_arrivee.x][pos_arrivee.y] = self.matrice_jeu[self.pos_depart.x][self.pos_depart.y]
        self.matrice_jeu[self.pos_depart.x][self.pos_depart.y] = 0

    def capturePion(self, pos):
        if not self.matrice_jeu[pos.x, pos.y] in (11, 12):
            self.matrice_jeu[pos.x, pos.y] = 0

    def partieTerminee(self):
        return self.matrice[4, 4] in (11, 12)

    def posVoisinesPion(self, pos):
        """
        # 4 position voisines possibles pour les soldats
        :param pos: position du pion avant déplacement
        :return:
        """
        l = []
        # on ajoute à la "list" l les vosins horizontaux et verticaux
        if pos.x - 1 >= 0: l.append((pos.x - 1, pos.y))
        if pos.y - 1 >= 0: l.append((pos.x, pos.y - 1))
        if pos.x + 1 <= 8: l.append((pos.x + 1, pos.y))
        if pos.y + 1 <= 8: l.append((pos.x, pos.y + 1))
        return l

    def posVoisinesChef(self, pos):
        l = []
        long_chemin = len(CHEMIN)
        i = CHEMIN.index((pos.x, pos.y))
        if i - 1 >= 0: l.append(CHEMIN[i - 1])
        if i + 1 <= long_chemin - 1: l.append(CHEMIN[i + 1])
        return l

    def jouer(self, i, j):
        print("right_player :", self.firstClickOk(i, j))
        print("click = ", self.click)
        if self.click == 0 and self.firstClickOk(i, j):
            self.click = 1
            self.pos_depart = Position(i, j)
        elif self.click == 1:  # nb : (i, j) est la position arrivee car second click de l'utilisateur
            self.click = 0
            self.pos_arrivee = Position(i, j)  # affectation ajoutée pour rendre le code plus lisible
            if self.secondClickOk(self.pos_depart, self.pos_arrivee):
                self.movePion(self.pos_depart, self.pos_arrivee)
                self.switch_player()



    def save_jeu(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.player) + "\n")
            for i in range(N):
                for j in range(N):
                    if self.matrice_jeu[i][j] != 0:
                        f.write(str(i) + " " + str(j) + " " + str(self.matrice_jeu[i][j]) + "\n")


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

    :return:
    """
    matrice_jeu = np.zeros((9, 9), dtype=int)
    with open(filename, 'r') as f:
        player = int(f.readline())
        if player == 0: player = randint(1, 2)  #
        for line in f:
            w = line.strip().split()
            matrice_jeu[int(w[0])][int(w[1])] = int(w[2])
    return matrice_jeu, player
