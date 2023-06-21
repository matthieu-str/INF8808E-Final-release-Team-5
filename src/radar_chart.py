import pandas as pd
import numpy as np
import plotly.graph_objs as go
from hover_template import get_hover_univ, get_hover_discipline

df = pd.read_csv('assets/data/thesesMemoiresQC2000-2022-v20230508-1.csv')

def update_graph(mode):
    x = "maîtrise"
    y = "doctorat"

    if mode == 'univ':
        x_freq = df[df["grade"] == x].groupby('univ').size()
        y_freq = df[df["grade"] == y].groupby('univ').size()
        
        universities = df['univ'].unique().tolist()

        hovertext_master, hovertext_doctorat = get_hover_univ(x_freq, y_freq, universities)
        
        data = [
            go.Scatterpolar(
                r = [np.log10(x_freq[uni]+1) if uni in x_freq else 0 for uni in universities],
                theta = universities,
                fill = 'toself',
                name = x,
                hoverinfo='text',
                hovertext=hovertext_master
            ),
            go.Scatterpolar(
                r = [np.log10(y_freq[uni]+1) if uni in y_freq else 0 for uni in universities],
                theta = universities,
                fill = 'toself',
                name = y,
                hoverinfo='text',
                hovertext=hovertext_doctorat
            )
        
        ]
        layout = go.Layout(
            polar = dict(
                radialaxis = dict(
                    visible = True,
                    range = [0, max(np.log10(x_freq.max()+1), np.log10(y_freq.max()+1))],
                    tickfont=dict(size=13)  # Increase the font size
                )
            ),
            showlegend = True,
            title = f"{x} vs {y} by University",
            legend=dict(x=.8, y=1),  # Adjust position of the legend
            annotations=[
                dict(
                    text="Radial axis in logarithmic scale",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=-0.2  # Position of the annotation
                )
            ]
        )

    else:
        x_freq = df[df["grade"] == x].groupby('discipline').size()
        y_freq = df[df["grade"] == y].groupby('discipline').size()

        freq_df = pd.DataFrame({'x_freq': x_freq, 'y_freq': y_freq}).fillna(0)
        freq_df['total_freq'] = freq_df['x_freq'] + freq_df['y_freq']
        freq_df = freq_df.nlargest(10, 'total_freq')

        universities = freq_df.index.tolist()
        x_freq = freq_df['x_freq'].tolist()
        y_freq = freq_df['y_freq'].tolist()

        hovertemplate_master, hovertemplate_doctorat = get_hover_discipline()
        
        data = [
            go.Scatterpolar(
                r = x_freq,
                theta = universities,
                fill = 'toself',
                name = x,
                hovertemplate = hovertemplate_master
            ),
            go.Scatterpolar(
                r = y_freq,
                theta = universities,
                fill = 'toself',
                name = y,
                hovertemplate = hovertemplate_doctorat
            )
        ]
        layout = go.Layout(
            polar = dict(
                radialaxis = dict(
                    visible = True,
                    range = [0, max(x_freq + y_freq)]
                )
            ),
            showlegend = True,
            title = f"{x} vs {y} by top 10 discipline"
        )

    return {'data': data, 'layout': layout}
def init_figure():
    """
    Function to initialize figure with 'univ' mode.
    
    Returns:
    Polar plot for university data.
    """
    try:
        return update_graph('univ')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
