import numpy as np
import pandas as pd
import os
from helpers.config import script_dir
from helpers.lookups import float_cols, int_cols, time_cols, numeric_cols, locations_df
from helpers.preprocessing import convert_numeric


def clean_historical(df: pd.DataFrame):
    df = df.drop(columns=['nombre', 'provincia', 'altitud', 'horaPresMax', 'horaPresMin'])
    df = df.rename(columns={'indicativo': 'idema',
                        'hrMax': 'hr_max', 'hrMedia': 'hr_media', 'hrMin': 'hr_min',
                        'horaHrMax': 'hora_hr_max', 'horaHrMin': 'hora_hr_min',
                        'presMax': 'pres_max', 'presMin': 'pres_min',
                        'horatmax': 'hora_tmax', 'horatmin': 'hora_tmin',
                        'horaracha': 'hora_racha'
                       })

    df = df.replace({'Varias': np.nan})

    df[float_cols] = df[float_cols].apply(lambda x: x.str.replace(',', '.', regex=False))
    df[float_cols] = df[float_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df[float_cols] = df[float_cols].apply(pd.to_numeric, errors='coerce')

    df[int_cols] = df[int_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df[int_cols] = df[int_cols].apply(pd.to_numeric, errors='coerce')

    df[time_cols] = df[time_cols].apply(lambda col: pd.to_datetime(col, format='%H:%M', errors='coerce').dt.time)

    df = df.replace({pd.NaT: None, np.nan: None, pd.NA: None})

    return df

def provincia_avg_diario(df):
    df = df.merge(locations_df[['idema', 'provincia_id']], on='idema', how='left')
    cols = numeric_cols + ['provincia_id', 'fecha']
    df = df[cols]

    df['provincia_id'] = df['provincia_id'].astype(str)
    df = convert_numeric(df, numeric_cols)

    df = df.groupby(['provincia_id', 'fecha']).agg({
        **{col: 'mean' for col in df.select_dtypes(include=['number']).columns if col not in ['provincia_id', 'fecha']}
    }).reset_index().round(2)

    df = df.replace({pd.NaT: None, np.nan: None, pd.NA: None})

    return df


def sort_historical(year):
    historico_path = os.path.join(script_dir, f'../data/historical/historico/{year}.csv')

    df = pd.read_csv(historico_path)
    df = df.sort_values(by="fecha")
    df.to_csv(historico_path, index=False)

def sort_historico_avg(year):
    historico_avg_path = os.path.join(script_dir, f'../data/historical/historico_avg/{year}.csv')

    avg_df = pd.read_csv(historico_avg_path)
    avg_df = avg_df.sort_values(by=["fecha", "provincia_id"])
    avg_df.to_csv(historico_avg_path, index=False)

sort_historico_avg(2019)