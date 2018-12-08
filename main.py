#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 17:34:07 2018

@author: joujoucous
"""
#imports
import csv
import folium
import matplotlib.pyplot as plt
import os
import pandas as pd
import math
from selenium import webdriver
import time 
import zipfile
from decimal import Decimal


#récuperer les deux csv sur internet et les dezippe
def recuperer_donnees():
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
    path=os.getcwd() + "\chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'' + path )
    
    driver.get("https://www.kaggle.com/account/login?returnUrl=%2Fmomanyc%2Fmuseum-collection%2Fversion%2F1")
    time.sleep(5) # Let the user actually see something!
    
    driver.find_element_by_name('username').send_keys('pythonesiee')
    driver.find_element_by_name('password').send_keys('python.esiee16')
    driver.find_element_by_id('submit-sign-in-button').click()
    driver.find_element_by_name('download').click()
    
    time.sleep(5) # Let the user actually see something!
    driver.quit()
    
    zip_ref = zipfile.ZipFile(os.getcwd() + "\museum-collection.zip", 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()
    #https://www.science-emergence.com/Articles/T%C3%A9l%C3%A9charger-un-fichier-pdf-du-web-avec-python/

#faire la carte du monde avec les nationalitées des artistes
def creer_carte():
    #ouverture du fichier artistes avec la methode sécurisée
    with open('artists.csv', 'r', encoding='utf8') as f:
        r = csv.reader(f)
        listeLignes = list(r) # l'itérable est converti en liste
        nbLignes=len(listeLignes)
            
        #ouverture du fichier contenant les nationalitees et les codes pays avec la methode sécurisée
        with open('SAFEcountries.csv', 'r', encoding='utf8') as f2:
            r = csv.reader(f2)
            listeLignesCountry = list(r) # l'itérable est converti en liste
            d={}
            
            #on compte le nombre d'artistes de chaques nationalité
            for i in range(1,nbLignes) :
                if not listeLignes[i][2] in d :
                    d[listeLignes[i][2]] = 1
                else:
                    d[listeLignes[i][2]] = d[listeLignes[i][2]]+1
                    
            # Pour chaqués clés du dico
            #	pour choques lignes du csv country
            #		si clé EST CONTENU DANS les nationalitees
            #			clé <- code pays        ``
            dCountry={}
            #transformet la nationalité en pays
            for k in d.keys():
                nbLignes=len(listeLignesCountry)
                for i in range(1,nbLignes) :
                    if k in listeLignesCountry[i][4] :
                        if not listeLignesCountry[i][2]=='UMI' :
                            if not listeLignesCountry[i][2]=='ASM' :
                                dCountry[listeLignesCountry[i][2]]=d[k]
                                break
            #transforme une donnée n en log(n) pour plus de lisiblité sur la carte
            for k in dCountry.keys():
                dCountry[k]=math.log(dCountry[k])
    
    #créer un fichier csv avec les données du dictionaire dCountry
    with open('cleanData.csv','w') as f:
        w = csv.writer(f)
        w.writerow(['Pays d origine', 'Nombre total d artiste'])
        w.writerows(dCountry.items())
    
    
    # charge les formes du monde
    word_geo = os.path.join('map.geojson')
     
    # charge le nombre d'artistes de chaques pays
    artists_origine = os.path.join('cleanData.csv')
    word_data = pd.read_csv(artists_origine)
     
    # Initialise la map:
    coords = (46.6299767,1.8489683)
    m = folium.Map(location=coords, zoom_start=2)
     
    # ajoute les couleurs pour chloropleth:
    m.choropleth(
     geo_data=word_geo,
     name='choropleth',
     data=word_data,
     columns=['Pays d origine', 'Nombre total d artiste'],
     key_on='feature.properties.A3',
     nan_fill_color='white',
     fill_color='YlOrRd',
     fill_opacity=1.0,
     line_opacity=0.2,
     legend_name='Origine geographique des artises'
    )
    folium.LayerControl().add_to(m)
     
    # Save to html
    m.save('MOMA.html')



#l'histogramme avec les tailles des oeuvres ou ave le nombre d'oeuvres crées par années
def creer_histogramme():
    with open('artworks.csv', 'r', encoding='utf8') as f3:
        r = csv.reader(f3)
        listeLignesOeuvres = list(r) # l'itérable est converti en liste
        nbOeuvres=len(listeLignesOeuvres)
    
        creationYear=[]
        surfaceAriaObject=[]
        for i in range(1,nbOeuvres) :
            try:
                if(float(listeLignesOeuvres[i][15])!=0 and float(listeLignesOeuvres[i][17])!=0):
                    surfaceAriaObject.append(float(listeLignesOeuvres[i][15])*float(listeLignesOeuvres[i][17]))               
            except ValueError:
                print ("invalid value on line ", i)
            if  (listeLignesOeuvres[i][4])!="" :
                str = (listeLignesOeuvres[i][4]).replace('-', ' ')
                creationYear+=([int(c) for c in str.split(' ') if (c.isdigit() and int(c)>1900)])
        
    #print(surfaceAriaObject)   
    
    plt.hist(creationYear,bins = list(range(1900,2018,5)), color = 'green',edgecolor = 'white')
    plt.xlabel("Année de création")
    plt.ylabel("Nombre d'oeuvres")
    plt.title("Nombre d'oeuvres créées par période")
    plt.show()
    
    print(surfaceAriaObject) 
    plt.hist(surfaceAriaObject,bins = list(range(0,9000,200)), color='blue',edgecolor = 'white')
    plt.xlabel("Surface(cm^2)")
    plt.ylabel("Nombre d'oeuvres")
    plt.title("Nombre d'oeuvres par surface")
    plt.show()
recuperer_donnees()
creer_carte()
creer_histogramme()