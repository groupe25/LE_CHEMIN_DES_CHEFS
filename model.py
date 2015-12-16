__author__ = 'IENAC15 - groupe 25'
import sys
sys.path.insert(0, sys.path[0] + "/data/")
DATA = sys.path[0]
EXT = ".png"

DATA = sys.path[0]

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



def load_jeu(filename):
    """
    :param filename: nom du fichier txt à charger e.g. init_jeu.txt : image i j
     avec image = pion1, pion2, chef1, chef2 ou rien
    :return:
    """
    jeu = []
    t = ("pion1"+ EXT , "chef1" + EXT, "pion2" + EXT, "chef2" + EXT)
    with open(filename,'r') as f:
        for line in f:
            w = line.strip().split()
            if w[0] not in t: w[0] = ""
            pion = Pion(w[0], int(w[1]), int(w[2]))
            jeu.append(pion)
    return jeu

