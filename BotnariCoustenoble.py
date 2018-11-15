#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 17:34:07 2018

@author: joujoucous
"""
#imports
import csv
import folium

#récuperer les deux csv sur internet
#https://www.science-emergence.com/Articles/T%C3%A9l%C3%A9charger-un-fichier-pdf-du-web-avec-python/





#faire la carte du monde avec les nationalitées des artistes
    #ouverture du fichier artistes avec la methode sécurisée
with open('artists.csv', 'r') as f:
    r = csv.reader(f)
    listeLignes = list(r) # l'itérable est converti en liste
    nbLignes=len(listeLignes)
    
    with open('countries.csv', 'r') as f2:
        
        r = csv.reader(f2)
        listeLignesCountry = list(r) # l'itérable est converti en liste
        d={}
        for i in range(1,nbLignes) :
            print(listeLignes[i][2]+"\n")
            if not listeLignes[i][2] in d :
                d[listeLignes[i][2]] = 1
            else:
                d[listeLignes[i][2]] = d[listeLignes[i][2]]+1
                

    #transformet la nationalité en pays

#faire l'histogramme avec les tailles des oeuvres ou ave le nombre d'oeuvres crées par années