from tkinter import*
import ast


######################################################################
## Zacetne nastavitve

PRAZNO = 0
JAZ = "Beli"
ON = "Crni"
VELIKOST = 5

######################################################################
## Igra

class tabla():
    def __init__(self):
        self.matrika = [[(True, True)] * self.velikost for _ in range(self.velikost)]
        self.na_vrsti = JAZ

        def dovoljeno(self, x, y):
            pass

        def konec_igre(self):
            pass

######################################################################
## Uporabniski vmesnik

class crnobelo():
    # Ustvarimo tag, da se bomo lahko kasneje sklicevali.
    TAG_KROG = 'krog'

    def __init__(self, master, velikost=VELIKOST):

        # Definira vrednosti.
        self.velikost = velikost
        self.canvas = Canvas(master, width=100*(self.velikost+1), height=100*(self.velikost +1))
        self.canvas.grid(row=1, column=0)

        # Na canvas narise zacetno polje.
        self.narisi()

        # Povezemo klik z dogodkom.
        self.canvas.bind("<Button-1>", self.izberi)

        # Ustvarimo napis, ki nas obvesca o dogajanju.
        self.napis = StringVar()
        label_napis = Label(master, textvariable=self.napis)
        label_napis.grid(row=0, column=0)

        # Glavni menu.
        menu = Menu(master)
        master.config(menu=menu)

        # Dodamo moznosti v menu.
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Nova igra", command=self.nova_igra)
        file_menu.add_command(label="Shrani", command=self.shrani)
        file_menu.add_command(label="Odpri", command=self.odpri)
        file_menu.add_separator()
        file_menu.add_command(label="Izhod", command=master.destroy)

        settings_menu = Menu(menu)
        menu.add_cascade(label="Velikost", menu=settings_menu)
        settings_menu.add_command(label="5", command= lambda: self.nova_igra(5))
        settings_menu.add_command(label="6", command= lambda: self.nova_igra(6))
        settings_menu.add_command(label="7", command= lambda: self.nova_igra(7))
        settings_menu.add_command(label="8", command= lambda: self.nova_igra(8))
        settings_menu.add_command(label="9", command= lambda: self.nova_igra(9))

    # Funkcija za risanje sahovnice.
    def narisi(self):
        for i in range(self.velikost+1):
            self.canvas.config(width=100*(self.velikost+1), height=100*(self.velikost +1))
            self.canvas.create_line(50, i*100 + 50,(self.velikost*100)+50,i*100 +50)
            self.canvas.create_line(i*100 +50, 50 , i*100 +50, (self.velikost*100) +50)

    # Funkcija, ki zacne igro.
    def zacni_igro(self):

        self.igra = tabla()
        self.nova_igra()

    # Funkcija, ki ustvari novo igro.
    def nova_igra(self, velikost=None):

        if  velikost:
            self.velikost = velikost
            self.canvas.delete("all")
            self.narisi()
        else:
            self.canvas.delete(crnobelo.TAG_KROG)

        self.matrika1 = [[(True, True)] * self.velikost for _ in range(self.velikost)]
        self.napis.set("")
        self.na_vrsti = JAZ

    # Funkcija, ki reagira na izbiro polja s strani uporabnika.
    def izberi(self, event):
        self.napis.set("")
        x, y = (event.x - 50) // 100, (event.y - 50) // 100
        # Preveri, ce je konec igre. V primeru, da je konec, nocemo vec dogajanja na plosci.
        if not self.konec_igre():
            # Preveri, ce je poteza dovoljena.
            if self.dovoljeno(x, y):
                if self.na_vrsti == JAZ:
                    # Spremeni matriko, v kateri imamo zapisano katere poteze so mozne.
                    self.spremeni_matriko(x, y, 1)
                    # Na potezi je nasprotnik.
                    self.na_vrsti = ON
                    # Narise krog.
                    self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140)
                else:
                    self.spremeni_matriko(x, y, 0)
                    self.na_vrsti = JAZ
                    self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140, fill="black")

                if self.konec_igre():
                    if self.na_vrsti == JAZ:
                        self.na_vrsti = ON
                    else:
                        self.na_vrsti = JAZ
                    self.napis.set("Konec igre! Zmagal je {0}!".format(self.na_vrsti))

            else:
                self.napis.set("Neveljavna poteza!")

    # Funkcija, ki shrani igro v datoteko.
    def shrani(self):
        ime = filedialog.asksaveasfilename()
        if ime == "":
            return
        with open(ime, "wt", encoding="utf8") as f:
            print(self.matrika1, file=f)
            print(self.na_vrsti, file=f)
            print(self.velikost, file=f)

    # Funkcija, ki nalozi igro iz datoteke.
    def odpri(self):
        ime = filedialog.askopenfilename()
        s = open(ime, encoding="utf8")
        sez = s.readlines()
        s.close

        self.matrika = ast.literal_eval(sez[0].strip())
        KDO = sez[1].strip()
        velikost = sez[2].strip()

        self.nova_igra(velikost)

        if KDO == str("Beli"):
            self.na_vrsti = JAZ
        else: self.na_vrsti = ON

        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.matrika[i][j][0]:
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j * 100 + 140)
                if self.matrika[i][j][1]:
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j* 100 + 140, fill="black")

    # Funkcija, ki potezo zapise v matriko in hkrati doloci katere poteze so mogoce.
    def spremeni_matriko(self, x, y, n):
        self.matrika[x][y][0] = False
        self.matrika[x][y][1] = False
        try:
            self.matrika[x-1][y][n] = False
        except:
            pass

        try:
            self.matrika[x+1][y][n] = False
        except:
            pass

        try:
            self.matrika[x][y-1][n] = False
        except:
            pass

        try:
            self.matrika[x][y+1][n] = False
        except:
            pass

######################################################################
## Igralec minimax

class minimax():
    pass

######################################################################
## Igralec alfabeta

class alfabeta():
    pass

######################################################################
## Igralec clovek

class clovek():
    pass


######################################################################
## Glavni program

if __name__ == "__main__":
    # Naredimo glavno okno in nastavimo ime
    root = Tk()
    root.title("Crnobelo")
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    aplikacija = crnobelo(root)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
