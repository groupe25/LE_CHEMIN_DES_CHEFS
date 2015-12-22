__author__ = 'IENAC15 - groupe 25'
import sys
import numpy as np

from random import randint
sys.path.insert(0, sys.path[0] + "/ressources/")
DATA = sys.path[0]
DATA = sys.path[0]
N = 9  # 9 intersections  donc 8 cases
CHEMIN = [(4, 0), (5, 1), (5, 3), (6, 4), (7, 3), (7, 4), \
           (8, 4), (7, 5), (8, 6), (7, 6), (7, 7), (6, 6), \
           (5, 7), (5, 6), (4, 6), (5, 5), (4, 4), (3, 3), \
           (4, 2), (3, 2), (3, 1), (2, 2), (1, 1), (1, 2), \
           (0, 2), (1, 3), (0, 4), (1, 4), (1, 5), (2, 4), \
           (3, 5), (3, 7), (4, 8)]

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)


class Jeu:
    def __init__(self,first_player, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        # self.player = randint(1, 2)
        self.player = first_player
        self.click = 0
        self.pos_depart = Position(0, 0)

    def switch_player(self):
        if self.player == 1: self.player = 2
        elif self.player == 2: self.player = 1

    def right_player(self, i, j):
        boule = False
        if self.player == 1 and self.matrice_jeu[i][j] in (1, 11): boule = True
        if self.player == 2 and self.matrice_jeu[i][j] in (2, 12): boule = True
        return boule

    def voisins(self, pos):
        """
        # position voisines possibles pour les soldats: PROBLEME les chefs doivent pouvoir se déplacer obliquement
        contrairement aux soldat
        :param pos:
        :return:
        """
        l = []
        if pos.x - 1 >= 0: l.append((pos.x - 1, pos.y))
        if pos.y - 1 >= 0: l.append((pos.x, pos.y - 1))
        if pos.x + 1 <= 8: l.append((pos.x + 1, pos.y))
        if pos.y + 1 <= 8: l.append((pos.x, pos.y + 1))
        return l

    def jouer(self, i, j):
        print("right_player :", self.right_player(i, j))
        print("click = ", self.click)
        if self.click == 0 and self.right_player(i, j):
            self.click = 1
            self.pos_depart = Position(i, j)
        elif self.click == 1: # (i, j) est la position arrivee car second click de l'utilisateur
            self.click = 0
            if self.matrice_jeu[i][j] == 0 and (i, j) in self.voisins(self.pos_depart) : # le joueur qui a la main fait une action licite
                self.matrice_jeu[i][j] = self.matrice_jeu[self.pos_depart.x][self.pos_depart.y]
                self.matrice_jeu[self.pos_depart.x][self.pos_depart.y] = 0
                self.switch_player()  # implémenter la modif de l'affichage "A vous de jouer joueur x"

    def save_jeu(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.player) + "\n")
            # for line in f:
            for i in range(N):
                for j in range(N):
                    if self.matrice_jeu[i][j] != 0:
                        f.write(str(i) + " " + str(j) + " " + str(self.matrice_jeu[i][j]) + "\n")




def load_jeu(filename):
    """
    :param filename: nom du fichier txt à charger par exemple init_jeu.txt
    qui représente la matrice qui modélise la répartition des pions. cf. ./data/init_jeu.txt
    structure des données :
    la première ligne  commence par 0,  1,  ou 2 correspondant au joueur
     qui commence la partie : 0 correspond au cas où le first player est choisi au hasard
    i j code_pion
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
        if player == 0 : player = randint(1, 2) #
        for line in f:
            w = line.strip().split()
            matrice_jeu[int(w[0])][int(w[1])] = int(w[2])
    return matrice_jeu, player




