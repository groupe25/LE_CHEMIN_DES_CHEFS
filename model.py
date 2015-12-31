__author__ = 'IENAC15 - groupe 25'
import numpy as np
import collections
from random import randint

# import networkx

N = 9  # 9 intersections  donc 8 cases

CHEMIN = [(4, 0), (5, 1), (5, 2), (5, 3), (6, 4), (7, 3),
          (7, 4), (8, 4), (7, 5), (8, 6), (7, 6), (7, 7),
          (6, 6), (5, 7), (5, 6), (4, 6), (5, 5), (4, 4),
          (3, 3), (4, 2), (3, 2), (3, 1), (2, 2), (1, 1),
          (1, 2), (0, 2), (1, 3), (0, 4), (1, 4), (1, 5),
          (2, 4), (3, 5), (3, 6), (3, 7), (4, 8)]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return self.x + other, self.y + other



class Jeu(object):
    def __init__(self, first_player, matrice_jeu):
        self.matrice_jeu = matrice_jeu
        # self.player = randint(1, 2)
        self.player = first_player
        self.click = 0
        self.pos_depart = Position(0, 0)
        # self.pos_arrivee = Position(0,0)

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

    def movePion(self, pos_depart, pos_arrivee):
        self.matrice_jeu[pos_arrivee.x][pos_arrivee.y] = self.matrice_jeu[self.pos_depart.x][self.pos_depart.y]
        self.matrice_jeu[self.pos_depart.x][self.pos_depart.y] = 0

    def capturePions(self, l):
        """

        :param l: liste de positions à capturer
        :return:
        """
        for pos in l:
            if not self.matrice_jeu[pos.x, pos.y] in (11, 12):
                self.matrice_jeu[pos.x, pos.y] = 0

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
            voisinsAdversaire = Position(i, j)
            boule = self.isPionAdverseVoisinCapturable(pos, voisinsAdversaire)
            if boule: break # il existe au moins une case libre autour de chacun des adversaires : 4 adversaires au max
        return boule

    def isPionAdverseVoisinCapturable(self,pos, pos_adv):
        """
        :param pos: pos pion joueur courant
        :param pos_adv: pos pion adversaire voisin
        :return:booléen
        """
        boule = False
        pos_prise = Position(2 * pos_adv.x - pos.x, 2 * pos_adv.y - pos.y)# calcul qui renvoie la position de prise "n+2"
        if 0 <= pos_prise.x <= 8 and 0 <= pos_prise.y <= 8 : #pos existe car plateau de 9 x 9 position
            if self.matrice_jeu[pos_prise.x][pos_prise.y] == 0 : # pos libre
                boule = True
        return boule #, pos_prise

    def existePosVoisineLibre(self, pos):
        """
        indique si autour de pos, il y a au moins une position libre = 0
        A utiliser pour déterminer si un pion adverse est prenable car il existe une pos vide voisine
        :param pos: position d'un pion
        :return: boule un booléen = True s'il existe un pos vide
        """
        boule = False
        l = self.posVoisinesPion(pos)  # ici, la liste retournée élimine la case centrale 4 4
        # un pion soldat ne peut se positionner sur cette case mais a t il le droit de la "traverser"
        # dans le cas de prise multiple n'induisant pas un positionnement sur cette case ??????????
        for (i, j) in l:
            if self.matrice_jeu[i][j] == 0:
                boule = True ; break
        return boule

    def listePosPriseObligatoire(self):
        """
        Pour tous les pions du jeu on détermine la liste des positions
        sur lesquelles le joueur doit obligatoirement clicker : Pb : ici on ne tiens
        pas encore compte des prises multiples. si le joeur adverse joue et provoque
        en un coup l'appartition de plusieurs possiblités de prises, c'est la plus longue qui
        doit être prise en considération. MEME PB RECURSIF que pour traiter la validité du second click

        :return: liste des positions des pions du joueur courant qui doivent qui peuvent/doivent prendre
        au moins un pion adverse.
        """
        l = []
        for i in range(N):
            for j in range(N):
                pos = Position(i, j)
                if self.matrice_jeu[i, j] == self.player and self.existeCaptureObligatoire(pos):
                    # par exemple si player=1 on ne considère que les pos avec des pions1 qui ont un voisin qui est un adversaire "capturable"
                    l.append((i, j))
        return l

    def firstClickOk(self, i, j):
        """ contrôle de la validité du 1er clic du joueur
        :param i:
        :param j:
        :return:
        """
        boule = False
        l = self.listePosPriseObligatoire()
        print("listePosPriseObligatoire : ", l)
        if len(l) == 0:  # pas de prise oblig détectée alors le joueur est libre de cliquer (1er click)
            # sur n'importe laquelle de ses pièces
            if (self.player == 1 and self.matrice_jeu[i][j] in (1, 11)) or \
                    (self.player == 2 and self.matrice_jeu[i][j] in (2, 12)):
                boule = True
        elif (i, j) in l:  # le joueur doit prendre un ou des pions adverses
            boule = True
        print("boule ds firstclickok", boule)
        return boule

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
                g.append((i,j))
                self.plusLongueCapture(Position(i, j)) ; print("appel de plusLongueCapture")
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

    def secondClickOk(self, pos_depart, pos_arrivee):
        boule = self.posLibre(pos_arrivee)
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

    def posVoisinesChef(self, pos):
        l = []
        long_chemin = len(CHEMIN)
        i = CHEMIN.index((pos.x, pos.y))
        if i - 1 >= 0: l.append(CHEMIN[i - 1])
        if i + 1 <= long_chemin - 1: l.append(CHEMIN[i + 1])
        return l

    def jouer(self, i, j):
        print("firstClickOK :", self.firstClickOk(i, j))
        print("click = ", self.click)
        if self.click == 0 and self.firstClickOk(i, j):  # 1er click du joueur qui a la main
            self.click = 1
            self.pos_depart = Position(i, j)
            # self.plusLongueCapture(self.pos_depart)
        elif self.click == 1:  # nb : (i, j) est la position arrivee car second click de l'utilisateur
            self.click = 0
            pos_arrivee = Position(i, j)  # affectation ajoutée pour rendre le code plus lisible
            if self.secondClickOk(self.pos_depart, pos_arrivee):
                self.movePion(self.pos_depart, pos_arrivee)
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


   # def existeCaptureObligatoire2(self, pos):
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
    #         voisinsAdversaire = Position(i, j)
    #         l = self.posVoisinesPion(voisinsAdversaire)  # positions voisines du ou des adversaires
    #         for (i, j) in l:
    #             if self.matrice_jeu[i, j] == 0: boule = True
    #     return boule