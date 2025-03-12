import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def histogram(
        df,
        title: str,
        col: str,
        x_label: str,
        y_label: str = "Frecuencia"
) -> go.Figure:

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


def histograms(
        df: pd.DataFrame,
        title: str,
        cols: list,
        colors: list,
        x_label: str,
        y_label: str = "Frecuencia",
        nbins: int = 20
) -> go.Figure:

    df = df.dropna(subset=cols)

    fig = px.histogram(
        df,
        x=cols[0],
        nbins=nbins,
        title=title,
        template="plotly_white"
    )

    fig.data = []

    for i, col in enumerate(cols):
        fig.add_trace(
            go.Histogram(
                x=df[col],
                name=col,
                nbinsx=nbins,
                marker_color=colors[i],
                opacity=0.85,
                histnorm='probability density'
            )
        )

    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        barmode='group',
        bargap=0.1,
        bargroupgap=0,
        title_x=0.5
    )

    if len(cols) > 1:
        all_data = []
        for col in cols:
            all_data.extend(df[col].dropna().tolist())

        min_val = min(all_data)
        max_val = max(all_data)
        bin_width = (max_val - min_val) / nbins

        for trace in fig.data:
            trace.xbins = dict(
                start=min_val,
                end=max_val,
                size=bin_width
            )

    return fig

def scatter_matrix(
        df: pd.DataFrame,
        x_cols: list,
        y_cols: list,
        x_labels: list,
        y_labels: list,
        title: str,
        color: str,
        trendline: bool
) -> go.Figure:

    df = df.copy()
    df = df.sample(min(500, len(df)))
    df = df.dropna(subset=x_cols + y_cols)

    fig = make_subplots(
        rows=len(y_cols),
        cols=len(x_cols),
        shared_xaxes=True,
        shared_yaxes=True,
        horizontal_spacing=0.02,
        vertical_spacing=0.02
    )

    for i, y_col in enumerate(y_cols):
        y_label = y_labels[i]
        for j, x_col in enumerate(x_cols):
            x_label = x_labels[j]

            fig.add_trace(
                go.Scatter(
                    x=df[x_col],
                    y=df[y_col],
                    mode='markers',
                    marker=dict(
                        color=color,
                        size=5,
                        opacity=0.5
                    ),
                    name=f"{x_label} vs {y_label}"
                ),
                row=i + 1,
                col=j + 1
            )

            if trendline:
                fig.add_trace(
                    add_trendline(df, x_col, y_col),
                    row = i + 1,
                    col = j + 1
                )

            if i == len(y_cols) - 1:
                fig.update_xaxes(title_text=x_label, row=i + 1, col=j + 1)
            if j == 0:
                fig.update_yaxes(title_text=y_label, row=i + 1, col=j + 1)

    fig.update_layout(
        title=title,
        width=1300,
        height=800,
        showlegend=False
    )

    return fig


import plotly.graph_objects as go


def time_series(
        df: pd.DataFrame,
        title: str,
        cols: list,
        colors: list,
        x_label: str = "Fecha",
        y_label: str = "Valor",
        opacity: float = 0.85
) -> go.Figure:

    fig = go.Figure()

    for i, col in enumerate(cols):
        fig.add_trace(
            go.Scatter(
                x=df['fecha'],  # assuming 'fecha' is the column with time series data
                y=df[col],
                mode='lines',  # draw lines
                name=col,  # label in the legend
                line=dict(color=colors[i]),  # custom line color
                opacity=opacity  # custom line opacity
            )
        )

    fig.update_layout(
        title=title,
        xaxis_title=x_label,
        yaxis_title=y_label,
        template="plotly_white",
        title_x=0.5,
        showlegend=True
    )

    return fig


def add_trendline(df, x_col, y_col):

    slope, intercept = np.polyfit(df[x_col], df[y_col], 1)
    trendline = slope * df[x_col] + intercept

    return go.Scatter(
        x=df[x_col],
        y=trendline,
        mode='lines',
        line=dict(
            color='white',
            width=2,
            dash='dot'
        ),
        showlegend=False,
        opacity=0.8
    )

def bar_plots(
        sorted_data: pd.DataFrame,
        title: str,
        cols: list,
        x_label: str,
        y_label: str,
        label_maps: dict,
        colors: list
):

    fig = px.bar(
        sorted_data,
        x=sorted_data.index,
        y=cols,
        title=title,
        labels={'x': x_label, 'y': y_label},
        barmode='group'
    )

    for i, trace in enumerate(fig.data):
        col_name = trace.name
        if col_name in label_maps:
            trace.name = label_maps[col_name]
        trace.marker.color = colors[i]

    fig.update_layout(
        xaxis_tickangle=-45,
        title_x=0.5,
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend=dict(
            title='',
            orientation="h",
            yanchor="bottom",
            y=-0.6,
            xanchor="center",
            x=0.5,
            traceorder="normal",
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0)",
        )
    )

    return fig

def choropleth_map(
        avg_df: pd.DataFrame,
        selected_column: str,
        geojson: dict,
        label_maps: dict,
        choropleth_color_maps: dict
):

    fig = px.choropleth(
        data_frame=avg_df[['provincia_id', selected_column, 'provincia']],
        geojson=geojson,
        color=selected_column,
        locations='provincia_id',
        featureidkey="properties.provincia_id",
        labels={
            selected_column: label_maps[selected_column],
            'Provincia': 'provincia'
        },
        hover_data={'provincia': True, selected_column: True, 'provincia_id': False},
        color_continuous_scale=choropleth_color_maps[selected_column],
        hover_name='provincia',
    )

    fig.update_geos(
        center={"lat": 39.7, "lon": -3.2},
        projection_scale=20,
        showframe=False,
        resolution=50,
    )

    fig.update_layout(
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        geo=dict(
            showcoastlines=True,
            coastlinecolor="rgba(0, 0, 0, 0.2)",
            showland=True,
            landcolor="white",
            showocean=True,
            oceancolor="rgba(173, 216, 230, 0.4)",
            showcountries=True,
            countrycolor="rgba(0, 0, 0, 0.2)"
        ),
        coloraxis_colorbar=dict(
            thickness=15,
            len=0.7,
            xanchor="right",
            x=0,
            yanchor="middle",
            y=0.5,
            title=dict(
                text=label_maps[selected_column],
                side="right"
            ),
            outlinewidth=1,
        ),
        geo_showframe=True,
        geo_framecolor="rgba(150, 150, 150, 0.3)",
        geo_framewidth=2,
    )

    fig.update_traces(
        hovertemplate='<b>%{hovertext}</b><br>' +
                      f'{label_maps[selected_column]}: %{{z:.2f}}<extra></extra>'
    )

    fig.update_traces(marker_line_width=0.3, marker_line_color="rgba(0, 0, 0, 0.3)")

    return fig
