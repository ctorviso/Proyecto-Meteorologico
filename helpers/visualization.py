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
        color: str
) -> go.Figure:

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
                        size=6,
                        opacity=0.7
                    ),
                    name=f"{x_label} vs {y_label}"
                ),
                row=i + 1,
                col=j + 1
            )

            if i == len(y_cols) - 1:
                fig.update_xaxes(title_text=x_label, row=i + 1, col=j + 1)
            if j == 0:  # First column
                fig.update_yaxes(title_text=y_label, row=i + 1, col=j + 1)

    fig.update_layout(
        title=title,
        width=1300,
        height=800,
        showlegend=False
    )

    return fig