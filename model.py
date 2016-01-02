__author__ = 'IENAC15 - groupe 25'
from constantes import *
import numpy as np
from random import randint
from graph import Node, WGraph
# import networkx as nx
from graphnx import Graph


class Noeud(Node):
    def __init__(self, l):
        super(Noeud, self).__init__(id)
        self.l = l

    def __repr__(self):
        return "({}, {}, {})".format(self.l[0], self.l[1], self.l[3])


class Arbre(WGraph):
    def __init__(self):
        super(Arbre, self).__init__()


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return self.x + other, self.y + other

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)


class Jeu(object):
    def __init__(self, first_player, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        self.player = first_player
        self.click = 0
        self.pos_depart = Position(0, 0)
        self.pos_arrivee = Position(0, 0)
        self.g = Graph()  # implémentation d'un arbre n-aire par un graphe sans doute orienté
        # pour garder la notion de parentée

    def switch_player(self):
        if self.player == 1:
            self.player = 2
        elif self.player == 2:
            self.player = 1

    def posLibre(self, pos):
        return self.matrice_jeu[pos.x, pos.y] == 0

    def movePion(self, pos_depart, pos_arrivee):
        self.matrice_jeu[pos_arrivee.x, pos_arrivee.y] = self.matrice_jeu[self.pos_depart.x, self.pos_depart.y]
        self.matrice_jeu[self.pos_depart.x, self.pos_depart.y] = 0

    def capturePions(self, pos_init, pos_finale, l):
        """

        :param l: liste de positions à capturer
        :return:
        """
        for pos in l:
            if not self.matrice_jeu[pos.x, pos.y] in (11, 12):
                self.matrice_jeu[pos.x, pos.y] = 0
        self.matrice_jeu[pos_init.x, pos_init.y] = 0
        self.matrice_jeu[pos_finale.x, pos_finale.y] = self.player

    def partieTerminee(self):
        return self.matrice[4, 4] in (11, 12)

    def listePosAdversesVoisines(self, pos):
        """
        donne parmi les positions voisines celles occupées par un pion adverse
        :param pos:
        :return:
        """
        l = self.posVoisinesPion(pos)
        g = []
        for (i, j) in l:
            if (self.player == 1 and self.matrice_jeu[i, j] == 2) or \
                    (self.player == 2 and self.matrice_jeu[i, j] == 1):
                g.append((i, j))
        # print("pos voisines avec pions adverse :", g)
        return g

    def existeCaptureObligatoire(self, pos):
        """
        détermine si le pion adverse peut, donc doit, être pris i.e. il existe une case vide voisine du pion adverse
        donc pion prenable
        :param pos:
        :return:
        """
        boule = False
        g = self.listePosAdversesVoisines(pos)
        if len(g) == 0: return boule  # cas pas d'adversaires voisins
        for (i, j) in g:
            voisinAdversaire = Position(i, j)
            boule = self.isPionAdverseVoisinCapturable(pos, voisinAdversaire)[0]
            if boule: break  # il existe au moins une case libre autour de chacun des adversaires : 4 adversaires au max
        return boule

    def isPionAdverseVoisinCapturable(self, pos, pos_adv):
        """
        :param pos: pos pion joueur courant
        :param pos_adv: pos pion adversaire voisin
        :return:booléen , position finale après prise, position à capturer
        """
        boule = False
        pos_prise = Position(2 * pos_adv.x - pos.x,
                             2 * pos_adv.y - pos.y)  # calcul qui renvoie la position de prise "n+2"
        if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8:  # pos existe car plateau de 9 x 9 position
            if self.matrice_jeu[pos_prise.x, pos_prise.y] == 0:  # pos libre
                boule = True
        return boule, pos_prise

    def listePosSuiv(self, pos_depart):
        """
        :param pos: position départ
        :return:   renvoie la liste des positions qui capturent un pion à partir de la position pos_depart
        en utilisant isPionAdverseVoisinCapturable
        """
        listePosSuivantes = []
        for (i, j) in self.listePosAdversesVoisines(pos_depart):
            listePosSuivantes.append(self.isPionAdverseVoisinCapturable(pos_depart, Position(i, j))[1])
        return listePosSuivantes

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

    def plusLongueCapture(self, pos):
        """
        on cherche à retourner une liste avec les pos finales
        maximisant le nombre de captures ( liste qui aura un cardinale de 0 à 4 ; 0 pas de capture, 4 : quatre
         capture de même longeur et retourne
        aussi les positions des pions capturés pour pouvoir les supprimer
        :param pos: position de départ avant le début des captures
        :return: 1 - liste [] pos finales valide 2 - dico {pos_finales : [liste pions à capturer]}
        détails :
        1 - une liste [] avec les pos_finales valides  (à utiliser pour gérer la validités des choix du joeur)
        2 - une liste  de dictionnaires [{clé = pos_finale valide : valeur liste[] avec les pos des pions à prendre}]
        les positions finales sont celles qui capturent le meme nombre max de pions et
        parmi lesquelles le joueur est obligé de choisir. On utilise la clé pos_valides choisie par le joeur
        pour récupérer la liste des pions adverses à capturer
        """
        l = self.posVoisinesPion(pos)
        g = []
        for (i, j) in l:

            if (self.player == 1 and self.matrice_jeu[i, j] == 2) or \
                    (self.player == 2 and self.matrice_jeu[i, j] == 1):
                g.append((i, j))
                self.plusLongueCapture(Position(i, j));
                print("appel de plusLongueCapture")
        print("pos voisines avec pions adverse :", g)
        return g

    def posVoisinesPion(self, pos):
        """
        # retourne les 4 positions voisines possibles au maximum pour les soldats
        # on en profite pour empêcher la pos centrale (4,4) interdite aux pions soldats
        :param pos: position du pion avant déplacement
        :return:
        """
        l = []
        # on ajoute à la "list" l les vosins horizontaux et verticaux
        if pos.x - 1 >= 0: l.append((pos.x - 1, pos.y))
        if pos.y - 1 >= 0: l.append((pos.x, pos.y - 1))
        if pos.x + 1 <= 8: l.append((pos.x + 1, pos.y))
        if pos.y + 1 <= 8: l.append((pos.x, pos.y + 1))
        try:
            l.remove((4, 4))
        except ValueError:
            pass
        return l

    def creationArbre(self, pos_dep):
        """
        1er essai alimentation récursive de l'arbre self.g
        utilise un graphe du module networknx
        peut-être utiliser un graphe orienté pour implémenter cet arbre n-aire
        :param pos_dep:
        :return:
        """
        s = self.listePosSuiv(pos_dep)
        if len(s) == 0:
            exit()  # sortie de la récursion
        for (m, n) in s:  # pour chaque branche
            self.g.add_edge((pos_dep.x, pos_dep.y), (m, n))
            self.creationArbre(Position(m, n))

    def priseMax(self, listePosPionsQuiDoiventCapturer):
        listePosPriseMax = []
        listeCapture = []
        listePosArrivee = []

        l = list(listePosPionsQuiDoiventCapturer)

        for (i, j) in l:  # pour (i, j) fixé
            s = self.listePosSuiv(Position(i, j))
            # s= self.listePosAdversesVoisines(Position(i,j))
            # while len(s)!=0:
            # for (m, n) in s:
            #     dd = self.listePosSuiv(Position(m,n))
            #     g = Graph()
            #     u = 0
            #   #  g.add_node(u)
            #     v = u+1
            #     g.add_edge(u, v)

        return listePosPriseMax, listeCapture, listePosArrivee

    def firstClickValide(self, pos):
        boule = False
        l = []
        for m in range(N):
            for n in range(N):
                if (self.player == 1 and self.matrice_jeu[m, n] in (1, 11)) or \
                        (self.player == 2 and self.matrice_jeu[m, n] in (2, 12)):
                    l.append((m, n))  # contient les pos des pions du joueur courant
        # self.listePriseMax contient la liste des pos initiales avant capture
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
        # on a la liste listePosPionsQuiDoiventCapturer ; pour chaque pos de cette liste on dot déterminer
        # la ou les pos qui donne lieu à une prise maxi. c'est donc un nouveau filtrage.
        # on cherche à avoir une listePosPriseMax qui donnera les positions valides pour le 1er click.
        # or (pos.x, pos.y) in listePosPionsQuiDoiventCapturer: cette condition est insuffisante,

        # on crée une méthode qui prend en argument une liste de positions dont on sait qu'elles captures au moins
        # un pions et qui retourne la liste listePosPriseMax, la liste des pions à prendre listeCapture
        #  et la liste des pos finales du pion qui donnera une prise max
        #  listePosArrivee donc liste des pos valide pour le second click
        return boule

    def secondClickValide(self, pos_depart, pos_arrivee):
        boule = self.posLibre(pos_arrivee) and pos_arrivee != pos_depart
        if self.matrice_jeu[pos_depart.x, pos_depart.y] in (1, 2):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesPion(self.pos_depart)
            print("pos voisines pions : ", self.posVoisinesPion(self.pos_depart))
        # ici on traite le cas du déplacement des chefs
        # nb : les chemins imposés resp. aux chefs sont voisins d'où la nécessité
        # de séparer les deux chemins : utilisation d'un dictionnaire CHEF_PATH de type dict() pour associer
        # le chemin 1 au chef1 et le chemin 2 au chef2
        else:  # cas où les pions sont des chefs  self.matrice_jeu[pos_depart.x, pos_depart.y] in (11, 12):
            boule = boule and (pos_arrivee.x, pos_arrivee.y) in self.posVoisinesChef(self.pos_depart)
        return boule

    def jouer(self, i, j):
        pos = Position(i, j)
        if self.click == 0 and self.firstClickValide(pos):  # 1er click du joueur qui a la main
            self.click = 1
            self.pos_depart = Position(i, j)
            # self.plusLongueCapture(self.pos_depart)
        elif self.click == 1:  # nb : (i, j) est la position arrivee car second click de l'utilisateur
            self.pos_arrivee = Position(i, j)  # affectation ajoutée pour rendre le code plus lisible
            self.click = 0
            if self.secondClickValide(self.pos_depart, self.pos_arrivee):
                self.movePion(self.pos_depart, self.pos_arrivee)
                self.switch_player()

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

    :return:
    """
    matrice_jeu = np.zeros((9, 9), dtype=int)
    with open(filename, 'r') as f:
        player = int(f.readline())
        if player == 0: player = randint(1, 2)  #
        for line in f:
            w = line.strip().split()
            matrice_jeu[int(w[0]), int(w[1])] = int(w[2])
    return matrice_jeu, player
