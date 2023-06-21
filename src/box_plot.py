import plotly.express as px
import plotly.graph_objects as go

def overview_box_plot(filtered_df):
    fig = px.box(filtered_df, x="année", y="pages")
    fig.update_layout(
        title="Box Plot of Number of Pages by Year",
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        showlegend=True)
    return fig

def mvd_box_plot(filtered_df_maitrise, filtered_df_doctorat):
    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=filtered_df_maitrise["année"],
            y=filtered_df_maitrise["pages"],
            name="Maîtrise"))
    fig.add_trace(
        go.Box(
            x=filtered_df_doctorat["année"],
            y=filtered_df_doctorat["pages"],
            name="Doctorat"))

    fig.update_layout(
        title="Comparison of Number of Pages by Year for Maîtrise and Doctorat",
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        boxmode="group",
        showlegend=True)
    return fig