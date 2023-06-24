import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ


def sunburst(df, mode):
    df_sun = df
    df_sun['langue_new'] = df_sun['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('autres langues')
    language_map = {"fr": "français", "en": "anglais", "autres langues": "autres langues"}
    df_sun['langue_new'] = df_sun['langue_new'].map(language_map)
    # df = df[~df['domaine'].isin(['inclassable'])]
    df_sun = df_sun[~df_sun['langue_new'].isin(['autres langues'])]
    df_domain_languages = df_sun.groupby(["domaine", "langue_new"], as_index=False).count()[
        ["domaine", "langue_new", "grade"]]
    df_domain_languages.rename(columns={"grade": "count"}, inplace=True)
    df_domain_uni = df_sun.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "grade"]]
    df_domain_uni.rename(columns={"grade": "count"}, inplace=True)
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
            if domain == 'programme individualisé ou inconnu':
                continue
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
            insidetextfont=dict(
                size=14,
                color='white'
            ),
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
            # marker=dict(
            #     colors=['rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)',
            #             'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)',
            #             'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)'],
            # ),
        ))
        fig.update_layout(width=700, height=700,
                          title='La répartition des langues dans différents domaines',
                          annotations=[dict(
                            text="Cliquez sur chaque partie de domaine pour voir plus de détails.",                  
                            x=-0.05, y=1.05,
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            ),
                            dict(
                            text="Note: La classe de domaine du programme individualisé et les autres langues ont été exclues parce qu'elles sont illisibles.",
                            x=-0.15, y=-0.1,
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            )]
                         )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_langue(),
            leaf=dict(opacity=1),
           )

    elif mode == 'univ':
        # fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count', custom_data=['univ'])
        labels = []
        parents = []
        values = []

        for domain, domain_df in df_domain_uni.groupby('domaine'):
            if domain == 'programme individualisé ou inconnu':
                continue
                """for row in top2_children.itertuples():
                    labels.append(f"{domain}-{row.univ}")
                    parents.append(domain)
                    values.append(row.count)
                other_count = domain_values - top2_children["count"].sum()
                labels.append(f"{domain}-Autres universités")
                parents.append(domain)
                values.append(other_count)"""
            
            domain_values = domain_df['count'].sum()
            top5_children = domain_df.nlargest(5, "count")
            """top2_children = domain_df.nlargest(2, "count")"""
            labels.append(domain)
            parents.append('')
            values.append(domain_values)


            for row in top5_children.itertuples():
                labels.append(f"{domain}-{row.univ}")
                parents.append(domain)
                values.append(row.count)
            other_count = domain_values - top5_children["count"].sum()
            labels.append(f"{domain}-Autres universités")
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
            insidetextfont=dict(
                size=14,
                color='white'
                ),
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
        ))

        fig.update_layout(width=700, height=700,
                          title='La répartition des meilleures universités dans différents domaines',
                          annotations=[dict(
                              text='Cliquez sur chaque partie de domaine pour voir plus de détails.',
                              x=-0.05, y=1.05,
                              showarrow=False,
                              font=dict(size=12, color='black'),
                          ),
                            dict(
                            text="Note: La classe de domaine du programme individualisé a été exclue car elle est illisible.",
                            x=-0.15, y=-0.1,
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            )]
                          )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ(),
            leaf=dict(opacity=1),
        )
    return fig



"""import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ
from preprocess import rename_inclassable

def sunburst(df, mode):
    df=rename_inclassable(df)
    df['langue_new'] = df['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('autres langues')
    language_map = {"fr": "français", "en": "anglais", "autres langues": "autres langues"}
    df['langue_new'] = df['langue_new'].map(language_map)
    # df = df[~df['domaine'].isin(['inclassable'])]
    # df = df[~df['langue_new'].isin(['les autres'])]
    df_domain_languages = df.groupby(["domaine", "langue_new"], as_index=False).count()[
        ["domaine", "langue_new", "grade"]]
    df_domain_languages.rename(columns={"grade": "count"}, inplace=True)
    df_domain_uni = df.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "grade"]]
    df_domain_uni.rename(columns={"grade": "count"}, inplace=True)
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
            insidetextfont=dict(
                size=14,
                color='white'
            ),
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
            # marker=dict(
            #     colors=['rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(255, 0, 0, 1)',
            #             'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)', 'rgba(0, 255, 0, 1)',
            #             'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 255, 1)'],
            # ),
        ))
        fig.update_layout(width=700, height=700,
                          title='La répartition des langues dans différents domaines',
                          annotations=[dict(
                            text='Cliquez sur chaque partie de domaine pour voir plus de détails',
                            x=-0.05, y=1.05,
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            )]
                         )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_langue(),
            leaf=dict(opacity=1),
           )

    elif mode == 'univ':
        # fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count', custom_data=['univ'])
        labels = []
        parents = []
        values = []

        for domain, domain_df in df_domain_uni.groupby('domaine'):
            domain_values = domain_df['count'].sum()
            top5_children = domain_df.nlargest(5, "count")
            top2_children = domain_df.nlargest(2, "count")
            labels.append(domain)
            parents.append('')
            values.append(domain_values)
            if domain == 'programme individualisé ou inconnu':
                for row in top2_children.itertuples():
                    labels.append(f"{domain}-{row.univ}")
                    parents.append(domain)
                    values.append(row.count)
                other_count = domain_values - top2_children["count"].sum()
                labels.append(f"{domain}-Autres universités")
                parents.append(domain)
                values.append(other_count)
            else:
                for row in top5_children.itertuples():
                    labels.append(f"{domain}-{row.univ}")
                    parents.append(domain)
                    values.append(row.count)
                other_count = domain_values - top5_children["count"].sum()
                labels.append(f"{domain}-Autres universités")
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
            insidetextfont=dict(
                size=14,
                color='white'
                ),
            opacity=1,
            texttemplate='%{text}',
            text=[label.split('-')[-1].strip() for label in labels],
        ))

        fig.update_layout(width=700, height=700,
                          title='La répartition des meilleures universités dans différents domaines',
                          annotations=[dict(
                              text='Cliquez sur chaque partie de domaine pour voir plus de détails',
                              x=-0.05, y=1.05,
                              showarrow=False,
                              font=dict(size=12, color='black'),
                          )]
                          )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ(),
            leaf=dict(opacity=1),
        )
    return fig
"""
