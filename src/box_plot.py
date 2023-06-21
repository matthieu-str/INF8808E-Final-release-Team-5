import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_box_plot


def overview_box_plot(filtered_df):

    fig = px.box(filtered_df, x="année", y="pages")
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
        hovertemplate=get_hover_box_plot(),
        marker=dict(color='black'))

    return fig

def mvd_box_plot(filtered_df_maitrise, filtered_df_doctorat):

    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=filtered_df_maitrise["année"],
            y=filtered_df_maitrise["pages"],
            name="Maîtrise",
            hovertemplate=get_hover_box_plot()),
        )
    fig.add_trace(
        go.Box(
            x=filtered_df_doctorat["année"],
            y=filtered_df_doctorat["pages"],
            name="Doctorat",  
            hovertemplate=get_hover_box_plot()),
        )

    fig.update_layout(
        title={
            'text': "Comparison of Number of Pages by Year for Maîtrise and Doctorat",
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        boxmode="group",
        showlegend=True)

    return fig