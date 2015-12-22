__author__ = 'IENAC15 - groupe 25'
#! /usr/bin/python
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication
# from PyQt5.QtMultimedia import QSound
from view import Window, initialise_jeu
import sys
#from model import DATA, load_jeu



if __name__ == '__main__':
    app = QApplication(sys.argv)
    initialise_jeu("init_jeu.txt")
    # f = Window(matrice_jeu)  # crée la fenetre, le plateau et le pavage du plateau par des boutons transparents
    # f.draw_pions(matrice_jeu) # trace les pions
    # f.show()
    sys.exit(app.exec_())