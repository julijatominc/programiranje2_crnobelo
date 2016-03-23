from tkinter import*
from tabla import*
from igralci import*
import ast
import argparse
import logging


PRAZNO = 0
JAZ = "Beli"
ON = "Crni"
VELIKOST = 6
GLOBINA = 5


class crnobelo():
    # Ustvarimo tag, da se bomo lahko kasneje sklicevali.
    TAG_KROG = 'krog'


    def __init__(self, master, velikost=VELIKOST):
        self.JAZ = None
        self.ON = None
        self.igra = None

        # Ustvarimo napis, ki nas obvesca o dogajanju.
        self.napis = StringVar()
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Definira vrednosti.
        self.velikost = velikost
        self.canvas = Canvas(master, width=100*(self.velikost+1), height=100*(self.velikost +1))
        self.canvas.grid(row=1, column=0)

        # Na canvas narise zacetno polje.
        self.narisi()

        # Povezemo klik z dogodkom.
        self.canvas.bind("<Button-1>", self.plosca_klik)

    
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
        settings_menu.add_command(label="5", command= lambda: self.nova_igra(None, None, 5))
        settings_menu.add_command(label="6", command= lambda: self.nova_igra(None, None, 6))
        settings_menu.add_command(label="7", command= lambda: self.nova_igra(None, None, 7))
        settings_menu.add_command(label="8", command= lambda: self.nova_igra(None, None, 8))
        settings_menu.add_command(label="9", command= lambda: self.nova_igra(None, None, 9))

        settings_menu = Menu(menu)
        menu.add_cascade(label="Igralci", menu=settings_menu)
        settings_menu.add_command(label="Clovek-Clovek", command= lambda: self.nova_igra(clovek(self), clovek(self), None))
        settings_menu.add_command(label="Clovek-Racunalnik", command= lambda: self.nova_igra(clovek(self), Racunalnik(self, Minimax(GLOBINA)), None))
        settings_menu.add_command(label="Clovek-RacunalnikAB", command= lambda: self.nova_igra(clovek(self), Racunalnik(self, alfabeta()), None))
        settings_menu.add_command(label="Racunalnik-RacunalnikAB", command= lambda: self.nova_igra(Racunalnik(self, alfabeta()), Racunalnik(self, Minimax(GLOBINA)), None))
        settings_menu.add_command(label="Racunalnik-Racunalnik", command= lambda: self.nova_igra(Racunalnik(self, Minimax(GLOBINA)), Racunalnik(self, Minimax(GLOBINA)), None))
        settings_menu.add_command(label="RacunalnikAB-RacunalnikAB", command= lambda: self.nova_igra(Racunalnik(self, alfabeta()), Racunalnik(self, alfabeta()), None))

        settings_menu = Menu(menu)
        menu.add_cascade(label="Dodatno", menu=settings_menu)
        #settings_menu.add_command(label="Debug")
        settings_menu.add_command(label="Pomoc")

        # logging.debug("Velikost: {0}.".format(self.velikost)),
        self.zacni_igro()

    # Funkcija za risanje sahovnice.
    def narisi(self):
        for i in range(self.velikost+1):
            self.canvas.config(width=100*(self.velikost+1), height=100*(self.velikost +1))
            self.canvas.create_line(50, i*100 + 50,(self.velikost*100)+50,i*100 +50)
            self.canvas.create_line(i*100 +50, 50 , i*100 +50, (self.velikost*100) +50)

    # Funkcija, ki zacne igro.
    def zacni_igro(self, beli=None, crni=None):
        if not beli:
            beli = clovek(self)
        if not crni:
            crni = clovek(self)

        logging.debug("Beli:{0}, Crni:{1}".format(beli,crni))
        self.igra = tabla(self.velikost)
        self.nova_igra(beli, crni)

    # Funkcija, ki ustvari novo igro.
    def nova_igra(self, beli=None, crni=None, velikost=None):
        logging.debug("Nova igra")
        self.prekini_igralce()

        if  velikost:
            self.velikost = velikost
            self.canvas.delete("all")
            self.narisi()
        else:
            self.canvas.delete(crnobelo.TAG_KROG)

        if beli and crni:
            self.JAZ = beli
            self.ON = crni

        # logging.debug("Velikost: {0}.".format(self.velikost))

        self.igra.matrika = [[[True, True, None] for _ in  range(self.velikost)] for _ in range(self.velikost)]
        self.napis.set("")
        self.igra.na_vrsti = JAZ
        logging.debug("Na vrsti:{0}".format(self.igra.na_vrsti))

        logging.debug("Beli: {0}, Crni: {1}".format(self.JAZ, self.ON))
        
        
        self.JAZ.igraj()

    # Funkcija, ki preda dogodek na plosci razredu igralca, ki je storil to potezo
    def plosca_klik(self, event):
        if self.igra.na_vrsti == JAZ:
            self.JAZ.klik(event)
        elif self.igra.na_vrsti == ON:
            self.ON.klik(event)
        else:
            pass

    # Funkcija, ki glede na igralca na vrsti in na njegovo dejanje naredi potezo
    def izberi(self, xy):
        x = xy[0]
        y = xy[1]
        # Preveri, ce je konec igre. V primeru, da je konec, nocemo vec dogajanja na plosci.
        #logging.debug("Preverim, ce je konec igre.")
        if not self.igra.je_konec():
            self.napis.set("")
            poteza = self.igra.povleci_potezo(xy)
               
            if poteza is None:
                self.napis.set("Neveljavna poteza!")
                if self.igra.na_vrsti == JAZ:
                    self.JAZ.igraj()
                elif self.igra.na_vrsti == ON:
                    self.ON.igraj()
                else:
                    assert False
            else:
            
                if self.igra.na_vrsti == ON:
                    self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140, tag=crnobelo.TAG_KROG)
                    
                else:
                    self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140, fill="black", tag=crnobelo.TAG_KROG)

                if self.igra.je_konec():
                    if self.igra.na_vrsti == JAZ:
                        self.igra.na_vrsti = ON
                    else:
                        self.igra.na_vrsti = JAZ
                    self.napis.set("Konec igre! Zmagal je {0}!".format(self.igra.na_vrsti))

                else:

                    if self.igra.na_vrsti == JAZ:
                        self.JAZ.igraj()
                    elif self.igra.na_vrsti == ON:
                        self.ON.igraj()
                    else:
                        assert False

    # Funkcija, ki shrani igro v datoteko.
    def shrani(self):
        ime = filedialog.asksaveasfilename()
        if ime == "":
            return
        with open(ime, "wt", encoding="utf8") as f:
            print(self.igra.matrika, file=f)
            print(self.igra.na_vrsti, file=f)
            print(self.velikost, file=f)

    # Funkcija, ki nalozi igro iz datoteke.
    def odpri(self):
        ime = filedialog.askopenfilename()
        s = open(ime, encoding="utf8")
        sez = s.readlines()
        s.close

        self.igra.matrika = ast.literal_eval(sez[0].strip())
        KDO = sez[1].strip()
        velikost = sez[2].strip()

        self.nova_igra(velikost)

        if KDO == "Beli":
            self.igra.na_vrsti = JAZ
        else: self.igra.na_vrsti = ON

        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.matrika[i][j][2] == "Beli":
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j * 100 + 140)
                if self.igra.matrika[i][j][2] == "Crni":
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j* 100 + 140, fill="black")

    

    # Funkcija, ki prekine igralce
    def prekini_igralce(self):
        if self.JAZ:
            self.JAZ.prekini()
        if self.ON:
            self.ON.prekini()

######################################################################
## Glavni program

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Igrica Crnobelo")

    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporocila o dogajanju')

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Naredimo glavno okno in nastavimo ime
    root = Tk()
    root.title("Crnobelo")
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    aplikacija = crnobelo(root)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
