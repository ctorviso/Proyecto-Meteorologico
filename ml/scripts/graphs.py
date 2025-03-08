import numpy as np
import plotly.graph_objects as go

def plot_forecast(
        historical_dates,
        historical,
        future_dates,
        predictions,
        predict_start):

    fig = go.Figure()

    all_dates = np.concatenate([historical_dates, future_dates])
    all_temps = np.concatenate([historical, predictions])

    # Create a color array
    colors = ['#1F77B4'] * len(historical_dates) + ['#FF4B4B'] * len(future_dates)

    fig.add_trace(
        go.Scatter(
            x=all_dates,
            y=all_temps,
            mode='lines+markers',
            line=dict(color='#1F77B4', width=3),
            marker=dict(
                size=8,
                color=colors
            ),
            showlegend=False
        )
    )

    fig.add_vline(x=predict_start, line_width=1, line_dash="dash", line_color="red")

    fig.update_layout(
        title=f'Predicción de Temperatura Media (tmed) a partir de {predict_start.strftime("%Y-%m-%d")}',
        xaxis_title='Date',
        yaxis_title='Temperatura Media (tmed) (°C)',
        template='plotly_white',
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode='x unified'
    )

    return fig
