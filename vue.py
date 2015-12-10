__author__ = 'IENAC15 - groupe 25'
#! /usr/bin/python3
#-*-coding: utf-8 -*-


# from PyQt5.QtWidgets import *


import sys
sys.path.insert(0, sys.path[0] + "/data/")
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QGraphicsEllipseItem, QMainWindow, QGraphicsScene,QGraphicsView, \
    qApp
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygon, QIcon
from PyQt5.QtCore import Qt, QPoint

N = 9 # 9 intersections  donc 8 cases
RATIO = 0.9 # ratio d'occupation de la fenêtre vis à vis de l'écran
PLATEAUSIZE = 800
PATH_COLOR = QColor(0, 50, 250)
RED = QColor(255, 0, 0)
GREEN = QColor(0,255,0)


class fenPrincipale(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        winSize = min(QDesktopWidget().height(),QDesktopWidget().width()) # dim fenetre vs écran
        self.resize(RATIO * winSize, RATIO * winSize)
        # self.setFixedSize(RATIO * winSize, RATIO * winSize)
        self.centrerSurEcran()
        self.initMenu()
        self.show()


    def initMenu(self):
        self.setWindowTitle('Le chemin des chefs')
        self.setWindowIcon(QIcon(sys.path[0] + 'general.png'))
        menuFichier = self.menuBar().addMenu("&Fichier")
        # menuEdition = self.menuBar().addMenu("&Edition")
        # menuAffichage = self.menuBar().addMenu("&Affichage")
        actionNouvellePartie = menuFichier.addAction("&Nouvelle partie")
        actionNouvellePartie.setShortcut("Ctrl+N")
        actionNouvellePartie.setIcon(QIcon(sys.path[0] + 'general.png'))
        actionChargerPartie= menuFichier.addAction("&Charger une partie")
        actionChargerPartie.setShortcut("Ctrl+C")
        actionEnregistrerPartie = menuFichier.addAction("&Enregistrer la partie")
        actionEnregistrerPartie.setShortcut("Ctrl+E")
        actionQuitter = menuFichier.addAction("&Quitter")
        actionQuitter.setIcon(QIcon(sys.path[0] + "exit.png"))
        print(sys.path[0])
        actionQuitter.setShortcut("Ctrl+Q")
        actionQuitter.setStatusTip('Exit application')
        actionQuitter.triggered.connect(qApp.quit)
        self.statusBar()
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(actionQuitter)
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        centralWidget.setParent(self)
        centralWidget.setGeometry(0,0,1000,1000)
        centralWidget.setStyleSheet("background-color:white;")
        plateau = Plateau()
        plateau.setParent(centralWidget)
        plateau.setGeometry(100,100,800,800)

    def centrerSurEcran(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class Plateau(QWidget):

    def __init__(self):
        super().__init__()
        # winSize = RATIO * QDesktopWidget().height()
        self.resize(PLATEAUSIZE, PLATEAUSIZE)
        # self.center()
        # self.setWindowTitle('Le chemin des chefs')
        # self.setStyleSheet("background-color:white;")
        # self.setWindowIcon(QIcon(sys.path[0] + 'general.png'))
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawPlateau(qp)
        qp.end()

    def drawPlateau(self, qp):
        # winSize = min(self.height(), self.width())
        # marge = winSize / 10
        marge = 0
        step = (PLATEAUSIZE - 2 * marge) / (N - 1) # taille d'une case
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        for i in range(0, N):
            qp.drawLine(marge + i * step, marge, marge + i * step, PLATEAUSIZE - marge)
            qp.drawLine(marge, marge + i * step, PLATEAUSIZE - marge, marge + i * step)
        pen = QPen(PATH_COLOR, 6, Qt.SolidLine)
        qp.setPen(pen)
        chemin = self.chiefPath
        l = []
        for pt in chemin:
            l.append(QPoint(marge + pt[0] * step, marge + pt[1] * step))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = step / 5
        b = a / 2
        qp.drawRect(marge + 4 * step - b, marge + 4 * step - b, a, a)



    @property
    def chiefPath(self):
        ''' calcul of the chiefs path considering its symmetry
        :return:chiefs' path as a list ; top left corner position is (0, 0)
        '''
        chemin = [(4,0),(5,1), (5,3), (6,4),(7,3), \
                  (7,4),(8,4),(7,5),(8,6),(7,6),(7,7),\
                  (6,6),(5,7),(5,6),(4,6),(5,5), (4,4)]
        ch2 = []
        for pt in chemin:
            ch2.append((8 - pt[0], 8 - pt[1]))  # car le chemin est symétrique de centre (4,4)
        ch2.pop()
        ch2.reverse()
        return chemin + ch2


