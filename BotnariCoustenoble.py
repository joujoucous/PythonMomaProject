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
import json
import os
import pandas as pd

#récuperer les deux csv sur internet

#from selenium import webdriver
#import time 
#import zipfile #pour dezipper
#import os #pour retrouver le chemin courant


#chrome_options = webdriver.ChromeOptions()
#prefs = {'download.default_directory' : os.getcwd()}
#chrome_options.add_experimental_option('prefs', prefs)
#path=os.getcwd() + "\chromedriver.exe"
#driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'' + path )

#driver.get("https://www.kaggle.com/account/login?returnUrl=%2Fmomanyc%2Fmuseum-collection%2Fversion%2F1")
#time.sleep(5) # Let the user actually see something!

#username = driver.find_element_by_name('username').send_keys('pythonesiee')
#password=driver.find_element_by_name('password').send_keys('python.esiee16')
#signIn=driver.find_element_by_id('submit-sign-in-button').click()
#download=driver.find_element_by_name('download').click()

#time.sleep(5) # Let the user actually see something!
#driver.quit()

#zip_ref = zipfile.ZipFile(os.getcwd() + "\museum-collection.zip", 'r')
#zip_ref.extractall(os.getcwd())
#zip_ref.close()
#https://www.science-emergence.com/Articles/T%C3%A9l%C3%A9charger-un-fichier-pdf-du-web-avec-python/



#faire la carte du monde avec les nationalitées des artistes
    #ouverture du fichier artistes avec la methode sécurisée
with open('artists.csv', 'r', encoding='utf8') as f:
    r = csv.reader(f)
    listeLignes = list(r) # l'itérable est converti en liste
    nbLignes=len(listeLignes)
    
    with open('SAFEcountries.csv', 'r', encoding='utf8') as f2:
        
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
                    if not listeLignesCountry[i][2]=='UMI' :
                        if not listeLignesCountry[i][2]=='ASM' :
                            dCountry[listeLignesCountry[i][2]]=d[k]
                            ok = 1
                            break
            if ok==0:
                print(k+"\n")

#créer un fichier csv avec les données du dictionaire dCountry
with open('cleanData.csv','w') as f:
    w = csv.writer(f)
    w.writerow(['Pays d origine', 'Nombre total d artiste'])
    w.writerows(dCountry.items())


# Load the shape of the zone
word_geo = os.path.join('map.geojson')
 
# Load the number of artists comeing from each country
artists_origine = os.path.join('cleanData.csv')
word_data = pd.read_csv(artists_origine)
 
# Initialize the map:
coords = (46.6299767,1.8489683)
m = folium.Map(location=coords, zoom_start=2)
 
# Add the color for the chloropleth:
m.choropleth(
 geo_data=word_geo,
 name='choropleth',
 data=word_data,
 columns=['Pays d origine', 'Nombre total d artiste'],
 key_on='feature.properties.A3',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.2,
 legend_name='Origine des artises'
)
folium.LayerControl().add_to(m)
 
# Save to html
m.save('MOMA.html')

  #faire l'histogramme avec les tailles des oeuvres ou ave le nombre d'oeuvres crées par années
                
with open('artworks.csv', 'r', encoding='utf8') as f3:
    r = csv.reader(f3)
    listeLignesOeuvres = list(r) # l'itérable est converti en liste
    nbOeuvres=len(listeLignesOeuvres)
    for i in range(1,nbOeuvres) :
        if  (listeLignesOeuvres[i][5])!="" :
            data[i-1]=listeLignesOeuvres[i][5]
            print(data[i-1]+"\n")
     
#data = [1995,1997,1995,1974,1995,1997,1987,1940,1956,1977,1990]
#plt.hist(data,normed=1)
plt.hist(data,bins = list(range(1940,2000,10)), color = 'yellow',edgecolor = 'red')
plt.xlabel('Année création oeuvres')
plt.ylabel('Nombre Oeuvres')
plt.title('Exemple d\' histogramme simple')
plt.show()
        

