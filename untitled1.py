import folium
import json

#préparation des données géographiques
#préparation des données numériques


#création d’une instance de Folium.Map
coords = (46.6299767,1.8489683)
map = folium.Map(location=coords, tiles='OpenStreetMap', zoom_start=2)

#style function
sf = lambda x :{'fillColor':'#E88300', 'fillOpacity':0.5, 'color':'#E84000', 'weight':1, 'opacity':1}

folium.GeoJson(
        data='map.geojson',
        name='map.geojson',
        style_function= sf
    ).add_to(map)

geo_data = {"type": "FeatureCollection", "features": []} # master dict structure

fGeo = open('map.geojson', 'r', encoding='utf8')
g = json.loads(fGeo.read())
fGeo.close()
geo_data["features"].extend((g["features"])) # add current geojson data to master dict

#data prep


#application la méthode choropleth() à l'instance map
map.choropleth(
    geo_data=geo_data,
    name='choropleth',
    data=df,
    columns=['Pays d origine', 'Nombre total d artiste'], # data key/value pair
    key_on='feature.properties.code', # corresponding layer in GeoJSON
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Origine des artistes du MOMA'
)

map.save(outfile='map.html')