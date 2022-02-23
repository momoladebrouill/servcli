from threading import Thread
from random import *
from time import sleep
from tkinter import *
import socket

# le client se connecte a un serveur

serveur = "127.0.1.1"
port = 15555
so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((serveur, port))

print ("Connection on {} yes".format(port))

L=400
W=50

# une fenetre avec un champ pour ecrire et un champ pour visualiser 

class App(Tk):
 
    def __init__(self):
        self.n="CLI"
        Tk.__init__(self)
        self.title(self.n)
        F=Frame()
        F.pack()
        self.listbox=Listbox(F,width=W)
        self.listbox.pack(side = LEFT, fill = BOTH)
        self.scrollbar = Scrollbar(F)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.affiche("Bienvenue sur le chat, "+self.n);
        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)
        self.entree=Entry(self,width=W)
        self.entree.bind('<Return>',self.action)
        self.entree.pack(side = BOTTOM, fill = BOTH)
        self.prise=so
        self._fred=Thread(target=self.recevoir)
        self._fred.start()
    def affiche(self,txt):
        for elem in txt.split("\0"):
            self.listbox.insert(END,elem)
        self.listbox.yview_moveto(1)

    def action(self,*args):
        
        txt=self.entree.get()
        self.entree.delete(0,END)
        if txt.startswith("µ"):
            t=txt.split()
            self.listbox[t[1]]=t[2]
            self.affiche(f"µ time ! : {t[1]} = {self.listbox[t[1]]}")
        else:
            self.affiche(f"\0{self.n} : {txt}")
            self.prise.send(bytes(f"\0{self.n} : {txt}",'utf-8'))


    def recevoir(self):
        while True:
            txt=self.prise.recv(128).decode()
            self.affiche(txt)
            sleep(0.5)
         
App().mainloop()

