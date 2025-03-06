import pandas as pd
import numpy as np
import os
import sys
sys.path.append('..')
from helpers.config import script_dir


_li_cols = ['tmed', 'tmin', 'tmax', 'prec', 'hr_media']
_knn_cols = ['velmedia', 'racha', 'dir_sin', 'dir_cos']

_lookup_dir = os.path.join(script_dir, '../data/locations/estacion_distance_lookup.csv')
_lookup = pd.read_csv(_lookup_dir)


def _impute_knn(df, k=4):

    for fecha in df['fecha'].unique():
        fecha_data = df[df['fecha'] == fecha]

        for col in _knn_cols:
            nan_mask = fecha_data[col].isna()

            for index, row in fecha_data[nan_mask].iterrows():
                nearest_idemas = _lookup[row['idema']]
                nearest_values = fecha_data[fecha_data['idema'].isin(nearest_idemas)][col][:k]

                if not nearest_values.empty:
                    imputed_value = nearest_values.mean()
                    df.loc[index, col] = imputed_value

    return df


def impute_df(df: pd.DataFrame) -> pd.DataFrame:

    df_imputed = df.copy()
    
    df_imputed[_li_cols] = df_imputed[_li_cols].interpolate(method='linear', axis=0)

    df_imputed = _impute_knn(df_imputed)
    df_imputed = df_imputed.interpolate(method='linear', axis=0)

    df_imputed = df_imputed.drop(columns=['idema'])
    df_imputed = df_imputed.round(4)

    return df_imputed
