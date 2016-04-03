from tkinter import*
from tkinter import filedialog
from Tabla import*
from Igralci import*
import ast
import argparse
import logging
import re
try:
    import winsound
except:
    pass


# Zacetne vrednosti.
BELI = "Beli"
CRNI = "Crni"
VELIKOST = 6
MINIMAX_GLOBINA = 2
ALFABETA_GLOBINA = 2


# Razred, ki definira graficni vmesnik.
class Crnobelo():
    # Ustvarimo tag, da se bomo lahko kasneje sklicevali.
    TAG_KROG = 'krog'
    TAG_POTEZA = 'poteza'
    TAG_NAMIG = 'namig'
    TAG_ZP = 'zadnja' #poteza


    def __init__(self, master, velikost=VELIKOST):
        self.BELI = None
        self.CRNI = None
        self.igra = None
        self.zvocnik = True
        self.NAMIG = False

        # Ustvarimo napis, ki nas obvesca o dogajanju. Sporoča, kaj se dogaja z igralcem racunalnik.
        self.napis = StringVar()
        Label(master, textvariable=self.napis).grid(row=0, column=0)

        # Ustvarimo napis, ki nas obvesca o dogajanju. Sporoča, kdo je na vrsti.
        self.napis2 = StringVar()
        Label(master, textvariable=self.napis2).grid(row=1, column=0)
    
        
        # Nastavi velikost.
        self.velikost = velikost

        # Ustvari canvas.
        self.canvas = Canvas(master, width=100*(self.velikost+1), height=100*(self.velikost +1))

        self.canvas.grid(row=2, column=0, columnspan=2)

        # Na canvas narise zacetno polje.
        self.narisi()

        # Povezemo klik z dogodkom.
        self.canvas.bind("<Button-1>", self.plosca_klik)
        
        # Gumb za namig.
        Button(master, text= "Namig", command = lambda: self.pobarvaj_namig()).grid(row = 0, column = 1, rowspan = 2)
    
        # Glavni menu.
        menu = Menu(master)
        master.config(menu=menu)
        
        # Velikosti okna ne moremo spreminjati.
        master.resizable(width=False, height=False) 

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

        settings_menu = Menu(menu)
        menu.add_cascade(label="Barva ozadja", menu=settings_menu)
        settings_menu.add_command(label="Siva", command = lambda: self.canvas.configure(background='light slate gray'))
        settings_menu.add_command(label="Modra", command = lambda: self.canvas.configure(background='light sky blue'))
        settings_menu.add_command(label="Zelena", command = lambda: self.canvas.configure(background='pale green'))
        settings_menu.add_command(label="Rumena", command = lambda: self.canvas.configure(background='light goldenrod'))
        settings_menu.add_command(label="Brez barve", command = lambda: self.canvas.configure(background='gray94'))

        menu.add_command(label="Pomoc", command = lambda: pomoc())

        # Funkcija, ki odpre novo okno. Vsebina je pomoč.
        def pomoc():
            window = Toplevel(root)
            label = Label(window, text = """Navodila:
Cilj igre:
Igro igrata dva igralca na kvadratni sahovnici, katere velikost se da nastaviti v kaskadi velikost.
Zacne igralec, ki polaga bele kroge, nato igralca izmenicno igrata dokler enemu od njih ne zmanjka moznih potez. Takrat je igre konec, 
zmagal je igralec, ki je zadnji opravil potezo. Barva zmagovalca se izpise nad igralno plosco.

Pravila igre:
Igralec lahko takrat ko je na potezi igra svoj krog na tista polja, za katera je izpolnjen naslednji pogoj: Na nobenem od sosednjih polj
ni nasprotnikovega kroga. Pri tem se za sosednja polja stejejo polja levo, desno, nad in pod poljem (ce so seveda znotraj sahovnice). Če
igralec odigra napačno potezo, ga uporabniski vmesnik na to opozori z napisom "Neveljavna poteza!" nad sahovnico. Vsakic ko je na potezi
cloveski igralec, se mozne poteze obarvajo s sivo.

Izbira igralcev in Namig:
Uporabnik lahko izbira med igralci v kaskadi igralci. Moznih je vec izbir, uporabnik lahko izbere katerakoli dva izmed treh razlicnih
racunalniskih igralcev in enim cloveskim. Ko je na vrsti racunalniski igralec, se nad sahovnico izpise "Razmisljam.". Cloveski igralec ima
moznost, da uporabi namig racunalnika s klikom na gumb "Namig". Po kliku zacne racunalnik razmisljati, ko izracuna potezo, jo na sahovnici
oznaci z rdeco.

Nova igra:
V kaskadi "Datoteka" lahko igralec zacne novo igro. Pri tem se zamenja vrstni red igranja. Na primer: ce je v prejsnji igri igralec 1 ena
bil beli (in s tem zacel), je sedaj beli njegov nasprotnik (torej zacne on).

Zvok:
Vsakic ko se opravi poteza, se zaslisi ton nizke frekvence. Ko je igre konec pa ton visje frekvence. Uporabnik lahko v kaskadi "Zvok"
izklopi oziroma znova vklopi zvocne efekte.
Zvok deluje samo v operacijskem sistemu Windows.

Barva ozadja:
V kaskadi "Barva ozadja" lahko uporabnik izbira barvo ozadja. Izbira lahko med sivo, modro, zeleno in rumeno, lahko pa tudi povrne barvo
na prvotno.

Shrani in odpri:
V kaskadi "Datoteka" ima uporabnik moznost, da igro s klikom na "Shrani" shrani v tekstovno datoteko, ki jo sam poimenuje. Shranjeno igro
lahko kadarkoli zopet nadaljuje s klikom na "Odpri" in ustrezno izbiro datoteke.

Izhod:
S klikom na "Izhod" v kaskadi "Datoteka" uporabnik zapusti igro.""")
        
            label.pack(side = "top", fill = "both")

        logging.debug("Velikost: {0}.".format(self.velikost))
        
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
        self.canvas.delete(Crnobelo.TAG_NAMIG)
        self.NAMIG = False
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

        logging.debug("Velikost: {0}.".format(self.velikost))

        #Ustvarimo matriko z zacetnimi vrednostmi
        self.igra.matrika = [[[True, True, None] for _ in  range(self.velikost)] for _ in range(self.velikost)]

        
        self.napis.set("")

        self.igra.na_vrsti = BELI
        self.napis2.set("Na vrsti je beli.")
        
        logging.debug("Na vrsti:{0}".format(self.igra.na_vrsti))
        logging.debug("Beli: {0}, Crni: {1}".format(self.BELI, self.CRNI))
        
        #Zacnemo igro
        self.BELI.igraj()

    # Funkcija, ki preda dogodek na plosci razredu igralca, ki je storil to potezo.
    def plosca_klik(self, event):
        # Če kliknemo medtem, ko je vklopljen namig, se ne zgodi nič.
        if self.NAMIG:
            pass
        # Predamo informacijo naprej.
        else:
            if self.igra.na_vrsti == BELI:
                self.BELI.klik(event)
            elif self.igra.na_vrsti == CRNI:
                self.CRNI.klik(event)
            else:
                pass

    # Funkcija, ki glede na igralca na vrsti in na njegovo dejanje naredi potezo ali pobarva namig, če je vklopljen.
    def izberi(self, xy):
        x = xy[0]
        y = xy[1]
        
        logging.debug("Preverim, ce je konec igre.")
        
        # Preveri, ce je konec igre. V primeru, da je konec, nocemo vec dogajanja na plosci.

        if not self.igra.je_konec():
            
            # Pobarvamo namig.
            if self.NAMIG:
                self.canvas.create_rectangle((x * 100* 6/(self.velikost)+ 50), (y *100* 6/(self.velikost)+ 50), (x * 100* 6/(self.velikost)+ 50+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50+100*6/(self.velikost)), fill="indian red", tag=Crnobelo.TAG_NAMIG)
                self.NAMIG = False

            # Naredimo potezo.
            else:
                self.napis.set("")
                poteza = self.igra.povleci_potezo(xy)
                
                # Poteza je neveljavna. Poskusimo ponovno
                if poteza is None:
                    self.napis.set("Neveljavna poteza!")
                    if self.igra.na_vrsti == BELI:
                        self.BELI.igraj()
                    elif self.igra.na_vrsti == CRNI:
                        self.CRNI.igraj()
                    else:
                        assert False

                # Poteza je veljavna.
                else:
                    if self.igra.na_vrsti == CRNI:
                        self.canvas.delete(Crnobelo.TAG_ZP)
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "white", tag=Crnobelo.TAG_KROG)
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "blue", tag=Crnobelo.TAG_ZP)
                        self.napis2.set("Na vrsti je crni.")
                        
                    else:
                        self.canvas.delete(Crnobelo.TAG_ZP)
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "black", tag=Crnobelo.TAG_KROG)
                        self.canvas.create_oval((x * 100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (y *100* 6/(self.velikost)+ 50+10* 6/(self.velikost)), (x * 100* 6/(self.velikost)+ 50-10* 6/(self.velikost)+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50-10* 6/(self.velikost)+100*6/(self.velikost)), fill = "blue", tag=Crnobelo.TAG_ZP)
                        self.napis2.set("Na vrsti je beli.")

                    # Ob odigrani potezi: beep!
                    if self.zvocnik:
                        try: winsound.Beep(150, 75)
                        except: pass
                        
                    # Ce je igre konec.
                    if self.igra.je_konec():
                        self.igra.na_vrsti = nasprotnik(self.igra.na_vrsti)
                        self.napis2.set("")
                        self.napis.set("Konec igre! Zmagal je {0}!".format(self.igra.na_vrsti))
                        if self.zvocnik:
                            try: winsound.Beep(500, 150)
                            except: pass

                    # Igre ni konec, nadaljujemo.
                    else:

                        if self.igra.na_vrsti == BELI:
                            self.BELI.igraj()
                        elif self.igra.na_vrsti == CRNI:
                            self.CRNI.igraj()
                        else:
                            assert False

        logging.debug("{0}".format(self.igra.veljavne_poteze()))

    # Poklice funkcijo izberi z alfabeta in pobarva namig.
    def pobarvaj_namig(self):
        
        self.NAMIG = True
        if self.igra.na_vrsti == BELI and ('Clovek' in (re.findall(r'\.(.+?)\s', str(self.BELI)))):
            Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)).igraj()
            self.BELI.igraj()
            
        elif self.igra.na_vrsti == CRNI and ('Clovek' in (re.findall(r'\.(.+?)\s', str(self.CRNI)))):
            Racunalnik(self, Alfabeta(ALFABETA_GLOBINA)).igraj()
            self.CRNI.igraj()

        # Namig deluje, če ga poklice človek
        else:
            self.NAMIG = False
            pass
        
    # Na canvasu pobarva veljavne poteze.  
    def pobarvaj_poteze(self):
        poteze = self.igra.veljavne_poteze()
        for i in poteze:
            x, y = i
            self.canvas.create_rectangle((x * 100* 6/(self.velikost)+ 50), (y *100* 6/(self.velikost)+ 50), (x * 100* 6/(self.velikost)+ 50+100*6/(self.velikost)), (y *100* 6/(self.velikost) + 50+100*6/(self.velikost)), fill='light grey', tag=Crnobelo.TAG_POTEZA)

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

    # Funkcija izklopi zvok.
    def zvok(self, bool):
        if not bool:
            self.zvocnik = False


    # Funkcija, ki prekine igralca.
    def prekini_igralce(self):
        if self.BELI:
            self.BELI.prekini()
        if self.CRNI:
            self.CRNI.prekini()

######################################################################
## Glavni program

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Igrica Crnobelo")

    # Opisemo argumente, ki jih sprejmemo iz ukazne vrstice.
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



    # Naredimo glavno okno in nastavimo ime.
    root = Tk()
    root.title("Crnobelo")
    # Naredimo objekt razreda Gui in ga spravimo v spremenljivko,
    aplikacija = Crnobelo(root)
    # Kontrolo prepustimo glavnemu oknu. Funkcija mainloop neha
    # delovati, ko okno zapremo.
    root.mainloop()
