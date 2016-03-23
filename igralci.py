from tkinter import*
from tabla import*
from crnobelo import*

import logging
import random
import threading




#####################################################################
## Racunalnik

class Racunalnik():
    def __init__(self, CRNOBELO, algoritem):
        self.CRNOBELO = CRNOBELO
        self.algoritem = algoritem # Algoritem, ki izracuna potezo
        self.mislec = None # Vlakno (thread), ki razmislja

    def igraj(self):
        """Igraj potezo, ki jo vrne algoritem."""
        # Tu sprozimo vzporedno vlakno, ki racuna potezo. Ker tkinter ne deluje,
        # ce vzporedno vlakno direktno uporablja tkinter (glej http://effbot.org/zone/tkinter-threads.htm),
        # zadeve organiziramo takole:
        # - pozenemo vlakno, ki poisce potezo
        # - to vlakno nekam zapise potezo, ki jo je naslo
        # - glavno vlakno, ki sme uporabljati tkinter, vsakih 100ms pogleda, ali
        #   je ze bila najdena poteza (metoda preveri_potezo spodaj).
        # Ta resitev je precej amaterska. Z resno knjiznico za GUI bi zadeve lahko
        # naredili bolje (vlakno bi samo sporocilo GUI-ju, da je treba narediti potezo).

        # Naredimo vlakno, ki mu podamo *kopijo* igre (da ne bo zmedel GUIja):
        # logging.debug("Velikost: {0}".format(self.CRNOBELO.igra.kopija()))
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(self.CRNOBELO.igra.kopija()))

        # Pozenemo vlakno:
        self.mislec.start()

        # Gremo preverjat, ali je bila najdena poteza:
        self.CRNOBELO.canvas.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        """Vsakih 100ms preveri, ali je algoritem ze izracunal potezo."""
        if self.algoritem.poteza is not None:
            # Algoritem je nasel potezo, povleci jo, ce ni bilo prekinitve
            self.CRNOBELO.izberi(self.algoritem.poteza)
            # Vzporedno vlakno ni vec aktivno, zato ga "pozabimo"
            self.mislec = None
        else:
            # Algoritem se ni nasel poteze, preveri se enkrat cez 100ms
            self.CRNOBELO.canvas.after(100, self.preveri_potezo)

    def prekini(self):
        # To metodo klice GUI, ce je treba prekiniti razmisljanje.
        if self.mislec:
            logging.debug ("Prekinjamo {0}".format(self.mislec))
            # Algoritmu sporocimo, da mora nehati z razmisljanjem
            self.algoritem.prekini()
            # Pocakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Racunalnik ignorira klike
        pass

######################################################################
## Algoritem minimax

class Minimax():
    def __init__(self, globina):
        self.prekiitev = False
        self.igra = None
        self.jaz = None
        self.poteza = None
        self.globina = globina

    def prekini(self):
        self.prekinitev = True


    def vrednost_pozicije(self):
        pass


    def izracunaj_potezo(self, igra):
        logging.debug("Igra minimax")
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_vrsti
        self.poteza = None
        poteza, vrednost = self.minimax()

        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def minimax(self):
        do_kdaj = False
        while not do_kdaj:
            x =  random.randint(0, (len(self.igra.matrika)) - 1)
            y =  random.randint(0, (len(self.igra.matrika)) - 1)
            logging.debug("{0},{1}".format(x,y))
            do_kdaj = self.igra.dovoljeno(x,y)

        return ((x,y), None)

    def prestej_L(self):
        stevilo = 0
        sez_L = []
        sez_dovoljenih = self.igra.veljavne_poteze()
        for i in sez_dovoljenih:
            if self.igra.preveri_L(i) != 0:
                sez_L.append((i, self.igra.preveri_l(i)))
                stevilo += self.igra.preveri_l(i)

        return stevilo

    def prestej_zavzeta_polja(self):
        steviloA = 0
        steviloB = 0
        a = self.igra.veljavne_poteze()
        b = []
        if self.igra.na_vrsti == JAZ:
            self.igra.na_vrsti = ON
            b = self.igra.veljavne_poteze()
            self.igra.na_vrsti = JAZ
        else:
            self.igra.na_vrsti = JAZ
            b = self.igra.veljavne_poteze()
            self.igra.na_vrsti = ON

        for i in a:
            if i not in b:
                steviloA += 1

        for j in b:
            if j not in a:
                steviloB += 1

        return (steviloA,steviloB)



######################################################################
## Igralec alfabeta

class alfabeta():
    def __init__(self):
        # Dodaj se globino.
        self.prekiitev = False
        self.igra = None
        self.jaz = None
        self.poteza = None

    def prekini(self):
        self.prekinitev = True


    def vrednost_pozicije(self):
        pass


    def izracunaj_potezo(self, igra):
        logging.debug("Igra alfabeta")
        self.igra = igra
        self.prekinitev = False
        self.jaz = self.igra.na_vrsti
        self.poteza = None
        poteza = self.alfabeta(igra)

        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def alfabeta(self, igra):
        do_kdaj = False
        while not do_kdaj:
            x =  random.randint(0, (len(self.igra.matrika)) - 1)
            y =  random.randint(0, (len(self.igra.matrika)) - 1)
            logging.debug("{0},{1}".format(x,y))
            do_kdaj = self.igra.dovoljeno(x,y)

        return (x,y)

######################################################################
## Igralec clovek

class clovek():
    def __init__(self, CRNOBELO):
        self.CRNOBELO = CRNOBELO

    def igraj(self):
        # Smo na potezi. Zaenkrat ne naredimo nic, ampak
        # cakamo, da bo uporanik kliknil na plosco. Ko se
        # bo to zgodilo, nas bo Gui obvestil preko metode
        # klik.
        logging.debug("Igra clovek")
        pass

    def prekini(self):
        # To metodo klice GUI, ce je treba prekiniti razmisljanje.
        # Clovek jo lahko ignorira.
        pass

    def klik(self, event):
        # Povlecemo potezo. Ce ni veljavna, se ne bo zgodilo nic.
        x, y = (event.x - 50) // 100, (event.y - 50) // 100
        if x >= 0 and y >= 0 and x < self.CRNOBELO.velikost and y <self.CRNOBELO.velikost:
            self.CRNOBELO.izberi((x,y))

