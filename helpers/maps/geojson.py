import glob
import json
import os
from helpers.config import script_dir


def read_provincias() -> dict:
    data = {}
    geojson_dir = os.path.join(script_dir, '../data/geojson/provincias')

    for file in glob.glob(os.path.join(geojson_dir, '*.geojson')):
        key = os.path.basename(file).removesuffix(".geojson")
        data[key] = {}
        with open(file, encoding="utf-8") as f:
            data[key] = json.load(f)

    return data



def update_properties(data: dict) -> dict:
    locations_file = os.path.join(script_dir, '../data/locations/provincias.json')

    with open(locations_file, encoding='utf-8') as f:
        loc_data = json.load(f)

    for key, value in loc_data.items():
        for feature in data[key]['features']:
            feature.setdefault('properties', {})
            feature['properties'].update(value)
            feature['properties']['provincia_id'] = key

    return data


def combine_features():
    data = read_provincias()
    data = update_properties(data)
    items = [v for k, v in data.items()]
    features = []
    for data in items:
        if data['features']:
            features.extend(data['features'])

    return features

geodata_provincias = {
    "type": "FeatureCollection",
    "features": combine_features()
}


def inject_col_values(df, cols):
    geodata = geodata_provincias.copy()
    for feature in geodata['features']:
        provincia_id = feature['properties']['provincia_id']
        matching_rows = df[df['provincia_id'] == provincia_id]
        row = matching_rows.iloc[0]
        for col in cols:
            feature['properties'][col] = row[col]

    return geodata
