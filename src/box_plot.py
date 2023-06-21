import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_box_plot
import plotly.colors


def overview_box_plot(filtered_df):

    fig = px.box(filtered_df, x="année", y="pages")
    color_palette = ["rgb(0, 0, 0)"] + plotly.colors.sequential.Viridis

    fig.update_layout(
        title={
            'text': "Box Plot of Number of Pages by Year",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        showlegend=True)
    fig.update_traces(
        hovertemplate=get_hover_box_plot(name_text=None),
        marker=dict(color=color_palette[3]))

    return fig

def mvd_box_plot(filtered_df_maitrise, filtered_df_doctorat, context_title):
    
    text = "Comparison of Number of Pages by Year for Maîtrise and Doctorat"
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
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        boxmode="group",
        showlegend=True)

    return fig