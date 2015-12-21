__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python3
# -*-coding: utf-8 -*-


from model import DATA, Jeu, CHEMIN
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow, qApp, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QSize



N = 9  # 9 intersections  donc 8 cases
RATIO = 0.9  # ratio d'occupation de la fenêtre vis à vis de l'écran
PLATEAUSIZE = 800
PATH_COLOR = QColor(0, 50, 250)
RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 0)
TAILLE_FEN = 1000
MARGE = TAILLE_FEN // 10 # marge fenêtre
TAILLE_CASE = TAILLE_FEN // 10
TAILLE_BTN = TAILLE_CASE
DECALAGE = TAILLE_CASE // 2
BLANC = "background-color:rgba(255,255,255,255);"
TRANSPARENT = "background-color: rgba(255,255,255,0) ;"


class Window(QMainWindow):
    def __init__(self, matrice_jeu):
        super(Window, self).__init__()
        self.image_pion = {1 : "pion1.png", 2 : "pion2.png", 11 : "chef1.png", 12 : "chef2.png", 0: ""}
        winSize = min(QDesktopWidget().height(), QDesktopWidget().width())  # dim fenetre vs écran
        self.resize(RATIO * winSize, RATIO * winSize)
        self.setWindowIcon(QIcon(DATA + "logo_enac.png"))
        # self.setFixedSize(RATIO * winSize, RATIO * winSize)
        self.centrerSurEcran()
        self.initMenu()
        self.jeu = Jeu(matrice_jeu)
        self.affichePlayerCourant(self.jeu.player, self.centralWidget())

    def initMenu(self):
        self.setWindowTitle('Le chemin des chefs - IENAC 15 - Groupe 25')
        self.setWindowIcon(QIcon(DATA + "logo_enac.png"))
        menuFichier = self.menuBar().addMenu("&Fichier")
        actionNouvellePartie = menuFichier.addAction("&Nouvelle partie")
        self.toolbar = self.addToolBar('')
        self.toolbar.addAction(actionNouvellePartie)
        actionNouvellePartie.setShortcut("Ctrl+N")
        actionNouvellePartie.setStatusTip('Nouvelle partie')
        actionNouvellePartie.setIcon(QIcon(DATA + "new.png"))
        actionChargerPartie = menuFichier.addAction("&Charger une partie")
        actionChargerPartie.setIcon(QIcon(DATA + "folder.png"))
        self.toolbar.addAction(actionChargerPartie)
        actionChargerPartie.setShortcut("Ctrl+C")
        actionChargerPartie.setStatusTip('Charger une partie')
        actionEnregistrerPartie = menuFichier.addAction("&Enregistrer la partie")
        actionEnregistrerPartie.setIcon(QIcon(DATA + "save.png"))
        self.toolbar.addAction(actionEnregistrerPartie)
        actionEnregistrerPartie.setShortcut("Ctrl+E")
        actionEnregistrerPartie.setStatusTip("Sauvegarder la partie")
        actionQuitter = menuFichier.addAction("&Quitter")
        actionQuitter.triggered.connect(qApp.quit)
        actionQuitter.setIcon(QIcon(DATA + "exit.png"))
        actionQuitter.setShortcut("Ctrl+Q")
        actionQuitter.setStatusTip('Quitter l\'application')
        self.statusBar()
        self.toolbar.addAction(actionQuitter)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.blockSignals(False)
        centralWidget.setParent(self)
        centralWidget.setGeometry(0, 0, TAILLE_FEN, TAILLE_FEN)
        centralWidget.setStyleSheet(BLANC)
        plateau = Plateau()
        plateau.setParent(centralWidget)
        plateau.setGeometry(MARGE, MARGE, PLATEAUSIZE, PLATEAUSIZE)

        self.btn = {} # dico des boutons qui effectuent un pavage, ou recouvrement, du plateau
        # chaque bouton symbolise une intersection dans la grille constituant le plateau de jeu.
        for i in range(0, N):
            for j in range(0, N):
                button = Button(self,i, j)
                button.setParent(centralWidget)
                # button.setObjectName("b_" + str(i) + "_" + str(j))
                button.setGeometry(QRect(DECALAGE + TAILLE_CASE * i, DECALAGE + TAILLE_CASE * j, TAILLE_BTN, TAILLE_BTN))
                button.setFlat(True)
                # button.setAcceptDrops(True)
                button.setStyleSheet(TRANSPARENT)
                button.setIconSize(QSize(64, 64))
                # button.setToolTip(str(i) +"_" + str(j))
                self.btn[(i,j)] = button

    def affichePlayerCourant(self, num_joueur, widgette_parent):
        """ Informe le joueur dont c'est le "tour" de jouer
        :param num_joueur: joueur 1 ou 2
        :param widgette_parent: widget contenant le QLabel
        :return:
        """
        aVousDeJouer = QLabel()
        aVousDeJouer.setParent(widgette_parent)
        txt = "A vous de jouer Joueur {} !!!!!".format(num_joueur)
        z = MARGE
        aVousDeJouer.setText(txt)
        x = PLATEAUSIZE / 2
        y = MARGE / 3 if num_joueur == 1 else TAILLE_FEN - MARGE / 2
        aVousDeJouer.setGeometry(x, y, 300, 20)

    def centrerSurEcran(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def draw_pions(self, mat_jeu):
        """
        :param jeu: type list contenant des types Pions
        :return:
        """
        for i in range(N):
            for j in range(N):
                icon = QIcon()
                # utilisation de la méthode get() de la classe python dictionnaire pour la fonctionnalité valeur par défaut
                icon.addPixmap(QPixmap(DATA + self.image_pion.get(mat_jeu[i][j], "")), QIcon.Normal, QIcon.Off)
                self.btn[(i,j)].setIcon(icon)


class Plateau(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlateau(qp)
        qp.end()

    def drawPlateau(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, N):
            qp.drawLine(i * TAILLE_CASE, 0, i * TAILLE_CASE, PLATEAUSIZE)
            qp.drawLine(0, i * TAILLE_CASE, PLATEAUSIZE, i * TAILLE_CASE)
        pen = QPen(PATH_COLOR, 6, Qt.SolidLine)
        qp.setPen(pen)
        l = []
        for pt in CHEMIN :
            l.append(QPoint( pt[0] * TAILLE_CASE, pt[1] * TAILLE_CASE))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = TAILLE_CASE / 5
        b = a / 2
        qp.drawRect(4 * TAILLE_CASE - b, 4 * TAILLE_CASE - b, a, a)



class Button(QPushButton):
    def __init__(self, win, i, j):
        super(Button, self).__init__()
        self.i = i
        self.j = j
        self.win = win

    def mousePressEvent(self, event):
        event.accept()
        print("souris pressed sur bouton : ", self.i, "  ", self.j)
        # self.
        self.win.jeu.jouer(self.i, self.j)
        self.win.draw_pions(self.win.jeu.matrice_jeu)

