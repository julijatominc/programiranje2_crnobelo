from tkinter import*
import ast

PRAZNO = 0
JAZ = "Beli"
ON = "Crni"
VELIKOST = 5


class Tabla():
    def __init__(self, master, velikost=VELIKOST):
        self.velikost = velikost
        self.canvas = Canvas(master, width=100*(self.velikost+1), height=100*(self.velikost +1))
        self.canvas.grid(row=1, column=0)

        self.matrika1 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.matrika2 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.na_vrsti = JAZ
        for i in range(self.velikost+1):
            self.canvas.create_line(50, i*100 + 50,(self.velikost*100)+50,i*100 +50)
            self.canvas.create_line(i*100 +50, 50 , i*100 +50, (self.velikost*100) +50)
        self.canvas.bind("<Button-1>", self.izberi)
        self.napis = StringVar()
        label_napis = Label(master, textvariable=self.napis)
        label_napis.grid(row=0, column=0)

        menu = Menu(master)
        master.config(menu=menu)
        
        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Nova igra", command=self.nova_igra)
        file_menu.add_command(label="Shrani", command=self.shrani)
        file_menu.add_command(label="Odpri", command=self.odpri)
        file_menu.add_separator() 
        file_menu.add_command(label="Izhod", command=master.destroy)

        settings_menu = Menu(menu)
        menu.add_cascade(label="Velikost", menu=settings_menu)
        settings_menu.add_command(label="5", command=self.nova_igra)
        settings_menu.add_command(label="6", command=self.nova_igra)
        settings_menu.add_command(label="7", command=self.nova_igra)
        settings_menu.add_command(label="8", command=self.nova_igra)
        settings_menu.add_command(label="9", command=self.nova_igra)



       
        

    def izberi(self, event):
        self.napis.set("")
        x, y = (event.x - 50) // 100, (event.y - 50) // 100
        
        if self.dovoljeno(x, y, self.na_vrsti):
            if self.na_vrsti == JAZ:
                self.matrika1[x][y] = JAZ
                self.na_vrsti = ON
                self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140)
            else:
                self.matrika2[x][y] = ON
                self.na_vrsti = JAZ
                self.canvas.create_oval(x * 100 + 60, y * 100 + 60, x * 100 + 140, y * 100 + 140, fill="black")

            if self.konec_zabave(self.na_vrsti):
                if self.na_vrsti == JAZ:
                    self.na_vrsti = ON
                else:
                    self.na_vrsti = JAZ
                self.napis.set("Konec igre! Zmagal je {0}!".format(self.na_vrsti))

        else:
            self.napis.set("Neveljavna poteza!")
        

    def dovoljeno(self, x, y, na_vrsti):
        if self.na_vrsti == JAZ:
            self.matrika = self.matrika2
        else: self.matrika = self.matrika1
        if x>PRAZNO and x< (self.velikost - 1) and y>PRAZNO and y< (self.velikost - 1):
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO and self.matrika[x+1][y]==PRAZNO and self.matrika[x][y+1]==PRAZNO and self.matrika[x][y-1]==PRAZNO:
                return True
            else:
                return False
                
            
        elif x>PRAZNO and x< (self.velikost - 1) and y==PRAZNO:
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO and self.matrika[x+1][y]==PRAZNO and self.matrika[x][y+1]==PRAZNO:
                return True
            else:
                return False
            
        elif x>PRAZNO and x< (self.velikost - 1) and y==(self.velikost -1):
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO and self.matrika[x+1][y]==PRAZNO and self.matrika[x][y-1]==PRAZNO:
                return True
            else:
                return False     
                
                
        elif x==PRAZNO  and y<(self.velikost -1)and y>PRAZNO :
            if self.matrika[x+1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y-1]==PRAZNO and self.matrika[x][y+1]==PRAZNO :
                return True
            else:
                return False
                
                
        elif  x== (self.velikost - 1)  and y<(self.velikost -1)and y>PRAZNO :
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y-1]==PRAZNO and self.matrika[x][y+1]==PRAZNO :
                return True
            else:
                return False

        elif x== (self.velikost - 1) and y==(self.velikost -1):
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y-1]==PRAZNO:
                return True
            else:
                return False

        elif x== (self.velikost - 1) and y==PRAZNO:
            if self.matrika[x-1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y+1]==PRAZNO:
                return True
            else:
                return False

        elif x==PRAZNO and y==PRAZNO:
            if self.matrika[x+1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y+1]==PRAZNO:
                return True
            else:
                return False

        elif x==PRAZNO and y==(self.velikost -1):
            if self.matrika[x+1][y]==PRAZNO and self.matrika[x][y]==PRAZNO  and self.matrika[x][y-1]==PRAZNO:
                return True
            else:
                return False

    def konec_zabave(self, na_vrsti):
        if self.na_vrsti == JAZ:
            self.matrika3 = self.matrika1
        else:
            self.matrika3 = self.matrika2
        
        for x in range(len(self.matrika3)):
            for y in range(len(self.matrika3)):
                if self.matrika3[x][y] == 0 and self.dovoljeno(x, y, self.na_vrsti):
                    return False
        return True

    def nova_igra(self):

        self.matrika1 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.matrika2 = [[PRAZNO] * self.velikost for _ in range(self.velikost)]
        self.canvas.delete("all")
        self.napis.set("")
        self.na_vrsti = JAZ

        for i in range(self.velikost +1):
             self.canvas.create_line(50, i*100 + 50, (self.velikost*100) + 50,i*100 +50)
             self.canvas.create_line(i*100 +50, 50 , i*100 +50, (self.velikost*100) + 50)

    def shrani(self):
        ime = filedialog.asksaveasfilename()
        if ime == "":
            return
        with open(ime, "wt", encoding="utf8") as f:
            print(self.matrika1, file=f)
            print(self.matrika2, file=f)
            print(self.na_vrsti, file=f)

    def odpri(self):
        ime = filedialog.askopenfilename()
        self.nova_igra()
        s = open(ime, encoding="utf8")
        sez = s.readlines()
        s.close

        self.matrika1 = ast.literal_eval(sez[0].strip())
        self.matrika2 = ast.literal_eval(sez[1].strip())
        KDO = sez[2].strip()
        if KDO == str("Beli"):
            self.na_vrsti = JAZ
        else: self.na_vrsti = ON
        
        for i in range(self.velikost):
            for j in range(self.velikost):
                if self.matrika1[i][j] != 0:
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j * 100 + 140)
                if self.matrika2[i][j] != 0:
                    self.canvas.create_oval(i * 100 + 60, j * 100 + 60, i * 100 + 140, j* 100 + 140, fill="black")
        
root = Tk()
aplikacija = Tabla(root)

root.mainloop()   
