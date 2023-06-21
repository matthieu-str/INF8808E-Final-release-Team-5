import pandas as pd
import plotly.express as px
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ

def sunburst(df, mode):
    df['langue_new'] = df['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('the others')
    language_map = {"fr": "French", "en": "English", "the others": "the others"}
    df['langue_new'] = df['langue_new'].map(language_map)
    df_domain_languages = df.groupby(["domaine", "langue_new"], as_index=False).count()[
        ["domaine", "langue_new", "pages"]]
    df_domain_languages.rename(columns={"pages": "count"}, inplace=True)
    df_domain_uni = df.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "pages"]]
    df_domain_uni.rename(columns={"pages": "count"}, inplace=True)
    if mode == 'langue':
        fig = px.sunburst(df_domain_languages, path=['domaine', 'langue_new'], values='count', custom_data=['langue_new'])
        fig.update_layout(width=800, height=800)
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_langue()
        )
    elif mode == 'univ':
        fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count', custom_data=['univ'])
        fig.update_layout(width=800, height=800)
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ()
        )
    return fig