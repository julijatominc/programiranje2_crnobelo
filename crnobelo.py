from tkinter import*


######################################################################
## Zacetne nastavitve

PRAZNO = 0
JAZ = "Beli"
ON = "Crni"
VELIKOST = 5

######################################################################
## Igra

class tabla():
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

        self.matrika1 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.matrika2 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.napis.set("")
        self.na_vrsti = JAZ

    # Funkcija, ki reagira na izbiro polja s strani uporabnika.
    def izberi(self, event):
        pass

    # Funkcija, ki shrani igro v datoteko.
    def shrani(self):
        pass

    # Funkcija, ki nalozi igro iz datoteke.
    def odpri(self):
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
