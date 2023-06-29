import pandas as pd
import numpy as np
import plotly.graph_objs as go
from hover_template import get_hover_univ, get_hover_discipline


def update_graph(df, mode):
     """
    Function to generate the radar graph and layout based on the selected mode .

    Args:
    df: The DataFrame containing the data to be plotted.
    mode (str): The mode to generate graph. It can be either 'univ' or 'discipline'.
    
    Returns:
    The radar graph with the layout.
    """
    x = "maîtrise"
    y = "doctorat"

    if mode == 'univ':
        x_freq = df[df["grade"] == x].groupby('univ').size()
        y_freq = df[df["grade"] == y].groupby('univ').size()

        universities = df['univ'].unique().tolist()

        hovertext_master, hovertext_doctorat = get_hover_univ(
            x_freq, y_freq, universities
        )

        data = [
            go.Scatterpolar(
                r=[
                    np.log10(x_freq.get(uni, 0) + 1) for uni in universities
                ],
                theta=universities,
                fill='toself',
                name=x,
                hoverinfo='text',
                hovertext=hovertext_master
            ),
            go.Scatterpolar(
                r=[
                    np.log10(y_freq.get(uni, 0) + 1) for uni in universities
                ],
                theta=universities,
                fill='toself',
                name=y,
                hoverinfo='text',
                hovertext=hovertext_doctorat
            )
        ]

        max_range = max(
            np.log10(x_freq.max() + 1),
            np.log10(y_freq.max() + 1)
        )

        layout = go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_range],
                    tickfont=dict(size=13)  # Increase the font size
                )
            ),
            showlegend=True,
            title=(f"Le nombre de grades de {x} et de {y}"
                   " pour chaque université"),
            legend=dict(
                x=.8,
                y=1,
                title=dict(text="Niveau d'études")
            ),
            annotations=[
                dict(
                    text="Axe radial en échelle logarithmique",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2  # Position of the annotation
                )
            ]
        )

    else:
        x_freq = df[df["grade"] == x].groupby('discipline').size()
        y_freq = df[df["grade"] == y].groupby('discipline').size()

        freq_df = pd.DataFrame(
            {'x_freq': x_freq, 'y_freq': y_freq}
        ).fillna(0)
        freq_df = freq_df.assign(total_freq=freq_df.sum(axis=1))
        freq_df = freq_df.nlargest(10, 'total_freq')

        universities = freq_df.index.tolist()
        x_freq = freq_df['x_freq'].tolist()
        y_freq = freq_df['y_freq'].tolist()

        hovertemplate_master, hovertemplate_doctorat = get_hover_discipline()

        data = [
            go.Scatterpolar(
                r=x_freq,
                theta=universities,
                fill='toself',
                name=x,
                hovertemplate=hovertemplate_master
            ),
            go.Scatterpolar(
                r=y_freq,
                theta=universities,
                fill='toself',
                name=y,
                hovertemplate=hovertemplate_doctorat
            )
        ]

        layout = go.Layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(x_freq + y_freq)]
                )
            ),
            showlegend=True,
            title=(f"Les dix premières disciplines pour {x} and {y}"),
            legend=dict(
                x=.8,
                y=1,
                title=dict(text="Niveau d'études")
            )
        )

    return {'data': data, 'layout': layout}


def init_figure(df):
    """
    Function to initialize figure with 'univ' mode.

    Returns:
    Polar plot for university data.
    """
    try:
        return update_graph(df, 'univ')
    except KeyError as error:
        print(f"KeyError occurred: {error}")
        return None
