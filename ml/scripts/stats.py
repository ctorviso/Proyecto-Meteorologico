import pandas as pd


def metrics_df(model_name, metrics):

    return pd.DataFrame({
        'Model': model_name,
        'MSE': metrics[0],
        'MAE': metrics[1],
        'RMSE': metrics[2],
        'R2': metrics[3],
    }, index=[0])


def daily_stats(y_pred, y_test, difference, test_dates_seq):

    predictions_df = pd.DataFrame({
        'fecha': test_dates_seq,
        'actual': y_test.flatten(),
        'predicted': y_pred.flatten(),
        'difference': difference
    })

    stats = predictions_df.groupby('fecha').agg({
        'actual': ['mean', 'min', 'max', 'std'],
        'predicted': ['mean', 'min', 'max', 'std']
    }).reset_index()

    stats.columns = ['fecha'] + ['_'.join(col).strip() for col in stats.columns[1:]]

    return stats
