__author__ = 'IENAC15 - groupe 25'
#! /usr/bin/python
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication

from vue import Window
import sys
from model import jeu_init,DATA

#jeu = load_jeu(DATA + "init_jeu.txt")
# for pion in jeu:
#      print(pion)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = Window()  # crée la fenetre, le plateau et le pavage du plateau par des boutons tranparents
    f.draw_pions(jeu_init) # trace les pions
    f.show()
    sys.exit(app.exec_())