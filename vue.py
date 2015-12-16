__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python3
# -*-coding: utf-8 -*-


from model import DATA
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMainWindow, qApp, QPushButton
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


class fenPrincipale(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        winSize = min(QDesktopWidget().height(), QDesktopWidget().width())  # dim fenetre vs écran
        self.resize(RATIO * winSize, RATIO * winSize)
        # self.setFixedSize(RATIO * winSize, RATIO * winSize)
        self.centrerSurEcran()
        self.initMenu()

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
        centralWidget.setGeometry(0, 0, TAILLE_FEN, TAILLE_FEN)
        centralWidget.setStyleSheet("background-color:rgba(255,255,255,255);")
        plateau = Plateau()
        plateau.setParent(centralWidget)
        plateau.setGeometry(MARGE, MARGE, PLATEAUSIZE, PLATEAUSIZE)
        self.btn = {} # dico de boutons
        for i in range(0, N):
            for j in range(0, N):
                button = Button(i, j)
                button.setParent(centralWidget)
                button.setObjectName("b_" + str(i) + "_" + str(j))
                button.setGeometry(QRect(DECALAGE + TAILLE_CASE * i, DECALAGE + TAILLE_CASE * j, TAILLE_BTN, TAILLE_BTN))
                button.setFlat(True)
                button.setStyleSheet("background-color: rgba(255,255,255,0) ;")
                button.setIconSize(QSize(64, 64))
                button.setToolTip(str(i) + str(j))
                self.btn[(i,j)] = button

    def centrerSurEcran(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def draw_pions(self, jeu):
        """
        :param jeu: type list contenant des types Pions
        :return:
        """
        for pion in jeu:
            icon = QIcon()
            icon.addPixmap(QPixmap(DATA + pion.image), QIcon.Normal, QIcon.Off)
            self.btn[(pion.i, pion.j)].setIcon(icon)


class Plateau(QWidget):
    def __init__(self):
        super().__init__()
        self.chemin = [(4, 0), (5, 1), (5, 3), (6, 4), (7, 3), (7, 4), \
                       (8, 4), (7, 5), (8, 6), (7, 6), (7, 7), (6, 6), \
                       (5, 7), (5, 6), (4, 6), (5, 5), (4, 4), (3, 3), \
                       (4, 2), (3, 2), (3, 1), (2, 2), (1, 1), (1, 2), \
                       (0, 2), (1, 3), (0, 4), (1, 4), (1, 5), (2, 4), \
                       (3, 5), (3, 7), (4, 8)]


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
        for pt in self.chemin:
            l.append(QPoint( pt[0] * TAILLE_CASE, pt[1] * TAILLE_CASE))
            poly = QPolygon(l)
        qp.drawPolyline(poly)
        qp.setBrush(PATH_COLOR)
        a = TAILLE_CASE / 5
        b = a / 2
        qp.drawRect(4 * TAILLE_CASE - b, 4 * TAILLE_CASE - b, a, a)


class Button(QPushButton):
    def __init__(self, i, j):
        super().__init__()
        self.i = i
        self.j = j













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
