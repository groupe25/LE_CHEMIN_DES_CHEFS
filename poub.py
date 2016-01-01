from model import Position


l = [(4, 0), (5, 1), (5, 2), (5, 3), (6, 4), (7, 3),
          (7, 4), (8, 4), (7, 5), (8, 6), (7, 6), (7, 7),
          (6, 6), (5, 7), (5, 6), (4, 6), (5, 5), (4, 4),
          (3, 3), (4, 2), (3, 2), (3, 1), (2, 2), (1, 1),
          (1, 2), (0, 2), (1, 3), (0, 4), (1, 4), (1, 5),
          (2, 4), (3, 5), (3, 6), (3, 7), (4, 8)]
g=[]

for (i,j) in l:
    g.append(Position(i,j))




pos = Position(i, j)
print("avant : ", pos)
if pos in g:pass

print("après : ", pos)




   # def existePosVoisineLibre(self, pos):
   #      """
   #      indique si autour de pos, il y a au moins une position libre = 0
   #      A utiliser pour déterminer si un pion adverse est prenable car il existe une pos vide voisine
   #      :param pos: position d'un pion
   #      :return: boule un booléen = True s'il existe un pos vide
   #      """
   #      boule = False
   #      l = self.posVoisinesPion(pos)  # ici, la liste retournée élimine la case centrale 4 4
   #      # un pion soldat ne peut se positionner sur cette case mais a t il le droit de la "traverser"
   #      # dans le cas de prise multiple n'induisant pas un positionnement sur cette case ??????????
   #      for (i, j) in l:
   #          if self.matrice_jeu[i,j] == 0:
   #              boule = True ; break
   #      return boule


      #
      # def listePosPriseObligatoire(self):
      #   """
      #   Pour tous les pions du jeu on détermine la liste des positions
      #   sur lesquelles le joueur doit obligatoirement clicker : Pb : ici on ne tiens
      #   pas encore compte des prises multiples. si le joeur adverse joue et provoque
      #   en un coup l'appartition de plusieurs possiblités de prises, c'est la plus longue qui
      #   doit être prise en considération. MEME PB RECURSIF que pour traiter la validité du second click
      #
      #   :return: liste des positions des pions du joueur courant qui doivent qui peuvent/doivent prendre
      #   au moins un pion adverse.
      #   """
      #   l = []
      #   for i in range(N):
      #       for j in range(N):
      #           pos = Position(i, j)
      #           if self.matrice_jeu[i, j] == self.player and self.existeCaptureObligatoire(pos):
      #               # par exemple si player=1 on ne considère que les pos avec des pions1 qui ont un voisin qui est un adversaire "capturable"
      #               l.append((i, j))
      #   return l
