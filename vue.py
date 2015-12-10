__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python3
# -*-coding: utf-8 -*-


# from PyQt5.QtWidgets import *


import sys

sys.path.insert(0, sys.path[0] + "/data/")
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGraphicsEllipseItem, QMainWindow, QGraphicsScene, QGraphicsView, \
    qApp, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QIcon, QPixmap
from PyQt5.QtCore import Qt, QPoint, QRect, QSize

DATA = sys.path[0]
N = 9  # 9 intersections  donc 8 cases
RATIO = 0.9  # ratio d'occupation de la fenêtre vis à vis de l'écran
PLATEAUSIZE = 800
PATH_COLOR = QColor(0, 50, 250)
RED = QColor(255, 0, 0)
GREEN = QColor(0, 255, 0)


class fenPrincipale(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        winSize = min(QDesktopWidget().height(), QDesktopWidget().width())  # dim fenetre vs écran
        self.resize(RATIO * winSize, RATIO * winSize)
        # self.setFixedSize(RATIO * winSize, RATIO * winSize)
        self.centrerSurEcran()
        self.initMenu()
        self.show()

    def initMenu(self):
        self.setWindowTitle('Le chemin des chefs')
        self.setWindowIcon(QIcon(DATA + 'general.png'))
        menuFichier = self.menuBar().addMenu("&Fichier")
        # menuEdition = self.menuBar().addMenu("&Edition")
        # menuAffichage = self.menuBar().addMenu("&Affichage")
        actionNouvellePartie = menuFichier.addAction("&Nouvelle partie")
        actionNouvellePartie.setShortcut("Ctrl+N")
        actionNouvellePartie.setIcon(QIcon(DATA + 'general.png'))
        actionChargerPartie = menuFichier.addAction("&Charger une partie")
        actionChargerPartie.setShortcut("Ctrl+C")
        actionEnregistrerPartie = menuFichier.addAction("&Enregistrer la partie")
        actionEnregistrerPartie.setShortcut("Ctrl+E")
        actionQuitter = menuFichier.addAction("&Quitter")
        actionQuitter.setIcon(QIcon(DATA + "exit.png"))
        actionQuitter.setShortcut("Ctrl+Q")
        actionQuitter.setStatusTip('Exit application')
        actionQuitter.triggered.connect(qApp.quit)
        self.statusBar()
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(actionQuitter)
        self.setDockNestingEnabled(False)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setParent(self)
        centralWidget.setGeometry(0, 0, 1000, 1000)
        centralWidget.setStyleSheet("background-color:rgba(255,255,255,255);")
        plateau = Plateau()
        plateau.setParent(centralWidget)
        plateau.setGeometry(100, 100, 800, 800)
        pions = PionsLayout(centralWidget)
        pions.setParent(centralWidget)
        pions.setGeometry(100, 100, PLATEAUSIZE, PLATEAUSIZE)

    def centrerSurEcran(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Plateau(QWidget):
    def __init__(self):
        super().__init__()
        self.chemin = [(4, 0), (5, 1), (5, 3), (6, 4), (7, 3), (7, 4), \
                       (8, 4), (7, 5), (8, 6), (7, 6), (7, 7), (6, 6), \
                       (5, 7), (5, 6), (4, 6), (5, 5), (4, 4), (3, 3), \
                       (4, 2), (3, 2), (3, 1), (2, 2), (1, 1), (1, 2), \
                       (0, 2), (1, 3), (0, 4), (1, 4), (1, 5), (2, 4), \
                       (3, 5), (3, 7), (4, 8)]

        # winSize = RATIO * QDesktopWidget().height()
        # self.resize(PLATEAUSIZE, PLATEAUSIZE)
        # self.setGeometry(0,0,PLATEAUSIZE,PLATEAUSIZE)
        # self.center()
        # self.setWindowTitle('Le chemin des chefs')
        # self.setStyleSheet("background-color:white;")
        # self.setWindowIcon(QIcon(DATA + 'general.png'))
        # self.show()

    # def center(self):
    #     qr = self.frameGeometry()
    #     cp = QDesktopWidget().availableGeometry().center()
    #     qr.moveCenter(cp)
    #     self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlateau(qp)
        qp.end()

    def drawPlateau(self, qp):
        # winSize = min(self.height(), self.width())
        # marge = winSize / 10
        marge = 0
        step = (PLATEAUSIZE - 2 * marge) / (N - 1)  # taille d'une case
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, N):
            qp.drawLine(marge + i * step, marge, marge + i * step, PLATEAUSIZE - marge)
            qp.drawLine(marge, marge + i * step, PLATEAUSIZE - marge, marge + i * step)
        pen = QPen(PATH_COLOR, 6, Qt.SolidLine)
        qp.setPen(pen)
        l = []
        for pt in self.chemin:
            l.append(QPoint(marge + pt[0] * step, marge + pt[1] * step))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = step / 5
        b = a / 2
        qp.drawRect(marge + 4 * step - b, marge + 4 * step - b, a, a)


class PionsLayout(QWidget):
    def __init__(self, widgetConteneur):
        """
        i : abscisse donc indice de colonne
        j : ordonnée donc indice de ligne dans le repère
        d'origine top-left axe des x == i vers la droite, axe des y == j vers le bas
        :param widgetConteneur:
        :return:
        """
        super().__init__(widgetConteneur)
        for i in range(0, N):
            for j in range(0, N):
                if j < 2 :
                    image = "pion1.png"
                if i == 4 and j == 0:
                    image = "chef1.png"
                if 2 <= j <= 6 :
                    image = ""
                if j > 6 :
                    image = "pion2.png"
                if j == 8 and i == 4:
                    image = "chef2.png"

                self.name = "b_" + str(i) + "_" + str(j)
                self.name = QPushButton(widgetConteneur)
                self.name.setGeometry(QRect(50 + 100 * i, 50 + 100 * j, 100, 100))
                self.name.setStyleSheet("background-color: rgba(255,255,255,0) ;")
                self.name.setFlat(True)
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(DATA + image), QIcon.Normal, QIcon.Off)
                self.name.setIcon(icon1)
                self.name.setIconSize(QSize(64, 64))
                self.name.setObjectName("b_0_0")




        #
        # self.p_0_0 = QGraphicsEllipseItem()
        # self.p_0_0.setRect(0,0, 100, 100)
        # self.p_0_0.setBrush(QColor("red"))










        # # utilisée 1 fois pour produire le chemin complet
        # @property
        # def chiefPath(self):
        #     ''' calcul of the chiefs path considering its symmetry
        #     :return:chiefs' path as a list ; top left corner position is (0, 0)
        #     '''
        #     chemin = [(4,0),(5,1), (5,3), (6,4),(7,3), \
        #               (7,4),(8,4),(7,5),(8,6),(7,6),(7,7),\
        #               (6,6),(5,7),(5,6),(4,6),(5,5), (4,4)]
        #     ch2 = []
        #     for pt in chemin:
        #         ch2.append((8 - pt[0], 8 - pt[1]))  # car le chemin est symétrique de centre (4,4)
        #     ch2.pop()
        #     ch2.reverse()
        #     print(chemin + ch2)
        #     return chemin + ch2
