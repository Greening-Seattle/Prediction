import adjustText as aT
import geopandas as gpd
from geopandas.tools import geocode
from greendata import get_zips
import matplotlib 
from matplotlib import pyplot as plt
from shapely.geometry import Point

def plot_zips():
    
    zips_map = get_zips()
    zips_map["center"] = zips_map["geometry"].centroid
    zips_points = zips_map.copy()
    zips_points.reset_index(inplace=True)
    
    ax = zips_map.plot(figsize = (20, 21), color = "whitesmoke", edgecolor = "darkgreen", linewidth = 1)
    ax.set_ylabel('Latitude')
    ax.set_xlabel('Longitude')
    ax.set_title('Seattle Metro Area ZIP Codes')
    texts = []

    for x, y, label in zip(zips_points.center.x, zips_points.center.y, zips_points['ZIPCODE']):
        texts.append(plt.text(x, y, label, fontsize = 10))
    
    aT.adjust_text(texts, expand_points=(1,1), expand_text=(1,1), 
               arrowprops=dict(arrowstyle="-", color='white', lw=0.5))

    return
  
  ##Format for code obtained from: https://github.com/shotleft/how-to-python/blob/master/How%20it%20works%20-%20labelling%20districts%20in%20GeoPandas.ipynb
