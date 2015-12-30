__author__ = 'IENAC15 - groupe 25'
# ! /usr/bin/python
# -*-coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication
from view import Window, initialise_jeu
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    initialise_jeu("init_jeu.txt")
    sys.exit(app.exec_())
