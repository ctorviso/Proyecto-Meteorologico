import numpy as np
import pandas as pd


def clean_historical(df: pd.DataFrame):
    df.drop(columns=['nombre', 'provincia', 'sol', 'altitud', 'presMax', 'horaPresMax', 'presMin', 'horaPresMin'],
            inplace=True)
    df = df.rename(columns={'indicativo': 'idema',
                            'hrMax': 'hr_max', 'hrMedia': 'hr_media', 'hrMin': 'hr_min',
                            'horaHrMax': 'hora_hr_max', 'horaHrMin': 'hora_hr_min'})

    df = df.replace({'Varias': np.nan})

    float_cols = ['tmed', 'prec', 'tmin', 'tmax', 'velmedia', 'racha']
    df[float_cols] = df[float_cols].apply(lambda x: x.str.replace(',', '.', regex=False))
    df[float_cols] = df[float_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df[float_cols] = df[float_cols].apply(pd.to_numeric, errors='coerce')

    int_cols = ['hr_media', 'hr_min', 'hr_max']
    df[int_cols] = df[int_cols].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df[int_cols] = df[int_cols].apply(pd.to_numeric, errors='coerce')

    time_cols = ['horatmin', 'horatmax', 'horaracha', 'hora_hr_max', 'hora_hr_min']
    df[time_cols] = df[time_cols].apply(lambda col: pd.to_datetime(col, format='%H:%M', errors='coerce').dt.time)

    zero_cols = ['dir', 'hr_max', 'hr_min', 'hr_media']
    df[zero_cols] = df[zero_cols].fillna(0)

    df = df.replace({pd.NaT: None, np.nan: None, pd.NA: None})

    return df
