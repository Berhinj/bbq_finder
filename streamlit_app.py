import streamlit as st
from streamlit_folium import folium_static
import folium
import numpy as np
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass



st.title('BBQ finder')

link = 'To get the full key/value list of possibilities, go search on [tagfinder](http://tagfinder.herokuapp.com/search?query=bbq&lang=en)'
st.markdown(link, unsafe_allow_html=True)

# Filtering area
area = st.text_input("Location", "Wallonie")

# Filtering tags
overpass = Overpass()
key = st.text_input("Key", "amenity")
value = st.text_input("Value", "bbq")
# selector = ['"amenity"="bbq"', '"leisure"="picnic_table"'][0]
selector = f'"{key}"="{value}"'

### Get the data ###
nominatim = Nominatim()
areaId = nominatim.query(area).areaId()
query = overpassQueryBuilder(area=areaId, elementType='node', selector=selector, out='body')
result = overpass.query(query)
coords = np.array([(i.lat(), i.lon()) for i in result.elements()])
# print(area, areaId, key, value, selector)

### Make the map ###
m = folium.Map(location=coords.mean(0))

# Add markers
for coord in coords:
    
    lat_lon = str(coord.tolist())[1:-1]
    folium.Marker(
        popup = f"Coordinnates: {lat_lon}",
        location=coord.tolist()
    ).add_to(m)

# Display m
folium_static(m)