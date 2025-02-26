import folium
import pandas as pd
from helpers.maps.cartopy import geodata_provincias
from helpers.lookups import element_cols_map, label_maps, color_maps


def spain_map():
    m = folium.Map(location=[40, -3], zoom_start=6)
    return m

def add_to_map(m: folium.Map, df, target_col: str, label: str, color: str):
    return folium.Choropleth(
        geo_data=geodata_provincias,
        data=df,
        columns=['provincia_id', target_col],
        key_on=f"properties.provincia_id",
        fill_color=color,
        fill_opacity=1.0,
        line_opacity=0.2,
        legend_name=label,
        highlight=True,
        reset_style_on_click=True
    ).add_to(m)

def add_map_data(m: folium.Map, avg_df: pd.DataFrame, element: str) -> None:
    """Groups historical data by provincia and adds it to the map"""
    for col in element_cols_map[element]:
        add_to_map(m=m, df=avg_df, target_col=col, label=label_maps[col], color=color_maps[col])
