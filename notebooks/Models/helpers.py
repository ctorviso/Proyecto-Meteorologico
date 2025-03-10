import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

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

def create_sequences(X, y, dates, n_days):
    
    X_seq, y_seq, dates_seq = [], [], []
    
    for i in range(n_days, len(X)):
        X_seq.append(X.iloc[i-n_days:i].values)
        y_seq.append(y.iloc[i])
        dates_seq.append(dates[i])
    
    X_seq = np.array(X_seq)
    y_seq = np.array(y_seq)
    
    return X_seq, y_seq, dates_seq

def inverse_predictions(y_pred_seq, y_test_seq, scaler_y_train):

    y_pred = scaler_y_train.inverse_transform(y_pred_seq.reshape(-1, 1))
    y_test = scaler_y_train.inverse_transform(y_test_seq.reshape(-1, 1))
    difference = y_pred.flatten() - y_test.flatten()

    return y_pred, y_test, difference

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
    
    daily_avg_predictions = predictions_df.groupby('fecha').agg({
        'actual': 'mean',
        'predicted': 'mean'
    }).reset_index()
    
    daily_stats = predictions_df.groupby('fecha').agg({
        'actual': ['mean', 'min', 'max', 'std'],
        'predicted': ['mean', 'min', 'max', 'std']
    }).reset_index()
    
    daily_stats.columns = ['fecha'] + ['_'.join(col).strip() for col in daily_stats.columns[1:]]
    
    return daily_stats

def daily_stats_comparison(model_name, daily_stats):
    
    fig = make_subplots(rows=2, cols=1, 
                       shared_xaxes=True,
                       subplot_titles=('Temperature Prediction Comparison', 'Prediction Error'),
                       row_heights=[0.7, 0.3],
                       vertical_spacing=0.1)
    
    fig.add_trace(
        go.Scatter(
            x=daily_stats['fecha'],
            y=daily_stats['actual_mean'],
            mode='lines+markers',
            name='Actual Temperature',
            line=dict(color='blue'),
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_stats['fecha'].tolist() + daily_stats['fecha'].tolist()[::-1],
            y=daily_stats['actual_max'].tolist() + daily_stats['actual_min'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(0, 0, 255, 0.1)',
            line=dict(color='rgba(0, 0, 255, 0)'),
            name='Actual Range (±std)',
            showlegend=True
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_stats['fecha'],
            y=daily_stats['predicted_mean'],
            mode='lines+markers',
            name='Predicted Temperature',
            line=dict(color='red'),
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=daily_stats['fecha'].tolist() + daily_stats['fecha'].tolist()[::-1],
            y=daily_stats['predicted_max'].tolist() + daily_stats['predicted_min'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.1)',
            line=dict(color='rgba(255, 0, 0, 0)'),
            name='Predicted Range (±std)',
            showlegend=True
        ),
        row=1, col=1
    )
    
    error = daily_stats['predicted_mean'] - daily_stats['actual_mean']
    fig.add_trace(
        go.Bar(
            x=daily_stats['fecha'],
            y=error,
            name='Prediction Error',
            marker_color='orange',
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=[daily_stats['fecha'].min(), daily_stats['fecha'].max()],
            y=[0, 0],
            mode='lines',
            line=dict(color='black', dash='dash'),
            showlegend=False
        ),
        row=2, col=1
    )
    
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error**2))
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.01, y=0.25,
        text=f"MAE: {mae:.2f}°<br>RMSE: {rmse:.2f}°",
        showarrow=False,
        font=dict(size=12),
        align="left",
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4
    )
    
    fig.update_layout(
        title=f'Daily Temperature Prediction Analysis ({model_name})',
        height=700,
        width=1300,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(title='Date'),
        xaxis2=dict(title='Date'),
        yaxis=dict(title='Temperature (°C)'),
        yaxis2=dict(title='Error (°C)')
    )
    
    return fig

def difference_histogram(model_name, difference):
    
    fig = go.Figure(data=[go.Histogram(
        x=difference,
        nbinsx=50,
        marker=dict(color='skyblue', line=dict(color='black', width=1))
    )])
    
    fig.update_layout(
        title=f'Histogram of Prediction Differences ({model_name})',
        xaxis_title='Difference (Predicted - Actual)',
        yaxis_title='Frequency',
        template='plotly_white',
        height=500,
        width=1300
    )

    return fig

def training_history(model_name, metrics):
    fig = make_subplots(rows=4, cols=1, subplot_titles=("Mean Squared Error (MSE)", "Mean Absolute Error (MAE)", "Root Mean Squared Error (RMSE)", "R2 Score"))
    
    row = 1
    for i, (metric, values) in enumerate([
        ('mse', metrics['loss']),
        ('val_mse', metrics['val_loss']), 
        ('mae', metrics['mean_absolute_error']),
        ('val_mae', metrics['val_mean_absolute_error']),
        ('rmse', metrics['root_mean_squared_error']),
        ('val_rmse', metrics['val_root_mean_squared_error']),
        ('r2', metrics['r2_score']),
        ('val_r2', metrics['val_r2_score'])
    ]):
        is_val = 'val' in metric
        fig.add_trace(
            go.Scatter(x=list(range(10)), y=values, name=metric, 
                      line=dict(dash='dash' if is_val else None, color='firebrick' if is_val else 'royalblue')),
            row=row, col=1
        )
        if is_val:
            row += 1
    
    fig.update_layout(height=1200, width=1000, title_text=f"Training History ({model_name})", legend=dict(orientation="h", y=1.1))
    fig.update_xaxes(title_text="Epoch", row=2, col=1)
    
    return fig

