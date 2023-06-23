import pandas as pd
import plotly.express as px
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ
from preprocess import rename_languages,rename_inclassable

# def sunburst(df, mode):
#     df=rename_inclassable(df)
#     if mode == 'univ':
#         # Get the unique values in the "domaine" column
#         domaines = df['domaine'].unique()
#         # Iterate over each unique "domaine" value
#         for domaine in domaines:
#             # Filter the data for the current "domaine" value
#             filtered_data = df[df['domaine'] == domaine]
#             # Count the number of occurrences for each university in the filtered data
#             univ_counts = filtered_data['univ'].value_counts()
#             # Get the top 5 universities
#             top_univs = univ_counts.index[:5]
#             # Iterate over each row in the filtered data
#             for index, row in filtered_data.iterrows():
#                 # Check if the university is not in the top 5
#                 if row['univ'] not in top_univs:
#                     # Rename the university to 'autres universités'
#                     df.at[index, 'univ'] = 'Autres universités'
#
#         df_domain_uni = df.groupby(["domaine", "univ"], as_index=False).count()[["domaine", "univ", "grade"]]
#         df_domain_uni.rename(columns={"grade": "count"}, inplace=True)
#
#         fig = px.sunburst(df_domain_uni, path=['domaine', 'univ'], values='count', custom_data=['univ'])
#         fig.update_layout(width=700, height=700,
#                           title='La répartition des 5 meilleures universités dans différents domaines',
#                           annotations=[dict(
#                               text='Cliquez sur chaque partie de domaine pour voir plus de détails',
#                               x=-0.05, y=1.05,
#                               showarrow=False,
#                               font=dict(size=12, color='black'),
#                           )]
#                           )
#         # Customize label positions
#         fig.update_traces(
#             hoverlabel=dict(
#                 align='right',
#                 font=dict(size=12)
#             )
#         )
#         fig.update_traces(hovertemplate=get_hover_sunburst_chart_univ())
#
#     if mode == 'langue':
#         df=rename_languages(df)
#         # Get the unique values in the "domaine" column
#         domaines = df['domaine'].unique()
#         # Iterate over each unique "domaine" value
#         for domaine in domaines:
#             # Filter the data for the current "domaine" value
#             filtered_data = df[df['domaine'] == domaine]
#             # Count the number of occurrences for each language in the filtered data
#             langue_counts = filtered_data['langue'].value_counts()
#             # Get the top 2 languages
#             top_langues = langue_counts.index[:2]
#             # Iterate over each row in the filtered data
#             for index, row in filtered_data.iterrows():
#                 # Check if the language is not in the top 2
#                 if row['langue'] not in top_langues:
#                     # Rename the university to 'autres universités'
#                     df.at[index, 'langue'] = 'autres langues'
#
#         df_domain_languages = df.groupby(["domaine", "langue"], as_index=False).count()[["domaine", "langue", "grade"]]
#         df_domain_languages.rename(columns={"grade": "count"}, inplace=True)
#
#         fig = px.sunburst(df_domain_languages, path=['domaine', 'langue'], values='count', custom_data=['langue'])
#         fig.update_layout(width=700, height=700,
#                           title='La répartition des langues dans différents domaines',
#                           annotations=[dict(
#                             text='Cliquez sur chaque partie de domaine pour voir plus de détails',
#                             x=-0.05, y=1.05,
#                             showarrow=False,
#                             font=dict(size=12, color='black'),
#                             )]
#                          )
#         # Customize label positions
#         fig.update_traces(
#             hoverlabel=dict(
#                 align='right',
#                 font=dict(size=12)
#             )
#         )
#         fig.update_traces(
#             hovertemplate=get_hover_sunburst_chart_langue()
#         )
#     return fig







import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from hover_template import get_hover_sunburst_chart_langue, get_hover_sunburst_chart_univ

def sunburst(df, mode):
    df['langue_new'] = df['langue'].str.lower().map({'fr': 'fr', 'en': 'en'}).fillna('les autres')
    language_map = {"fr": "Français", "en": "Anglais", "les autres": "les autres"}
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
            if domain == 'inclassable':
                continue
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
        fig.update_layout(width=800, height=800,
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
            leaf=dict(opacity=1)
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
            if domain == 'inclassable':
                continue
            for row in top10_children.itertuples():
                labels.append(f"{domain}-{row.univ}")
                parents.append(domain)
                values.append(row.count)
            other_count = domain_values - top10_children["count"].sum()
            labels.append(f"{domain}-les autres")
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

        fig.update_layout(width=800, height=800,
                          title='La répartition des 10 meilleures universités dans différents domaines',
                          annotations=[dict(
                              text='Cliquez sur chaque partie de domaine pour voir plus de détails',
                              x=-0.05, y=1.05,
                              showarrow=False,
                              font=dict(size=12, color='black'),
                          )]
                          )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ(),
            leaf=dict(opacity=1)
        )
    return fig
