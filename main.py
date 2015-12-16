__author__ = 'IENAC15 - groupe 25'
#! /usr/bin/python
#-*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication

import vue
import sys
from model import load_jeu, DATA

jeu = load_jeu(DATA + "init_jeu.txt")
# for pion in jeu:
#      print(pion)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    f = vue.fenPrincipale()  # crée la fenetre, le plateau et le pavage du plateau par des boutons tranparents
    f.draw_pions(jeu) # trace les pions
    f.show()
    sys.exit(app.exec_())