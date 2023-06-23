import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ

def sunburst(df, mode):
    df['langue_new'] = df['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('the others')
    language_map = {"fr": "Français", "en": "Anglais", "the others": "the others"}
    df['langue_new'] = df['langue_new'].map(language_map)
    df = df[~df['domaine'].isin(['inclassable'])]
    df = df[~df['langue_new'].isin(['the others'])]

    df_domain_languages = df.groupby(["domaine", "langue_new"], as_index=False).count()[
        ["domaine", "langue_new", "pages"]]
    df_domain_languages.rename(columns={"pages": "count"}, inplace=True)

    df_domain_uni = df.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "pages"]]
    df_domain_uni.rename(columns={"pages": "count"}, inplace=True)
    # df_uni_grouped = df_domain_uni.groupby('domaine').apply(lambda x: x.nlargest(10, 'count')).reset_index(drop=True)
    # df_uni_others = df_domain_uni[~df_domain_uni.index.isin(df_uni_grouped.index)]
    # print(df_uni_others)
    # df_uni_others_grouped = df_uni_others.groupby('domaine')['count'].sum().reset_index()
    # df_uni_others_grouped['univ'] = 'the others'
    # df_uni_combined = pd.concat([df_uni_grouped, df_uni_others_grouped])


    if mode == 'langue':
        # fig = px.sunburst(df_domain_languages, path=['domaine', 'langue_new'], values='count', custom_data=['langue_new'])
        labels = []
        parents = []
        values = []

        for domain, domain_df in df_domain_languages.groupby('domaine'):
            domain_values = domain_df['count'].sum()
            labels.append(domain)
            parents.append('')
            values.append(domain_values)
            for row in domain_df.itertuples():
                labels.append(f"{domain}-{row.langue_new}")
                parents.append(domain)
                values.append(row.count)

        fig = go.Figure()
        fig.add_trace(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            maxdepth=2,
            branchvalues="total",
            insidetextorientation='horizontal',
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
            # marker=dict(
            #     colors=['rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)',
            #             'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)',
            #             'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)'],
            # ),
        ))
        fig.update_layout(width=800, height=800,
                          title='La répartition des langues dans différents domaines')
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_langue(),
        )

    elif mode == 'univ':
        # fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count', custom_data=['univ'])
        labels = []
        parents = []
        values = []

        for domain, domain_df in df_domain_uni.groupby('domaine'):
            domain_values = domain_df['count'].sum()
            top10_children = domain_df.nlargest(10, "count")

            labels.append(domain)
            parents.append('')
            values.append(domain_values)
            for row in top10_children.itertuples():
                labels.append(f"{domain}-{row.univ}")
                parents.append(domain)
                values.append(row.count)
            other_count = domain_values - top10_children["count"].sum()
            labels.append(f"{domain}-the others")
            parents.append(domain)
            values.append(other_count)


        fig = go.Figure()
        fig.add_trace(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            maxdepth=2,
            branchvalues="total",
            insidetextorientation='horizontal',
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
        ))

        fig.update_layout(width=800, height=800,
                          title='La répartition des 10 meilleures universités dans différents domaines')
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ(),
        )
    return fig