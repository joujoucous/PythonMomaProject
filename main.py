#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 17:34:07 2018

@author: Botnari Marina et Coustenoble Julie
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
from jinja2 import Template
import webbrowser


#récuperer les deux csv sur internet et les dezippe
def recuperer_donnees():
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'' + path )
    
    driver.get("https://www.kaggle.com/account/login?returnUrl=%2Fmomanyc%2Fmuseum-collection%2Fversion%2F1")
    time.sleep(5) # temps de chragement de la page
    
    # l'identification sur le site
    driver.find_element_by_name('username').send_keys('pythonesiee')
    driver.find_element_by_name('password').send_keys('python.esiee16')
    driver.find_element_by_id('submit-sign-in-button').click()
    #telechargement de l'archive contenant les fichiers csv
    driver.find_element_by_name('download').click()
    
    time.sleep(5) 
    driver.quit()
    
    #dezarchiver
    zip_ref = zipfile.ZipFile(os.getcwd() + "\museum-collection.zip", 'r')
    zip_ref.extractall(os.getcwd())
    zip_ref.close()


#faire la carte du monde avec les nationalitées des artistes
def creer_carte():
    #ouverture du fichier artistes avec la methode sécurisée
    try:
        with open('artists.csv', 'r', encoding='utf8') as f:
            r = csv.reader(f)
            listeLignes = list(r) # l'itérable est converti en liste
            nbLignes=len(listeLignes)
              
            try:
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
                    #transformer la nationalité en pays
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
            except IOError:
                print ("Le fichier n'a pas été trouvé")
    except IOError:
            print ("Le fichier n'a pas été trouvé")
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
         legend_name='Origine geographique des artises (log(n))'
    )
    folium.LayerControl().add_to(m)
     
    # Save to html
    m.save('MOMA.html')

#faire un capture d'ecran de la carte créée pour obtenir la carte en format png
def image_carte():

    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'' + path )
    htmlFile="file:///"+os.getcwd() + "\MOMA.html"
    print(htmlFile)
    driver.get(htmlFile)
    driver.maximize_window()
    time.sleep(1)
    driver.save_screenshot('map.png')
    driver.quit()

# l'histogramme avec les surfaces des oeuvres
# et l'histogramme avec le nombre d'oeuvres crées par années
def creer_histogrammes():
    try:
        with open('artworks.csv', 'r', encoding='utf8') as f3:
            r = csv.reader(f3)
            listeLignesOeuvres = list(r) 
            nbOeuvres=len(listeLignesOeuvres)
        
            creationYear=[]
            surfaceAriaObject=[]
            #extraction données
            for i in range(1,nbOeuvres) :
                try:
                    if(float(listeLignesOeuvres[i][15])!=0 and 
                       float(listeLignesOeuvres[i][17])!=0) :
                        surfaceAriaObject.append(float(listeLignesOeuvres[i][15])*float(listeLignesOeuvres[i][17]))               
                except ValueError:
                        print ("invalid values on line", i)
                if  (listeLignesOeuvres[i][4])!="" :
                    str = (listeLignesOeuvres[i][4]).replace('-', ' ')
                    creationYear+=([int(c) for c in str.split(' ') if (c.isdigit() and int(c)>1900)])
    except IOError:
            print ("Le fichier n'a pas été trouvé")
            
    plt.hist(creationYear,bins = list(range(1900,2018,5)), color = 'green',edgecolor = 'white')
    plt.xlabel("Année de création")
    plt.ylabel("Nombre d'oeuvres")
    plt.title("Nombre d'oeuvres créées par période")
    plt.savefig("histogramme1.png")
    plt.show()
    
    plt.hist(surfaceAriaObject,bins = list(range(0,9000,200)), color='blue',edgecolor = 'white')
    plt.xlabel("Surface(cm^2)")
    plt.ylabel("Nombre d'oeuvres")
    plt.title("Nombre d'oeuvres par surface")
    plt.savefig("histogramme2.png")
    plt.show()

# mettre la carte et les deux histogrammes dans une page html
# et ouvrir la page finale html
def creer_html():
        t = Template("<html><body><img src='{{img1_src }}'width=1000><img src='{{img2_src }}'><img src='{{img3_src }}'></body></html>")
        try:
            with open('ResultatFinal.html','w') as html:
                html.write(t.render(img1_src='map.png', img2_src='histogramme1.png', img3_src='histogramme2.png'))
        except:                     
            print ("Le fichier n'a pas été trouvé")
            
        try:
            webbrowser.open("file:///"+os.getcwd() +"\ResultatFinal.html")
        except:                     
            print ("Le fichier n'a pas été trouvé")
            
# configurations browser Chhrome     
chrome_options = webdriver.ChromeOptions()
#chager le chemin des telechargements 
prefs = {'download.default_directory' : os.getcwd()}
chrome_options.add_experimental_option('prefs', prefs)
#donner le chemin de l'éxecutable du chrome driver
path=os.getcwd() + "\chromedriver.exe" 

recuperer_donnees()
creer_carte()
image_carte()
creer_histogrammes()
creer_html()
