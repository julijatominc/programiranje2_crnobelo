from tkinter import*
from tkinter import filedialog
from Tabla import*
from Igralci import*
import ast
import argparse
import logging
import re
import csv
try: import winsound
except: pass



BELI = "Beli"
CRNI = "Crni"
VELIKOST = 6
MINIMAX_GLOBINA = 2
ALFABETA_GLOBINA = 2


class Crnobelo():
    # Ustvarimo tag, da se bomo lahko kasneje sklicevali.
    TAG_KROG = 'krog'
    TAG_POTEZA = 'poteza'
    TAG_NAMIG = 'namig'


    def __init__(self, master, velikost=VELIKOST):
        self.BELI = None
        self.CRNI = None
        self.igra = None
        self.zvocnik = True
        self.NAMIG = False

        # Ustvarimo napis, ki nas obvesca o dogajanju.
        self.napis = StringVar()
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        self.napis2 = StringVar()
        Label(master, textvariable=self.napis2).grid(row=1, column=0)
    
        
        # Definira vrednosti.
        self.velikost = velikost
        self.canvas = Canvas(master, width=100*(self.velikost+1), height=100*(self.velikost +1), bg = "white")
        self.canvas.grid(row=2, column=0)

        # Na canvas narise zacetno polje.
        self.narisi()

        # Povezemo klik z dogodkom
        self.canvas.bind("<Button-1>", self.plosca_klik)
        
        # Gumb za namig
        b = Button(master, text="Namig", command = lambda: self.pobarvaj_namig()).grid(row = 3, column = 0)

    
        # Glavni menu.
        menu = Menu(master)
        master.config(menu=menu)

        # Dodamo moznosti v menu.
        file_menu = Menu(menu)
        menu.add_cascade(label="Datoteka", menu=file_menu)
        file_menu.add_command(label="Nova igra", command=self.nova_igra)
        file_menu.add_command(label="Shrani", command=self.shrani)
        file_menu.add_command(label="Odpri", command=self.odpri)
        file_menu.add_separator()
        file_menu.add_command(label="Izhod", command=master.destroy)

        settings_menu = Menu(menu)
        menu.add_cascade(label="Velikost", menu=settings_menu)
        settings_menu.add_command(label="5x5", command= lambda: self.nova_igra(None, None, 5))
        settings_menu.add_command(label="6x6", command= lambda: self.nova_igra(None, None, 6))
        settings_menu.add_command(label="7x7", command= lambda: self.nova_igra(None, None, 7))
        settings_menu.add_command(label="8x8", command= lambda: self.nova_igra(None, None, 8))
        settings_menu.add_command(label="9x9", command= lambda: self.nova_igra(None, None, 9))

        settings_menu = Menu(menu)
        menu.add_cascade(label="Igralci", menu=settings_menu)
        submenu = Menu(menu)
        settings_menu.add_command(label="Clovek - Clovek", command= lambda: self.nova_igra(Clovek(self), Clovek(self), None))
        settings_menu.add_cascade(label='Racunalnik', menu=submenu, underline = 0)

        
        submenu.add_command(label="Clovek - Random", command= lambda: self.nova_igra(Clovek(self), Racunalnik(self, Nakljucje()), None))
        submenu.add_command(label="Clovek - Racunalnik Minimax", command= lambda: self.nova_igra(Clovek(self), Racunalnik(self, Minimax(MINIMAX_GLOBINA )), None))
        submenu.add_command(label="Clovek - Racunalnik Alfa-beta", command= lambda: self.nova_igra(Clovek(self), Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), None))
        submenu.add_command(label="Racunalnik Minimax - Racunalnik Alfa-beta", command= lambda: self.nova_igra(Racunalnik(self, Minimax(MINIMAX_GLOBINA)), Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), None))
        submenu.add_command(label="Racunalnik Alfa-beta - Racunalnik Alfa-beta", command= lambda: self.nova_igra(Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)), None))

        settings_menu = Menu(menu)
        menu.add_cascade(label="Zvok", menu=settings_menu)
        settings_menu.add_command(label="Vklopi zvok", command = lambda: self.zvok(True))
        settings_menu.add_command(label="Izklopi zvok", command = lambda: self.zvok(False))
        settings_menu.add_command(label="Vzami nazaj", command = self.vzami_nazaj())


        menu.add_command(label="Pomoc")



        # logging.debug("Velikost: {0}.".format(self.velikost)),
        self.zacni_igro()

    # Funkcija za risanje sahovnice.
    def narisi(self):
        for i in range(self.velikost+1):
            self.canvas.create_line((50+i*100*6/(self.velikost)),50,(50+i*100*6/(self.velikost)),650)
            self.canvas.create_line(50,(50+i*100*6/(self.velikost)),650,(50+i*100*6/(self.velikost)))

    # Funkcija, ki zacne igro.
    def zacni_igro(self, beli=None, crni=None):
        if not beli:
            beli = Clovek(self)
        if not crni:
            crni = Clovek(self)

        logging.debug("Beli:{0}, Crni:{1}".format(beli,crni))
        self.igra = Tabla(self.velikost)
        self.nova_igra(beli, crni)

    # Funkcija, ki ustvari novo igro.
    def nova_igra(self, beli=None, crni=None, velikost=None):
        self.canvas.delete(Crnobelo.TAG_POTEZA)
        logging.debug("Nova igra")
        self.prekini_igralce()

        if  velikost:
            self.velikost = velikost
            self.canvas.delete("all")
            self.narisi()
        else:
            self.canvas.delete(Crnobelo.TAG_KROG)

        if beli and crni:
            self.BELI = beli
            self.CRNI = crni

        else:
            self.BELI, self.CRNI = self.CRNI, self.BELI

        # logging.debug("Velikost: {0}.".format(self.velikost))

        #Ustvarimo matriko z zacetnimi vrednostmi
        self.igra.matrika = [[[True, True, None] for _ in  range(self.velikost)] for _ in range(self.velikost)]

        
        self.napis.set("")

        self.igra.na_vrsti = BELI
        logging.debug("Na vrsti:{0}".format(self.igra.na_vrsti))

        logging.debug("Beli: {0}, Crni: {1}".format(self.BELI, self.CRNI))
        
        self.napis2.set("Na vrsti je beli.")

        #Zacnemo igro
        self.BELI.igraj()

    # Funkcija, ki preda dogodek na plosci razredu igralca, ki je storil to potezo
    def plosca_klik(self, event):
        if self.igra.na_vrsti == BELI:
            self.BELI.klik(event)
        elif self.igra.na_vrsti == CRNI:
            self.CRNI.klik(event)
        else:
            pass

    # Funkcija, ki glede na igralca na vrsti in na njegovo dejanje naredi potezo
    def izberi(self, xy):
        x = xy[0]
        y = xy[1]
        # Preveri, ce je konec igre. V primeru, da je konec, nocemo vec dogajanja na plosci.
        #logging.debug("Preverim, ce je konec igre.")
        if not self.igra.je_konec():
            if self.NAMIG:
                self.canvas.create_rectangle((x * 100* 6/(self.velikost)+ 50), (y *100* 6/(self.velikost)+ 50), (x * 100* 6/(self.velikost)+ 50+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50+100*6/(self.velikost)), fill="red", tag=Crnobelo.TAG_NAMIG)
                self.NAMIG = False
            else:
                self.napis.set("")
                poteza = self.igra.povleci_potezo(xy)
                
                #Poteza je neveljavna. Poskusimo ponovno
                if poteza is None:
                    self.napis.set("Neveljavna poteza!")
                    if self.igra.na_vrsti == BELI:
                        self.BELI.igraj()
                    elif self.igra.na_vrsti == CRNI:
                        self.CRNI.igraj()
                    else:
                        assert False
                #Poteza je veljavna.
                else:
                    if self.igra.na_vrsti == CRNI:
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "white", tag=Crnobelo.TAG_KROG)
                        self.napis2.set("Na vrsti je crni.")
                        
                    else:
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "black", tag=Crnobelo.TAG_KROG)
                        self.napis2.set("Na vrsti je beli.")

                    #Ob odigrani potezi: beep!
                    if self.zvocnik:
                        try: winsound.Beep(150, 75)
                        except: pass
                        
                    #Ce je igre konec.
                    if self.igra.je_konec():
                        self.igra.na_vrsti = nasprotnik(self.igra.na_vrsti)
                        self.napis2.set("")
                        self.napis.set("Konec igre! Zmagal je {0}!".format(self.igra.na_vrsti))
                        if self.zvocnik:
                            try: winsound.Beep(500, 150)
                            except: pass
                           #winsound.PlaySound("tara", winsound.SND_ALIAS)

                    #Igre ni konec, nadaljujemo.
                    else:

                        if self.igra.na_vrsti == BELI:
                            self.BELI.igraj()
                        elif self.igra.na_vrsti == CRNI:
                            self.CRNI.igraj()
                        else:
                            assert False

        #logging.debug("{0}".format(self.igra.veljavne_poteze()))

    #pokliče funkcijo izberi z alfabeta in poarva namig
    def pobarvaj_namig(self):
        self.NAMIG = True
        if self.igra.na_vrsti == BELI:
            nasprotnik = self.CRNI
            self.CRNI = Racunalnik(self, Alfabeta(ALFABETA_GLOBINA))
            self.CRNI.igraj()
            self.CRNI = nasprotnik
            self.BELI.igraj()
        elif self.igra.na_vrsti == CRNI:
            nasprotnik = self.BELI
            self.BELI = Racunalnik(self, Alfabeta(ALFABETA_GLOBINA))
            self.BELI.igraj()
            self.BELI = nasprotnik
            self.CRNI.igraj()
            
        #namig deluje, če ga pokliče človek
        else:
            self.NAMIG = False
            pass
        
    # Na canvasu pobarva veljavne poteze.  
    def pobarvaj_poteze(self):
        poteze = self.igra.veljavne_poteze()
        for i in poteze:
            x, y = i
            self.canvas.create_rectangle((x * 100* 6/(self.velikost)+ 50), (y *100* 6/(self.velikost)+ 50), (x * 100* 6/(self.velikost)+ 50+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50+100*6/(self.velikost)), fill="grey90", tag=Crnobelo.TAG_POTEZA)

    # Pobrise veljave poteze.
    def pobrisi_poteze(self):
        self.canvas.delete(Crnobelo.TAG_POTEZA)

    # Funkcija, ki shrani igro v datoteko.
    def shrani(self):
        self.prekini_igralce()

        beli = (re.findall(r'\.(.+?)\s', str(self.BELI))[0]).lower()
        crni = (re.findall(r'\.(.+?)\s', str(self.CRNI))[0]).lower()

        ime = filedialog.asksaveasfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")), defaultextension=".txt")
        if ime == "":
            return
        with open(ime, "wt", encoding="utf8") as f:
            print(self.igra.matrika, file=f)
            print(self.igra.na_vrsti, file=f)
            print(beli, file=f)
            print(crni, file=f)
            print(str(self.igra.st_potez), file=f)

    # Funkcija, ki nalozi igro iz datoteke.
    def odpri(self):
        ime = filedialog.askopenfilename(filetypes =(("Text File", "*.txt"),("All Files","*.*")))
        s = open(ime, encoding="utf8")
        sez = s.readlines()
        s.close


        KDO = sez[1].strip()
        beli = sez[2].strip()
        crni = sez[3].strip()
        velikost = len(ast.literal_eval(sez[0].strip()))
        stevilo = int(sez[4].strip())



        if str(beli) == "clovek":
            beli = Clovek(self)
        else:
            beli =  Racunalnik(self, Alfabeta(ALFABETA_GLOBINA))


        if str(crni) == "clovek":
            crni = Clovek(self)
        else:
            crni =  Racunalnik(self, Alfabeta(ALFABETA_GLOBINA))

        self.nova_igra(beli, crni, velikost)
        self.prekini_igralce()
        self.napis.set("")
        self.igra.matrika = ast.literal_eval(sez[0].strip())
        self.igra.st_potez = stevilo

        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.igra.matrika[j][i][2] == "Beli":
                    self.canvas.create_oval((i * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (j *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (i * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (j *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "white", tag=Crnobelo.TAG_KROG)
                if self.igra.matrika[j][i][2] == "Crni":
                    self.canvas.create_oval((i * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (j *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (i * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (j *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "black", tag=Crnobelo.TAG_KROG)


        if KDO == "Beli":
            self.igra.na_vrsti = BELI
            self.BELI.igraj()
            self.napis2.set("Na potezi je beli.")
        else:
            self.igra.na_vrsti = CRNI
            self.CRNI.igraj()
            self.napis2.set("Na potezi je crni.")


    def zvok(self, bool):
        if not bool:
            self.zvocnik = False


    # Funkcija, ki prekine igralce
    def prekini_igralce(self):
        if self.BELI:
            self.BELI.prekini()
        if self.CRNI:
            self.CRNI.prekini()

    # Funkcija, ki vzame potezo nazaj
    def vzami_nazaj(self):
        pass
##
##    def pobarvaj_namig(self):
##        poteza = self.BELI.igraj()[0]
##
##        elif self.CRNI:
##            return self.Crnobelo.CRNI.igraj()[]
##        assert False

######################################################################
## Glavni program

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Igrica Crnobelo")

    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporocila o dogajanju')
    
    parser.add_argument('--globinaM',
                        default=MINIMAX_GLOBINA,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    
    parser.add_argument('--globinaAB',
                        default=ALFABETA_GLOBINA,
                        type=int,
                        help='globina iskanja za alfabeta algoritem')
    

    
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)



    # Naredimo glavno okno in nastavimo ime
    root = Tk()
    root.title("Crnobelo")
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    aplikacija = Crnobelo(root)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
