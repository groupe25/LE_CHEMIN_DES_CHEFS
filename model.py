__author__ = 'IENAC15 - groupe 25'
import sys
import numpy as np
from random import randint

sys.path.insert(0, sys.path[0] + "/data/")
DATA = sys.path[0]
DATA = sys.path[0]


# class Jeu:
#     click = 0
#     pos_depart1 = 0
#     pos_depart2 = 0
#     def __init__(self,player, matrice_jeu):
#         self.player = player
#         self.matrice = matrice_jeu
#     #player: 1 ou 2
#     #click=None
#     first = randint(1, 2)
#     tour = first
#
#     def right_player(self, i, j):
#         return self.tour % 2 == self.matrice_jeu[i][j] or self.tour % 2 == (self.matrice_jeu[i][j] + 10) and self.matrice_jeu[i][j] != 0
#
#     def jouer(self, i, j):
#         if self.click == 0 and self.right_player(i, j):
#             click=1
#             pos_depart1 = i
#             pos_depart2 = j
#         elif self.click == 1:
#             a = self.matrice_jeu[i][j]
#             self.matrice_jeu[i][j] = self.matrice_jeu[self.pos_depart1][self.pos_depart2]
#             if self.matrice_jeu[i][j] == 0:
#                 self.matrice_jeu[self.pos_depart1][self.pos_depart2] = a
#             else:
#                 self.matrice_jeu[self.pos_depart1][self.pos_depart2] = 0
#             click=0


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y



class Jeu:
    click = 0
    pos_depart = Position(0, 0)
    def __init__(self, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        self.tour = randint(1, 2)

    def right_player(self, i, j):
        return (self.tour % 2 == self.matrice_jeu[i][j] or self.tour % 2 == (self.matrice_jeu[i][j] + 10)) and self.matrice_jeu[i][j] != 0

    def jouer(self, i, j):
        print("right_player :", self.right_player(i, j))
        print("click = ", self.click)
        if self.click == 0 and self.right_player(i, j):
            self.click = 1
            pos_depart = Position(i, j)
            print("pos depart  ",pos_depart)
        elif self.click == 1:
            a = self.matrice_jeu[i][j]
            pos_arrivee = Position(i, j)
            print("pos arr :", pos_arrivee)
            self.matrice_jeu[i][j] = self.matrice_jeu[self.pos_depart.x][self.pos_depart.y]
            if self.matrice_jeu[i][j] == 0:
                self.matrice_jeu[self.pos_depart.x][self.pos_depart.y] = a
            else:
                self.matrice_jeu[self.pos_depart.x][self.pos_depart.y] = 0
            click=0







# class Jeu:
#     def __init__(self, matrice_jeu):
#         self.matrice_jeu = matrice_jeu
#         self.first = randint(1, 2)
#
#     def jouer(self, i, j):
#         pass
#         # while self.matrice_jeu[4](4) not in (11, 12):
#         if self.matrice_jeu[i][j] % 2 == 0 :  # 0 si pion (i, j) de type 2 ou 12 sinon 1 ou 11
#             print( )
#
#     def right_player(self, i, j):
#          return self.tour % 2 == self.matrice_jeu[i][j] or self.tour % 2 == (self.matrice_jeu[i][j] + 10) and self.matrice_jeu[i][j] != 0


class Pion:
    def __init__(self, image, i, j):
        self.image = image
        self.i = i
        self.j = j

    def __str__(self):
        return "image : {} - position {} {}".format(self.image, self.i, self.j)



def load_jeu(filename):
    """
    :param filename: nom du fichier txt à charger par exemple init_jeu.txt
    qui représente la matrice qui modélise la répartition des pions. cf. ./data/init_jeu.txt
    structure des données : i j code_pion
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
        for line in f:
            w = line.strip().split()
            matrice_jeu[int(w[0])][int(w[1])] = int(w[2])
    return matrice_jeu


def save_jeu(filename):
    pass




# jeu_init=[\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2],\
# [11,1,0,0,0,0,0,2,12],\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2],\
# [1,1,0,0,0,0,0,2,2]]
