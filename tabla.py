from tkinter import*
from crnobelo import*
from igralci import*

import logging
import copy


PRAZNO = 0
JAZ = "Beli"
ON = "Crni"
VELIKOST = 5


## Igra

class tabla():
    def __init__(self, crnobelo):
        # crnobelo rabimo, ker klicemo self.velikost
        self.crnobelo = crnobelo
        self.matrika = [[[True, True, None] for _ in range(self.crnobelo.velikost)] for _ in range(self.crnobelo.velikost)]
        self.na_vrsti = JAZ
        self.konec = False
        logging.debug("Velikost(27): {0}.".format(self.crnobelo.velikost))

    # Funkcija, ki preveri, ce je poteza dovoljena.
    def dovoljeno(self, x, y):
        if self.na_vrsti == JAZ and self.matrika[y][x][0]:
            return True
        elif self.na_vrsti == ON and self.matrika[y][x][1]:
            return True
        else:
            return False

    # Funkcija,ki pove, ce je igre konec.
    def konec_igre(self):
        if self.na_vrsti == JAZ:
            n = 0
        else:
            n = 1

        for i in range(self.crnobelo.velikost):
            for j in range(self.crnobelo.velikost):
                 if self.matrika[i][j][n]:
                     return False

        return True

    # Funkcija, ki skopira tablo.
    def kopija(self, CRNOBELO):
        logging.debug("Kopiram...")
        k = tabla(CRNOBELO)
        k.matrika = copy.deepcopy(self.matrika)

        # k.matrika = [[[True, True, None] for _ in range(l)] for _ in range(l)]
        # for i in range(l):
        #     for j in range(l):
        #         k.matrika[i][j] = self.matrika[i][j]

        k.na_vrsti = self.na_vrsti
        k.konec = self.konec
        return k
