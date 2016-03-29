from Igralci import *

import logging
import copy


# Vrne seznam s tremi centralnimi vrednostmi na prvih treh mestih
def cent_sez(sez):
    a = len(sez)//2
    seznam=[]
    seznam.append(sez[a])
    seznam.append(sez[a+1])
    seznam.append(sez[a-1])
    del sez[a-1]
    del sez[a-1]
    del sez[a-1]
    return seznam+sez


## Igra 
class Tabla():
    def __init__(self, velikost):
        self.matrika = [[[True, True, None] for _ in range(velikost)] for _ in range(velikost)]
        self.na_vrsti = BELI
        # logging.debug("Velikost(27): {0}.".format(velikost))
        self.zgodovina = []

    def velikost(self):
        return len(self.matrika)

    # Funkcija, ki preveri, ce je poteza dovoljena.
    def dovoljeno(self, x, y):
        if self.na_vrsti == BELI and self.matrika[y][x][0]:
            return True
        elif self.na_vrsti == CRNI and self.matrika[y][x][1]:
            return True
        else:
            return False

    # Funkcija,ki pove, ce je igre konec.
    def je_konec(self):
        return (len(self.veljavne_poteze()) == 0)

    # Funkcija, ki skopira tablo.
    def kopija(self):
        #logging.debug("Kopiram...")
        velikost = self.velikost()
        k = Tabla(velikost)
        for i in range(velikost):
            for j in range(velikost):
                k.matrika[i][j] = self.matrika[i][j][:]
        k.na_vrsti = self.na_vrsti
        return k
    
    # Shrani pozicijo v zgodovino.
    def shrani_pozicijo(self):
        #logging.debug("Shranjujem pozicijo...")
        p = copy.deepcopy(self.matrika)
        self.zgodovina.append((p, self.na_vrsti))
        #logging.debug("{0}".format(self.zgodovina))

    # Razveljavi potezo in se vrne v prejšnje stanje.
    def razveljavi(self):
        #logging.debug("Razveljavljam...")
        #logging.debug("{0}".format(self.zgodovina))
        (self.matrika, self.na_vrsti) = self.zgodovina.pop()

    # Seznam veljavnih potez.
    def veljavne_poteze(self):
        velikost = self.velikost()
        poteze = []
        seznam = cent_sez(list(range(0,velikost)))
        for i in seznam:
            for j in seznam:
                if self.dovoljeno(j,i):
                    poteze.append((j,i))
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

        #logging.debug("{0}".format(self.matrika))

    #Funkcija shrani potezo v matriko
    def povleci_potezo(self, p):
        (x, y) = p

        if not self.dovoljeno(x,y):
            return None

        else:
            self.shrani_pozicijo()
            if self.na_vrsti == BELI:
                self.spremeni_matriko(x, y, 1)
                self.na_vrsti = CRNI
            else:
                self.spremeni_matriko(x, y, 0)
                self.na_vrsti = BELI
            
            return True

