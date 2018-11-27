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
        for k in dCountry.keys():
            dCountry[k]=math.log(dCountry[k])

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
 #threshold_scale=[1,100,500,1000,2000,5200],
 key_on='feature.properties.A3',
 #nan_fill_color='white',
 fill_color='YlOrRd',
 fill_opacity=1.0,
 line_opacity=0.2,
 #legend_name='Origine des artises'
)
folium.LayerControl().add_to(m)
 
# Save to html
m.save('MOMA.html')


#faire l'histogramme avec les tailles des oeuvres ou ave le nombre d'oeuvres crées par années
                
with open('artworks.csv', 'r', encoding='utf8') as f3:
    r = csv.reader(f3)
    listeLignesOeuvres = list(r) # l'itérable est converti en liste
    nbOeuvres=len(listeLignesOeuvres)

    data=[]
    for i in range(1,nbOeuvres) :
        if  (listeLignesOeuvres[i][4])!="" :
            str = (listeLignesOeuvres[i][4]).replace('-', ' ')
            data+=([int(c) for c in str.split(' ') if (c.isdigit() and int(c)>1900)])
    #print(data)
     
plt.hist(data,bins = list(range(1900,2018,5)), color = 'green',edgecolor = 'white')
plt.xlabel("Année de création")
plt.ylabel("Nombre d'oeuvres")
plt.title("Nombre d'oeuvres créées par période")
plt.show()

#{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"MultiPolygon","coordinates":[[[[-24.39,14.81],[-24.5,14.92],[-24.37,15.05],[-24.28,14.88],[-24.39,14.81]]],[[[-23.68,15.31],[-23.44,15.04],[-23.48,14.91],[-23.78,15.06],[-23.68,15.31]]],[[[-24.32,16.49],[-24.42,16.65],[-24.01,16.57],[-24.32,16.49]]],[[[-25.09,17.2],[-24.99,17.06],[-25.3,16.91],[-25.34,17.09],[-25.09,17.2]]],[[[-23.12,15.14],[-23.23,15.15],[-23.18,15.34],[-23.12,15.14]]],[[[-22.91,16.15],[-22.79,16.23],[-22.67,16.08],[-22.88,15.97],[-22.91,16.15]]],[[[-22.94,16.68],[-22.92,16.86],[-22.89,16.59],[-22.94,16.68]]]]},"properties":{"A3":"CPV"}}