import pandas as pd
import joblib
import os
import sys
sys.path.append('..')
from helpers.config import script_dir


def scale_df(df: pd.DataFrame) -> pd.DataFrame:

    df_unscaled = df.copy()

    scaler_path = os.path.join(script_dir, '../ml_scripts/minmax_scaler.joblib')

    scaler = joblib.load(scaler_path)
    
    data_scaled = scaler.transform(df_unscaled.drop(columns=['year']))
    
    df_scaled = pd.DataFrame(data_scaled, columns=df_unscaled.drop(columns=['year']).columns)

    df_scaled['year'] = df_unscaled['year'].values

    df_scaled = df_scaled.set_index(df_unscaled.index)

    df_scaled = df_scaled.round(4)

    return df_scaled
    