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
        # logging.debug("Velikost(27): {0}.".format(self.crnobelo.velikost))
        self.zgodovina = []

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
        if not self.veljavne_poteze():
            self.konec = True
            return True
        else:
            return False


    # Funkcija, ki skopira tablo.
    def kopija(self, CRNOBELO):
        logging.debug("Kopiram...")
        k = tabla(CRNOBELO)
        k.matrika = copy.deepcopy(self.matrika)
        k.na_vrsti = self.na_vrsti
        k.konec = self.konec
        return k
    
    # Shrani pozicijo v zgodovino.
    def shrani_pozicijo(self):
       p = copy.deepcopy(self.matrika)
       self.zgodovina.append((p, self.na_vrsti))

    # Razveljavi potezo in se vrne v prejšnje stanje.
    def razveljavi(self):
        (self.matrika, self.na_vrsti) = self.zgodovina.pop()

    # Seznam veljavnih potez.
    def veljavne_poteze(self):
        poteze = []
        for i in range(self.crnobelo.velikost):
            for j in range(self.crnobelo.velikost):
                if self.dovoljeno(j,i):
                    poteze.append((i,j))
        return poteze

    
    # Funkcija, ki potezo zapise v matriko in hkrati doloci katere poteze so mogoce.
    def spremeni_matriko(self, x, y, n):
        self.matrika[y][x][0] = False
        self.matrika[y][x][1] = False
        self.matrika[y][x][2] = self.na_vrsti

        if y-1 >= 0:
            self.matrika[y-1][x][n] = False
        else:
            pass

        try:
            self.matrika[y+1][x][n] = False
        except:
            pass

        if x-1 >= 0:
            self.matrika[y][x-1][n] = False
        else:
            pass

        try:
            self.matrika[y][x+1][n] = False
        except:
            pass 

    def povleci_potezo(self, p):
        (x, y) = p

        if not self.dovoljeno(x,y):
            return None

        else:
            self.shrani_pozicijo()
            if self.na_vrsti == JAZ:
                self.spremeni_matriko(x, y, 1)
                self.na_vrsti = ON
            else:
                self.spremeni_matriko(x, y, 0)
                self.na_vrsti = JAZ
            
            return True

    def preveri_L(self, xy):
        pass
        x, y = xy
        sez = [(x - 2, y - 1), (x - 2, y + 1),
               (x + 2, y - 1), (x + 2, y + 1),
               (x + 1, y - 2), (x - 1, y - 2),
               (x - 1, y + 2), (x + 1, y + 2)]
        
