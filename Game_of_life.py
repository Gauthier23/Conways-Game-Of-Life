# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 13:01:25 2022

@author: Gauthier Guyaz, Lycée Blaise-Cendrars, 3H

Github : https://github.com/Gauthier23
"""

from tkinter import*

###---Fonction dessinant la matrice---###
def dam():
    x, y, i = 0, 0, 0
    while x < side and y < side:    #tant qu'on a pas atteinds la dernière cellule en bas à droite
        can.create_rectangle(x, y, x + c, y + c, outline = "black", fill="")  #fill = "" ==> transparent
        dico[x/c,y/c]=0         
        x += c
        i += 1
        if i == side/c:             #quand "i" est égal à la longueur alors, on fait la ligne du dessous
            y += c
            x, i = 0, 0             #variables à zero pour recommancer la ligne
    
###---Fonction rendant vivante la cellule cliquée (valeur 1 sur la cellule cliquée au dico)---###
def click_gauche(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can.create_rectangle(x, y, x+c, y+c, fill='black')
    dico[x/c,y/c]=1
    
###---Fonction tuant la cellule cliquée donc met la valeur 0 pour la cellule cliquée au dico---###    
def click_droit(event): 
    x = event.x -(event.x%c)
    y = event.y -(event.y%c)
    can.create_rectangle(x, y, x+c, y+c, fill = backgroud_color)
    dico[x/c,y/c]=0    
            
          
###---Fonction comptant le nombre de cellule vivant limitrophe à la cellule concernée---###
def compte_voisins(x,y):                #coordonnés de la cellule (X,Y) comme entrée 
    nombre_voisins = 0                  #compteur du nombre de voisins à 0
    
    if dico.get((x-1, y-1), 0)==1:      #cellule au dessus à gauche, s'il n'existe pas dans le dico (ex: bords): on mets 0 par défault
        nombre_voisins+=1
        
    if dico.get((x-1, y), 0)==1:        #cellule à gauche, idem
        nombre_voisins+=1
        
    if dico.get((x-1, y+1), 0)==1:      #cellule en dessous à gauche, idem
        nombre_voisins+=1
        
    if dico.get((x, y-1), 0)==1:        #cellule en dessous, idem
        nombre_voisins+=1
        
    if dico.get((x, y+1), 0)==1:        #cellule au dessus, idem
        nombre_voisins+=1
        
    if dico.get((x+1, y-1), 0)==1:      #cellule en dessous à droite, idem
        nombre_voisins+=1
        
    if dico.get((x+1, y), 0)==1:        #cellule à droite, idem
        nombre_voisins+=1
        
    if dico.get((x+1, y+1), 0)==1:      #cellule au dessus à droite, idem
        nombre_voisins+=1
        
    return nombre_voisins               #on retourne la valeur du nombre de voisins

###---Fonction remplissant les carrés noirs selon les indications de la liste temporaire---###
def draw():
    global temp
    can.delete(ALL)                     #on supprime tout l'ancien Canvas
    dam()                               #recréation via fonction de la matrice neutre
    for y in range(0, int(side/c)):     #on parcours chaque coordonné Y
        for x in range(0, int(side/c)): #puis chaque X selon le Y
            if temp[x,y] == 1:          
                can.create_rectangle(c*x, c*y, c*x + c, c*y + c, fill="black")  #ajouts de la cellule vivante par rapport à la liste
    dico.update(temp)                   #on remplace notre dictionnaire par le temporaire
    
def calculer():
    global temp
    temp.update(dico)
    for y in range(0, int(side/c)):     #on parcours chaque coordonné Y
        for x in range(0, int(side/c)): #puis chaque X selon le Y
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
            fen.after(500, update_calculs)
        
def stop():
    global flag
    flag = 0
    
#####-----Variables et Constantes-----#####
c = 20                              #nombre de pixel pour le côté d'une cellule
side = 600                          #taille du côté du canvas carré dans lequel l'automate se développe
dico = {}                           #dictionaire principal contenant comme clé la position (x,y) et comme valeur son état (0 ou 1)
temp = {}                           #idem mais temporaire afin de gérer la transition vers un nouveau dictionaire principal
backgroud_color = "#D4E6F1"         #couleur de fond du canvas principal "#D4E6F1"

#####-----Gestionnaire du graphisme Tkinter-----#####    
  
fen = Tk()
Title = Label(text ='GAME OF LIFE',font = ("Helvetica", 10))
Title.pack(padx=7, pady=12)
can = Canvas(fen, width = side, heigh = side, bg = backgroud_color) 
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
