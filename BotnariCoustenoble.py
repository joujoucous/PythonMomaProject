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

from selenium import webdriver
import time 
import zipfile #pour dezipper
import os #pour retrouver le chemin courant


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : os.getcwd()}
chrome_options.add_experimental_option('prefs', prefs)
path=os.getcwd() + "\chromedriver.exe"
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'' + path )

driver.get("https://www.kaggle.com/account/login?returnUrl=%2Fmomanyc%2Fmuseum-collection%2Fversion%2F1")
time.sleep(5) # Let the user actually see something!

username = driver.find_element_by_name('username').send_keys('pythonesiee')
password=driver.find_element_by_name('password').send_keys('python.esiee16')
signIn=driver.find_element_by_id('submit-sign-in-button').click()
download=driver.find_element_by_name('download').click()

time.sleep(5) # Let the user actually see something!
driver.quit()

zip_ref = zipfile.ZipFile(os.getcwd() + "\museum-collection.zip", 'r')
zip_ref.extractall(os.getcwd())
zip_ref.close()



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