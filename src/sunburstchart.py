'''
Sunburst chart
'''

import plotly.graph_objects as go
from hover_template import get_hover_sunburst_chart_langue
from hover_template import get_hover_sunburst_chart_univ


def sunburst(df, mode):
    '''
    This function displays the sunburst graph showing the distribution
    of languages or universities in the main fields.

    Inputs :
    df : represents the data frame containing all the information.
    mode : takes the university or language variable according to the factor
    whose distribution we want to see within the main field.

    output:
    Returns the sunburst chart.
    '''
    # definition of variables related to top languages and universities
    df_sun = df
    df_sun['langue_new'] = (
        df_sun['langue']
        .str.lower()
        .map({'fr': 'fr', 'en': 'en'})
        .fillna('autres langues')
        )
    language_map = {
        "fr": "français",
        "en": "anglais",
        "autres langues": "autres langues"
        }
    df_sun['langue_new'] = df_sun['langue_new'].map(language_map)
    df_sun = df_sun[~df_sun['langue_new'].isin(['autres langues'])]
    df_domain_languages = (
        df_sun.groupby(["domaine", "langue_new"], as_index=False)
        .count()[["domaine", "langue_new", "grade"]]
        )
    df_domain_languages.rename(columns={"grade": "count"}, inplace=True)
    df_domain_uni = (
        df_sun.groupby(["domaine", "univ"], as_index=False)
        .count()[["domaine", "univ", "grade"]]
        )
    df_domain_uni.rename(columns={"grade": "count"}, inplace=True)
    if mode == 'langue':
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
        ))
        fig.update_layout(width=700, height=700,
                          title='La répartition des langues dans'
                                ' différents domaines',
                          annotations=[dict(
                            text="Cliquez sur chaque partie de domaine pour"
                                 " voir plus de détails.",
                            x=-0.05, y=1.05,
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            ),
                            dict(
                            text="Note: La classe de domaine du programme"
                                 " individualisé et les autres langues ont été"
                                 " exclues car elles sont illisibles.",
                            x=-0.15, y=-0.1,
                            showarrow=False,
                            font=dict(size=11, color='black'),
                            )]
                          )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_langue(),
            leaf=dict(opacity=1),
           )

    elif mode == 'univ':
        labels = []
        parents = []
        values = []

        for domain, domain_df in df_domain_uni.groupby('domaine'):
            if domain == 'programme individualisé ou inconnu':
                continue
            domain_values = domain_df['count'].sum()
            top5_children = domain_df.nlargest(5, "count")
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
                          title='La répartition des meilleures universités'
                                ' dans différents domaines',
                          annotations=[dict(
                              text='Cliquez sur chaque partie de domaine pour'
                                   ' voir plus de détails.',
                              x=-0.05, y=1.05,
                              showarrow=False,
                              font=dict(size=12, color='black'),
                          ),
                            dict(
                            text="Note: La classe de domaine du programme"
                                 " individualisé a été exclue car elle est"
                                 " illisible.",
                            x=-0.15, y=-0.1,
                            showarrow=False,
                            font=dict(size=11, color='black'),
                            )]
                          )
        fig.update_traces(
            hovertemplate=get_hover_sunburst_chart_univ(),
            leaf=dict(opacity=1),
        )
    return fig
