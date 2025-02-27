import plotly.express as px

def histograma(df, title: str, col: str, x_label: str, y_label: str = "Frecuencia"):
    fig = px.histogram(
        df,
        x=col,
        nbins=20,
        title=title,
        labels={col: x_label},
        template="plotly_white"
    )
    fig.update_traces(
        marker_color='purple',
        marker_line_color='black',
        marker_line_width=1.5,
        opacity=0.85
    )
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )
    return fig
