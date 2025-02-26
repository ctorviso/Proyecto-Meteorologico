import folium
import geopandas as gpd


def spain_map():
    m = folium.Map(
        location=[40.4168, -3.7038],
        zoom_start=6
    )
    return m

def set_map_bounds(m, geojson):
    gdf = gpd.GeoDataFrame.from_features(geojson["features"])
    bounds = gdf.total_bounds
    m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])


def get_column_choropleth(geojson, df, target_col: str, label: str, color: str):
    return folium.Choropleth(
        geo_data=geojson,
        data=df,
        columns=['provincia_id', target_col],
        key_on=f"properties.provincia_id",
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=label,
        highlight=True,
        reset_style_on_click=True
    )

def create_tooltip(
        col: str,
        col_label: str,
):
    return folium.GeoJsonTooltip(
        fields=['nombre', col],
        aliases=['Provincia:', col_label],
        localize=True,
        style=(
            "background-color: white; "
            "color: #333333; "
            "font-family: Arial, sans-serif; "
            "font-size: 12px; "
            "border: 1px solid gray; "
            "border-radius: 3px; "
            "padding: 5px;"
        ),
        max_width=800
    )