import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_box_plot
import plotly.colors


def overview_box_plot(filtered_df, context_title):

    text =  "Diagramme en Boîte du nombre de pages par année"
    title_text = text + context_title
    fig = px.box(filtered_df, x="année", y="pages")
    color_palette = ["rgb(0, 0, 0)"] + plotly.colors.sequential.Viridis

    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Année",
        yaxis_title="Nombre de Pages",
        showlegend=True)
    fig.update_traces(
        hovertemplate=get_hover_box_plot(name_text=None),
        marker=dict(color=color_palette[3]))

    return fig

def mvd_box_plot(filtered_df_maitrise, filtered_df_doctorat, context_title):
    
    text = "Comparaison du nombre de pages par année à la Maîtrise et au Doctorat"
    title_text = text + context_title
    
    fig = go.Figure()
    master = "Maîtrise"
    phd = "Doctorat"
    color_palette = plotly.colors.qualitative.D3

    fig.add_trace(
        go.Box(
            x=filtered_df_maitrise["année"],
            y=filtered_df_maitrise["pages"],
            name=master,
            hovertemplate=get_hover_box_plot(name_text=master),
            marker=dict(color=color_palette[0])),)
    
    fig.add_trace(
        go.Box(
            x=filtered_df_doctorat["année"],
            y=filtered_df_doctorat["pages"],
            name=phd,
            hovertemplate=get_hover_box_plot(name_text=phd),
            marker=dict(color=color_palette[1])))

    fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Année",
        yaxis_title="Nombre de Pages",
        boxmode="group",
        showlegend=True)

    return fig
