import pandas as pd
import numpy as np
import sys
sys.path.append('..')
from helpers import lookups


def clean_df(df: pd.DataFrame) -> pd.DataFrame:

    df_clean = df.copy()

    df_clean = df_clean.drop(columns=lookups.time_cols)

    numeric_cols = df_clean.drop(columns=['fecha', 'idema']).columns

    df_clean[numeric_cols] = df_clean[numeric_cols].apply(pd.to_numeric, errors='coerce')
    
    df_clean['year'] = df_clean['fecha'].dt.year
    df_clean['fecha_day'] = df_clean['fecha'].dt.dayofyear
    
    df_clean['fecha_sin'] = df_clean.apply(lambda row: np.sin(2 * np.pi * row['fecha_day'] / 366) if row['year'] % 4 == 0 \
                                           else np.sin(2 * np.pi * row['fecha_day'] / 365), axis=1)
    df_clean['fecha_cos'] = df_clean.apply(lambda row: np.cos(2 * np.pi * row['fecha_day'] / 366) if row['year'] % 4 == 0 \
                                           else np.cos(2 * np.pi * row['fecha_day'] / 365), axis=1)
    
    df_clean['year'] = (df_clean['year'] - 1950) / 100

    df_clean['dir_sin'] = df_clean.apply(lambda row: np.sin(2 * np.pi * row['dir'] / 99), axis=1)
    df_clean['dir_cos'] = df_clean.apply(lambda row: np.cos(2 * np.pi * row['dir'] / 99), axis=1)

    df_clean = df_clean.drop(columns=['dir', 'fecha_day', 'sol', 'pres_max', 'pres_min', 'hr_max', 'hr_min'])
    
    df_clean = df_clean.merge(lookups.locations_df[['idema', 'latitud', 'longitud', 'altitud']], on='idema', how='left')
    
    location_cols = ['latitud', 'longitud', 'altitud']
    df_clean[location_cols] = df_clean[location_cols].apply(pd.to_numeric, errors='coerce')
    
    df_clean = df_clean.round(4)

    return df_clean
