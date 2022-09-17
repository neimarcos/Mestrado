import requests
import geopandas as gpd
from shapely.geometry import shape

r = requests.get("https://data.cityofnewyork.us/resource/5rqd-h5ci.json")
r.raise_for_status()

data = r.json()
for d in data:
    d['the_geom'] = shape(d['the_geom'])

gdf = gpd.GeoDataFrame(data).set_geometry('the_geom')
gdf.head()