import pandas as pd
import plotly.express as px

def sunburst(df, mode):
    df['langue_new'] = df['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('the others')
    df_domain_languages = df.groupby(["domaine", "langue_new"], as_index=False).count()[
        ["domaine", "langue_new", "pages"]]
    df_domain_languages.rename(columns={"pages": "count"}, inplace=True)
    df_domain_uni = df.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "pages"]]
    df_domain_uni.rename(columns={"pages": "count"}, inplace=True)
    if mode == 'langue':
        fig = px.sunburst(df_domain_languages, path=['domaine', 'langue_new'], values='count')
        fig.update_layout(width=800, height=800)
    elif mode == 'univ':
        fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count')
        fig.update_layout(width=800, height=800)
    return fig