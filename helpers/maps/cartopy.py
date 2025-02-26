from typing import Optional
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
from matplotlib import pyplot as plt
from helpers.maps.geojson import geodata_provincias
from helpers.lookups import provincias


def add_region(ax: plt.Axes, geojson, alpha: float = 0, color: Optional[str] = None):
    for feature in geojson["features"]:
        coords = feature["geometry"]["coordinates"]
        geom_type = feature["geometry"]["type"]

        if geom_type == "Polygon":
            polygons = [coords]
        elif geom_type == "MultiPolygon":
            polygons = coords
        else:
            continue

        for polygon in polygons:
            for ring in polygon:
                lons, lats = zip(*ring)
                ax.plot(lons + (lons[0],), lats + (lats[0],), transform=ccrs.PlateCarree(), color='black',
                        linewidth=.5)
                ax.fill(lons, lats, transform=ccrs.PlateCarree(), color=color, alpha=alpha, linewidth=0)

# noinspection PydanticTypeChecker,PyTypeChecker
def spain_outline():
    fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

    inset_ax = fig.add_axes((0.68, 0.15, 0.2, 0.2), projection=ccrs.PlateCarree())
    inset_ax.set_extent([-19, -12, 27, 30], crs=ccrs.PlateCarree())

    for provincia_id, geojson in geodata_provincias.items():
        if provincia_id not in ['35', '38']:
            add_region(ax, geojson)
        else:
            add_region(inset_ax, geojson)

    return fig, ax, inset_ax


def add_area(provincia_id, ax, inset_ax, handles, alpha: float = 0.5, color: str = 'blue'):
    provincia = provincias[provincia_id]['nombre']

    if any(handle.get_label() == provincia for handle in handles):
        return

    if provincia_id in ['35', '38']:  # Islas Canarias
        add_region(inset_ax, geodata_provincias[provincia_id], alpha=alpha, color=color)
    else:
        add_region(ax, geodata_provincias[provincia_id], alpha=alpha, color=color)

    handles.append(mpatches.Patch(label=provincia, color=color))