def training_history_scaled(model_name, scaled_metrics, metrics):
    
    fig = go.Figure()
    
    metric_pairs = [
        ('loss', 'val_loss', 'MSE'),
        ('mean_absolute_error', 'val_mean_absolute_error', 'MAE'),
        ('root_mean_squared_error', 'val_root_mean_squared_error', 'RMSE'),
        ('r2_score', 'val_r2_score', 'R2')
    ]
    
    colors = {
        'loss': 'blue', 'val_loss': 'lightblue',
        'mean_absolute_error': 'green', 'val_mean_absolute_error': 'lightgreen',
        'root_mean_squared_error': 'red', 'val_root_mean_squared_error': 'pink',
        'r2_score': 'purple', 'val_r2_score': 'violet'
    }
    
    for train_metric, val_metric, label in metric_pairs:
        fig.add_trace(
            go.Scatter(
                x=list(range(len(scaled_metrics))),
                y=scaled_metrics[train_metric],
                name=f"{label} (Train)",
                line=dict(color=colors[train_metric]),
                hovertemplate=f"{label} (Train): %{{y:.4f}}<br>Original: %{{customdata:.4f}}<extra></extra>",
                customdata=metrics[train_metric]
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=list(range(len(scaled_metrics))),
                y=scaled_metrics[val_metric],
                name=f"{label} (Val)",
                line=dict(color=colors[val_metric], dash='dash'),
                hovertemplate=f"{label} (Val): %{{y:.4f}}<br>Original: %{{customdata:.4f}}<extra></extra>",
                customdata=metrics[val_metric]
            )
        )
    
    fig.update_layout(
        title=f"Training History Scaled ({model_name})",
        xaxis_title="Epoch",
        yaxis_title="Scaled Metric Value",
        height=600,
        width=1000,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified"
    )
    
    return fig

def visualize_prophet_forecast(forecast_avg):
    
    fig = make_subplots(
        rows=3, 
        cols=1,
        subplot_titles=("Average Forecast with Confidence Interval", "Average Trend Component", "Average Seasonal Components"),
        vertical_spacing=0.1,
        row_heights=[0.5, 0.25, 0.25]
    )
    
    fig.add_trace(
        go.Scatter(
            x=forecast_avg['ds'], 
            y=forecast_avg['yhat'],
            mode='lines',
            name='Average Forecast',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_avg['ds'], forecast_avg['ds'].iloc[::-1]]),
            y=pd.concat([forecast_avg['yhat_upper'], forecast_avg['yhat_lower'].iloc[::-1]]),
            fill='toself',
            fillcolor='rgba(0, 176, 246, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'
        ),
        row=1, col=1
    )
    
    actual_points = forecast_avg[forecast_avg['y'].notnull()]

    fig.add_trace(
        go.Scatter(
            x=actual_points['ds'],
            y=actual_points['y'],
            mode='markers',
            name='Actual Values',
            marker=dict(color='black', size=4)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=forecast_avg['ds'],
            y=forecast_avg['trend'],
            mode='lines',
            name='Average Trend',
            line=dict(color='darkblue')
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_avg['ds'], forecast_avg['ds'].iloc[::-1]]),
            y=pd.concat([forecast_avg['trend_upper'], forecast_avg['trend_lower'].iloc[::-1]]),
            fill='toself',
            fillcolor='rgba(0, 0, 139, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Trend Confidence Interval',
            showlegend=False
        ),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=forecast_avg['ds'],
            y=forecast_avg['weekly'],
            mode='lines',
            name='Weekly Pattern',
            line=dict(color='green')
        ),
        row=3, col=1
    )
        
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_avg['ds'], forecast_avg['ds'].iloc[::-1]]),
            y=pd.concat([forecast_avg['weekly_upper'], forecast_avg['weekly_lower'].iloc[::-1]]),
            fill='toself',
            fillcolor='rgba(0, 128, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Weekly Confidence Interval',
            showlegend=False
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=forecast_avg['ds'],
            y=forecast_avg['yearly'],
            mode='lines',
            name='Yearly Pattern',
            line=dict(color='red')
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_avg['ds'], forecast_avg['ds'].iloc[::-1]]),
            y=pd.concat([forecast_avg['yearly_upper'], forecast_avg['yearly_lower'].iloc[::-1]]),
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Yearly Confidence Interval',
            showlegend=False
        ),
        row=3, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=forecast_avg['ds'],
            y=forecast_avg['additive_terms'],
            mode='lines',
            name='All Seasonal Components',
            line=dict(color='purple')
        ),
        row=3, col=1
    )
        
    fig.add_trace(
        go.Scatter(
            x=pd.concat([forecast_avg['ds'], forecast_avg['ds'].iloc[::-1]]),
            y=pd.concat([forecast_avg['additive_terms_upper'], forecast_avg['additive_terms_lower'].iloc[::-1]]),
            fill='toself',
            fillcolor='rgba(128, 0, 128, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='Seasonal Confidence Interval',
            showlegend=False
        ),
        row=3, col=1
    )
    
    fig.update_layout(
        title="Prophet Forecast (Daily Average)",
        xaxis_title="Date",
        yaxis_title="Value",
        height=900,
        width=1000,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        template="plotly_white",
    )

    fig.update_yaxes(title_text="Value", row=1, col=1)
    fig.update_yaxes(title_text="Trend", row=2, col=1)
    fig.update_yaxes(title_text="Seasonal Effects", row=3, col=1)
    
    return fig
