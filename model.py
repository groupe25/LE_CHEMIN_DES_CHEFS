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
    print("Pour l'installer 'pip3 install networkx' ou 'python3 -m install pip networkx' ")


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

    #


    def listePosSuiv(self, pos_depart):
        """
        :param pos: position départ à partir de laquelle il y aura capture de pions adverses
        :return:   renvoie la liste des positions "n+2" (4 maxis) qui capturent un pion à partir de la position pos_depart
        """
        listePosSuivantes = []
        for (i, j) in self.listePosAdversesVoisines(pos_depart):
            pos_prise = Position(2 * i - pos_depart.x, 2 * j - pos_depart.y)  # calcul qui renvoie la position de prise "n+2"
            if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8:  # pos existe car plateau de 9 x 9 position
                if self.matrice_jeu[pos_prise.x, pos_prise.y] == 0:  # pos libre
                    listePosSuivantes.append((pos_prise.x,pos_prise.y))
        return listePosSuivantes




    def existeCaptureObligatoire(self, pos):
        return len(self.listePosSuiv(pos)) != 0
    def posVoisinesPion(self, pos):
        """
        # retourne les positions voisines de la position choisie par le joueur lors de son 1er click
        # on en profite pour empêcher la pos centrale (4,4) interdite aux pions soldats
        :param pos: position du pion avant déplacement
        :return: renvoie une liste de tuples
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
    def capturePion(self,pos_init, pos_finale ):
        """
        renvoie la pos du pion à capturer, connaissance la pos init et la pos finale du pions captureur
        C'est une simple moyenne arithmétique
        """
        return Position((pos_finale.x + pos_finale.x) / 2,(pos_finale.y + pos_finale.y) / 2)



    cpt=0 # BUG DANS CETTE FONCTION RECURSIVE : lien avec la pos (4,4)
    def creationArbre(self, pos_dep):
        """
        1er essai alimentation récursive de l'arbre self.g
        utilise un graphe du module networknx
        reprendre l'arbre créé avec les positions initales self.g
        de niveau 1, la racine symbolise le joueur ou le tour de jeu.
        pour chaque noeud niveau 1, on nos pos_dep
        comment récupérer les id de ces noeuds
        :param pos_dep:
        :return:
        """
        s = self.listePosSuiv(pos_dep) # liste des pos "n+2
        self.cpt +=1 ; print(self.cpt)
        # if self.cpt > 10: return
        print("dddddd len s ffff", len(s))
        if len(s) == 0 : return
        print("listepos suiv ", s)
        rang = 0
        for (m, n) in s:  # pour chaque branche
            rang +=1
            if (m,n) in self.g.nodes():break
            self.g.add_edge((pos_dep.x, pos_dep.y), (m, n))
            self.g.node[(m,n)]['rang'] = rang
            print(self.g.node[(m,n)])
            pos_a_capturer = self.capturePion(pos_dep, Position(m,n))
            self.matrice_jeu[pos_a_capturer.x,pos_a_capturer.y]= 0
            self.creationArbre(Position(m, n))
            nx.write_dot(self.g, 'toto.dot')
            os.system('dot -Tpng toto.dot -o toto.png')

    def firstClickValide(self, pos):

        ###############################################################################################
        self.g.clear()
        listeOfEdges = []
        for i in range(N):
            for j in range(N):

                if self.matrice_jeu[i, j] == self.player and self.existeCaptureObligatoire(Position(i, j)):
                    listeOfEdges.append(((-1, -1), (i, j)))
        self.g.add_edges_from(listeOfEdges) # crée les aretes et les noeuds associés
        # print(self.g.nodes())
        listePosDepart = [(i,j) for (i,j) in self.g if (i,j)!= (-1,-1) ]
        # print("list pos dep dans firstclic", listePosDepart)
        for (i,j) in listePosDepart:
              self.creationArbre(Position(i,j))
        print("self.posSuiv wwwwwwwwwww ", self.listePosSuiv(pos))
        #print("listePosAdversesVoisines(pos)", self.listePosAdversesVoisines( pos))


        nx.write_dot(self.g, 'toto.dot')
        os.system('dot -Tpng toto.dot -o toto.png')

        ###############################################################################################
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
    with open(filename, 'r') as f:
        player = int(f.readline())
        if player == 0: player = randint(1, 2)  #
        for line in f:
            w = line.strip().split()
            matrice_jeu[int(w[0]), int(w[1])] = int(w[2])
    return matrice_jeu, player






    # def existeCaptureObligatoire(self, pos):
    #     """
    #     détermine si le pion adverse peut, donc doit, être pris i.e. il existe une case vide voisine du pion adverse
    #     donc pion prenable
    #     :param pos:
    #     :return:
    #     """
    #     boule = False
    #     g = self.listePosAdversesVoisines(pos)
    #     if len(g) == 0: return boule  # cas pas d'adversaires voisins
    #     for (i, j) in g:
    #         voisinAdversaire = Position(i, j)
    #         l = list(self.isPionAdverseVoisinCapturable(pos, voisinAdversaire))
    #         boule = l[0]
    #         if boule:break  # il existe au moins une case libre autour de chacun des adversaires : 4 adversaires au max
    #     return boule  # boule2 pour éviter que boule ne revienne à False

    #
    # def isPionAdverseVoisinCapturable(self, pos, pos_adv):
    #     """
    #     :param pos: pos pion joueur courant
    #     :param pos_adv: pos pion adversaire voisin
    #     :return:booléen , position finale après prise, position à capturer
    #     """
    #     boule = False
    #     pos_prise = Position(2 * pos_adv.x - pos.x,
    #                          2 * pos_adv.y - pos.y)  # calcul qui renvoie la position de prise "n+2"
    #     if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8:  # pos existe car plateau de 9 x 9 position
    #         if self.matrice_jeu[pos_prise.x, pos_prise.y] == 0:  # pos libre
    #             boule = True
    #     return boule, pos_prise
    #




    # cpt=0 # BUG DANS CETTE FONCTION RECURSIVE : lien avec la pos (4,4)
    # def creationArbre(self, pos_dep):
    #     """
    #     1er essai alimentation récursive de l'arbre self.g
    #     utilise un graphe du module networknx
    #     reprendre l'arbre créé avec les positions initales self.g
    #     de niveau 1, la racine symbolise le joueur ou le tour de jeu.
    #     pour chaque noeud niveau 1, on nos pos_dep
    #     comment récupérer les id de ces noeuds
    #     :param pos_dep:
    #     :return:
    #     """
    #     s = self.listePosSuiv(pos_dep) # liste des pos "n+2
    #     print("listepos suiv ", s)
    #     print(len(s))
    #     self.cpt +=1 ; print(self.cpt)
    #     if self.cpt > 20: return
    #     if len(s) == 0 : return
    #     # if not self.existeCaptureObligatoire(pos_dep): return
    #     for (m, n) in s:  # pour chaque branche
    #         print("mn = ",self.existeCaptureObligatoire(pos_dep))
    #         # if not self.existeCaptureObligatoire(pos_dep): break
    #         bck_mat = self.matrice_jeu.copy()
    #         print("mat", bck_mat)
    #         self.g.add_edge((pos_dep.x, pos_dep.y), (m, n))
    #         print("edge ", pos_dep.x,pos_dep.y, m, n)
    #         pos_a_capturer = self.capturePion(pos_dep, Position(m,n))
    #         self.matrice_jeu[pos_a_capturer.x,pos_a_capturer.y]= 0
    #         print(" recursion creation arbre")
    #         self.creationArbre(Position(m, n))
    #         nx.write_dot(self.g, 'toto.dot')
    #         os.system('dot -Tpng toto.dot -o toto.png')
    #     self.matrice_jeu = bck_mat.copy()



    #
    # cpt=0 # BUG DANS CETTE FONCTION RECURSIVE : lien avec la pos (4,4)
    # def creationArbre(self, pos_dep):
    #     """
    #     1er essai alimentation récursive de l'arbre self.g
    #     utilise un graphe du module networknx
    #     reprendre l'arbre créé avec les positions initales self.g
    #     de niveau 1, la racine symbolise le joueur ou le tour de jeu.
    #     pour chaque noeud niveau 1, on nos pos_dep
    #     comment récupérer les id de ces noeuds
    #     :param pos_dep:
    #     :return:
    #     """
    #     s = self.listePosSuiv(pos_dep) # liste des pos "n+2
    #     print("listepos suiv ", s)
    #     print(len(s))
    #     self.cpt +=1 ; print(self.cpt)
    #     # if self.cpt > 10: return
    #     print("listePosSuiv :",s)
    #     if len(s) == 0 : return
    #
    #     for (m, n) in s:  # pour chaque branche
    #         bck_mat = self.matrice_jeu.copy()
    #         print("mat", bck_mat)
    #         self.g.add_edge((pos_dep.x, pos_dep.y), (m, n))
    #         print("edge ", pos_dep.x,pos_dep.y, m, n)
    #         pos_a_capturer = self.capturePion(pos_dep, Position(m,n))
    #         self.matrice_jeu[pos_a_capturer.x,pos_a_capturer.y]= 0
    #         print(" recursion creation arbre")
    #         self.creationArbre(Position(m, n))
    #         nx.write_dot(self.g, 'toto.dot')
    #         os.system('dot -Tpng toto.dot -o toto.png')
    #         self.matrice_jeu = bck_mat.copy()


    # def auSuivant(self, pos_dep, pos_arr):
    #
    #     s1 = set(self.listePosSuiv(pos_dep))
    #     s2 = set(self.listePosSuiv(pos_arr))
    #     return list()
    #
    #     lsd = []
    #     lsd = [(i,j) in l2 if (i,j) not in l1]
    #     for (i, j) in self.listePosAdversesVoisines(pos_dep):
    #         pos_prise = Position(2 * i - pos_dep.x, 2 * j - pos_dep.y)  # calcul qui renvoie la position de prise "n+2"
    #         if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8:  # pos existe car plateau de 9 x 9 position
    #             if self.matrice_jeu[pos_prise.x, pos_prise.y] == 0:  # pos libre
    #                 lsd.append((pos_prise.x,pos_prise.y))
    #     return lsd