import pandas as pd

def load_datasets():
    
    train = pd.read_csv('../data/ml/train_scaled.csv', parse_dates=['fecha'])
    validation = pd.read_csv('../data/ml/validation_scaled.csv', parse_dates=['fecha'])
    test = pd.read_csv('../data/ml/test_scaled.csv', parse_dates=['fecha'])
    full = pd.read_csv('../data/ml/full_scaled.csv', parse_dates=['fecha'])
    
    train = train.drop(columns=['idema'])
    validation = validation.drop(columns=['idema'])
    test = test.drop(columns=['idema'])
    full = full.drop(columns=['idema'])
    
    train.set_index('fecha', inplace=True)
    validation.set_index('fecha', inplace=True)
    test.set_index('fecha', inplace=True)
    full.set_index('fecha', inplace=True)

    return train, validation, test, full


