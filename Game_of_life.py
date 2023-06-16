# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 13:01:25 2022

@author: Gauthier Guyaz, Lycée Blaise-Cendrars, 3H
"""

from tkinter import*

#####-----Variables et Constantes-----#####
CELL = 10                              #nombre de pixel pour le côté d'une cellule
SIDE = 600                          #taille du côté du canvas carré dans lequel l'automate se développe
dico = {}                           #dictionaire principal contenant comme clé la position (x,y) et comme valeur son état (0 ou 1)
temp = {}                           #idem mais temporaire afin de gérer la transition vers un nouveau dictionaire principal
BACKGROUND_COLOR = "#FFFFFF"         #couleur de fond du canvas principal "#D4E6F1"

###---Fonction dessinant la matrice---###

def dam():
    #-double boucle parcourant chaque cellule du canvas-#
    for y in range(0, SIDE, CELL):
        for x in range(0, SIDE, CELL):
            #-création d'une cellule associée à une position-#
            can.create_rectangle(x, y, x + CELL, y + CELL, outline="black", fill="")
            #-initialisation de la cellule à 0 dans le dictionnaire-#
            dico[int(x/CELL), int(y/CELL)] = 0 
    
###---Fonction rendant vivante la cellule cliquée (valeur 1 sur la cellule cliquée au dico)---###
def click_gauche(event): 
    x = event.x -(event.x%CELL)
    y = event.y -(event.y%CELL)
    can.create_rectangle(x, y, x+CELL, y+CELL, fill='black')
    dico[int(x/CELL),int(y/CELL)]=1
    
###---Fonction tuant la cellule cliquée donc met la valeur 0 pour la cellule cliquée au dico---###    
def click_droit(event): 
    x = event.x -(event.x%CELL)
    y = event.y -(event.y%CELL)
    can.create_rectangle(x, y, x+CELL, y+CELL, fill = BACKGROUND_COLOR)
    dico[int(x/CELL),int(y/CELL)]=0    
            
          
###---Fonction comptant le nombre de cellule vivant limitrophe à la cellule concernée---###
def compte_voisins(x, y): #coordonnés de la cellule (X,Y) comme entrée
    nombre_voisins = 0
    voisins = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
    for coord in voisins:       #on parcourt chaque tuple
        if dico.get(coord, 0) == 1:
            nombre_voisins += 1
    return nombre_voisins

###---Fonction remplissant les carrés noirs selon les indications de la liste temporaire---###
def draw():
    global temp
    can.delete(ALL)                     #on supprime tout l'ancien Canvas
    dam()                               #recréation via fonction de la matrice neutre
    for y in range(0, int(SIDE/CELL)):     #on parcours chaque coordonné Y
        for x in range(0, int(SIDE/CELL)): #puis chaque X selon le Y
            if temp[x,y] == 1:          
                can.create_rectangle(CELL*x, CELL*y, CELL*x + CELL, CELL*y + CELL, fill="black")  #ajouts de la cellule vivante par rapport à la liste
    dico.update(temp)                   #on remplace notre dictionnaire par le temporaire
    
def calculer():
    global temp
    temp.update(dico)
    for y in range(0, int(SIDE/CELL)):     #on parcours chaque coordonné Y
        for x in range(0, int(SIDE/CELL)): #puis chaque X selon le Y
            nombre_voisins = compte_voisins(x,y) #on appelle la fonction permettant de connaître le nombre de voisins
            
            #-Règle 1 - mort d'isolement-#
            if dico[x,y] == 1 and nombre_voisins < 2: 
                temp[x,y] = 0 
            
            #-Règle 2 - Toute cellule avec 2 ou 3 voisins survit-#
            if dico[x,y] == 1 and (nombre_voisins == 2 or nombre_voisins == 3): 
                temp[x,y] = 1 
            
            #-Règle 3 - mort par surpopulation-#
            if dico[x,y] == 1 and nombre_voisins > 3:
                temp[x,y] = 0 #
            
            #-Règle 4 - naissance-#
            if dico[x,y] == 0 and nombre_voisins == 3: 
                temp[x,y] = 1 
    draw()

###---Fonction gérant la répétition des générations selon le temps---###

def withtime():
    global flag
    flag = 1
    update_calculs()
    
        
def update_calculs():
    calculer()
    if flag == 1:
            fen.after(200, update_calculs)
        
def stop():
    global flag
    flag = 0



#####-----Gestionnaire du graphisme Tkinter-----#####    
  
fen = Tk()
Title = Label(text ='GAME OF LIFE',font = ("Helvetica", 10))
Title.pack(padx=7, pady=12)
can = Canvas(fen, width = SIDE, heigh = SIDE, bg = BACKGROUND_COLOR) 
b1 = Button(fen, text='Lancer une étape', command=calculer )
can.pack(side=TOP, padx=20, pady=10)
b1.pack(side = LEFT, padx=5, pady=5)
can.bind("<Button-1>", click_gauche)
can.bind("<Button-3>", click_droit)
b2 = Button(fen, text='Lancer', command = withtime )
b3 = Button(fen, text='Stop', command = stop)
b2.pack(side = LEFT, padx=5, pady=5)
b3.pack(side = LEFT, padx=5, pady=5)

#####-----Préparation interface de base-----#####

dam()
fen.mainloop()
