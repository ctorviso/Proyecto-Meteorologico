import plotly.graph_objects as go


def plot_forecast(result_df, predict_start):
    fig = go.Figure()

    historical = result_df[result_df['fecha'] <= predict_start]
    future = result_df[result_df['fecha'] > predict_start]

    marker_size = 4 if len(historical) < 50 else 0
    line_width = 3 if len(historical) < 50 else 2

    fig.add_trace(
        go.Scatter(
            x=historical['fecha'],
            y=historical['historical_tmed'],
            mode='lines+markers',
            line=dict(color='#1F77B4', width=line_width),
            marker=dict(size=marker_size, color='#1F77B4'),
            name='Historical Data',
            showlegend=True
        )
    )

    gru_future = future[~future['gru_tmed'].isna()]
    gru_x = [historical['fecha'].iloc[-1]] + list(gru_future['fecha'])
    gru_y = [historical['historical_tmed'].iloc[-1]] + list(gru_future['gru_tmed'])

    lstm_future = future[~future['lstm_tmed'].isna()]
    lstm_x = [historical['fecha'].iloc[-1]] + list(lstm_future['fecha'])
    lstm_y = [historical['historical_tmed'].iloc[-1]] + list(lstm_future['lstm_tmed'])

    simple_rnn_future = future[~future['simple_rnn_tmed'].isna()]
    simple_rnn_x = [historical['fecha'].iloc[-1]] + list(simple_rnn_future['fecha'])
    simple_rnn_y = [historical['historical_tmed'].iloc[-1]] + list(simple_rnn_future['simple_rnn_tmed'])

    fig.add_trace(
        go.Scatter(
            x=gru_x,
            y=gru_y,
            mode='lines+markers',
            line=dict(color='#FF4B4B', width=line_width),
            marker=dict(size=marker_size, color='#FF4B4B'),
            name='GRU Prediction',
            showlegend=True
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lstm_x,
            y=lstm_y,
            mode='lines+markers',
            line=dict(color='#FFA15A', width=line_width),
            marker=dict(size=marker_size, color='#FFA15A'),
            name='LSTM Prediction',
            showlegend=True
        )
    )

    fig.add_trace(
        go.Scatter(
            x=simple_rnn_x,
            y=simple_rnn_y,
            mode='lines+markers',
            line=dict(color='#FFD700', width=line_width),
            marker=dict(size=marker_size, color='#FFD700'),
            name='SimpleRNN Prediction',
            showlegend=True
        )
    )

    prophet_future = future[~future['prop_tmed'].isna()]

    prophet_x = [historical['fecha'].iloc[-1]] + list(prophet_future['fecha'])
    prophet_y = [historical['historical_tmed'].iloc[-1]] + list(prophet_future['prop_tmed'])

    fig.add_trace(
        go.Scatter(
            x=prophet_x,
            y=prophet_y,
            mode='lines+markers',
            line=dict(color='#2CA02C', width=line_width),  # Green color for Prophet
            marker=dict(size=marker_size, color='#2CA02C'),
            name='Prophet Prediction',
            showlegend=True
        )
    )

    fig.add_vline(x=predict_start, line_width=1, line_dash="dash", line_color="red")

    fig.update_layout(
        title=f'Predicción de Temperatura Media (tmed)',
        xaxis_title='Date',
        yaxis_title='Temperatura Media (tmed) (°C)',
        template='plotly_white',
        height=500,
        margin=dict(l=20, r=20, t=50, b=20),
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    return fig