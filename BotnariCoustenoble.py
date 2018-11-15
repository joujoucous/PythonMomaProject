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
            if not listeLignes[i][2] in d :
                d[listeLignes[i][2]] = 1
            else:
                d[listeLignes[i][2]] = d[listeLignes[i][2]]+1
# Pour chaqués clés du dico
#	pour choques lignes du csv country
#		si clé EST CONTENU DANS linecountry[i][4]
#			clé <- linecountry[i][2]        ``
        dCountry={}
    #transformet la nationalité en pays

        for k in d.keys():
            ok=0
            nbLignes=len(listeLignesCountry)
            for i in range(1,nbLignes) :
                if k in listeLignesCountry[i][4] :
                    dCountry[listeLignesCountry[i][2]]=d[k]
                    ok = 1
                    break
        if ok==1 :
            print(k+"\n")
#faire l'histogramme avec les tailles des oeuvres ou ave le nombre d'oeuvres crées par années