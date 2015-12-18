__author__ = 'IENAC15 - groupe 25'
import sys
from random import randint
sys.path.insert(0, sys.path[0] + "/data/")
DATA = sys.path[0]
EXT = ".png"
pos_depart1=0
pos_depart2=0
click=0
DATA = sys.path[0]
class Jeu:
    def __init__(self,player,jeu):
        self.player=player
        self.jeu=jeu
    #player: 1 ou 2
    #click=None
    first=randint(1,2)
    tour=first
    def right_player(self,i,j):
        return tour%2==jeu[i][j] or tour%2==(jeu[i][j]+10) and jeu[i][j]!=0

    def jouer(self,i,j):
        if click==0 and right_player(i,j):
            click=1
            pos_depart1=i
            pos_depart2=j
        elif click==1:
            a=jeu[i][j]
            jeu[i][j]=jeu[pos_depart1][pos_depart2]
            if jeu[i][j]==0:
                jeu[pos_depart1][pos_depart2]=a
            else:
                jeu[pos_depart1][pos_depart2]=0
            click=0




class  Pion:
    def __init__(self,image, i, j):
        self.image = image
        self.i = i
        self.j = j


    def __str__(self):
        return "image : {} - position {} {}".format(self.image, self.i, self.j)


class Position:
    def __int__(self, i, j):
        self.i = i
        self.j = j


#
# def load_jeu(filename):
#     """
#     :param filename: nom du fichier txt à charger e.g. init_jeu.txt : image i j
#      avec image = pion1, pion2, chef1, chef2 ou rien
#     :return:
#     """
#     jeu = []
#     t = ("pion1"+ EXT , "chef1" + EXT, "pion2" + EXT, "chef2" + EXT)
#     with open(filename,'r') as f:
#         for line in f:
#             w = line.strip().split()
#             if w[0] not in t: w[0] = ""
#             pion = Pion(w[0], int(w[1]), int(w[2]))
#             jeu.append(pion)
#     return jeu
jeu_init=[[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2],[11,1,0,0,0,0,0,2,12],[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2],[1,1,0,0,0,0,0,2,2]]
