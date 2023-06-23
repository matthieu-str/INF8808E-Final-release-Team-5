import plotly.express as px
import pandas as pd
from preprocess import other_languages, other_univ, rename_languages, rename_inclassable

# TODO
# Text box top 5 disciplines for domains
def get_figure(df, y_axis, mode):

    titles = {'univ': 'Université',
              'domaine': 'Domaine',
              'langue': 'Langue',
              'grade': "Niveau d'études",
              'count': 'Nb de publications',
              'percentage': 'Pourc. de publications'}

    df_count = df.groupby(by=['année', f'{y_axis}'], as_index=False).count()[['année', f'{y_axis}', 'discipline']]
    df_count.rename(columns={"discipline": "count"}, inplace=True)

    top_disciplines = df.groupby(['année', f'{y_axis}'])['discipline'].apply(
        lambda x: '<b> (Top 5 disciplines)</b><br>' + '<br>'.join([
            f'{i} ({round(j, 2)}{"%" if mode=="percentage" else ""})' for i, j in zip(
                x.value_counts().nlargest(5).index, 
                (x.value_counts().nlargest(5)/x.value_counts().sum()*100 if mode=="percentage" else x.value_counts().nlargest(5).values)
            )
        ])
    ).reset_index()

    df_count = pd.merge(df_count, top_disciplines, on=['année', f'{y_axis}'])

    if y_axis == 'univ':
        df_count = other_univ(df_count)

    if y_axis == 'domaine':
        df_count = rename_inclassable(df_count)

    if y_axis == 'langue':
        df_count = other_languages(df_count)
        df_count = rename_languages(df_count)

    if mode == "percentage":
        count_tot = df_count.groupby(["année"], as_index=False).sum("count")
        count_tot.rename(columns={"count": "count_total"}, inplace=True)
        df_count = pd.merge(left=df_count, right=count_tot, how="left", on="année")
        df_count["percentage"] = round(100 * df_count["count"] / df_count["count_total"], 2)

    hover_data = {f'{y_axis}': False, "discipline": True}  

    fig = px.area(df_count.sort_values(y_axis, ascending=False),
                  x="année",
                  y=f"{mode}",
                  color=f"{y_axis}",
                  labels={f'{y_axis}': f'{titles[y_axis]}', f'{mode}': f'{titles[mode]}', 'année': 'Année'},
                  hover_data=hover_data) 
    fig.update_layout(legend_traceorder='reversed')
    fig.update_layout(height=600, width=1200)
    fig.update_xaxes(title_text="Année", title_font=dict(size=20))
    if mode == 'count':
        fig.update_yaxes(title_text='')
        fig.update_layout(title=dict(text='Nombre de publications',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=20)))
    elif mode == 'percentage':
        fig.update_yaxes(title_text='',
                         range=[0,100])
        fig.update_layout(title=dict(text='Pourcentage de publications [%]',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=20)))

    return fig





"""
def get_figure(df, y_axis, mode):

    titles = {'univ': 'Université',
              'domaine': 'Domaine',
              'langue': 'Langue',
              'grade': "Niveau d'études",
              'count': 'Nb de publications',
              'percentage': 'Pourc. de publications'}

    df_count = df.groupby(by=['année', f'{y_axis}'], as_index=False).count()[['année', f'{y_axis}', 'discipline']]
    df_count.rename(columns={"discipline": "count"}, inplace=True)

    if y_axis == 'univ':
        df_count = other_univ(df_count)

    if y_axis == 'domaine':
        df_count = rename_inclassable(df_count)

    if y_axis == 'langue':
        df_count = other_languages(df_count)
        df_count = rename_languages(df_count)

    if mode == "percentage":
        count_tot = df_count.groupby(["année"], as_index=False).sum("count")
        count_tot.rename(columns={"count": "count_total"}, inplace=True)
        df_count = pd.merge(left=df_count, right=count_tot, how="left", on="année")
        df_count["percentage"] = round(100 * df_count["count"] / df_count["count_total"], 2)

    fig = px.area(df_count.sort_values(y_axis, ascending=False), # sorting values for displaying areas in alphabetical order
                  x="année",
                  y=f"{mode}",
                  color=f"{y_axis}",
                  labels={f'{y_axis}': f'{titles[y_axis]}', f'{mode}': f'{titles[mode]}', 'année': 'Année'})
    fig.update_layout(legend_traceorder='reversed') # reverse ordering in the legend for having top layer the same as top legend
    fig.update_layout(height=600, width=1200)
    fig.update_xaxes(title_text="Année", title_font=dict(size=20))
    if mode == 'count':
        fig.update_yaxes(title_text='')
        fig.update_layout(title=dict(text='Nombre de publications',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=20)))
    elif mode == 'percentage':
        fig.update_yaxes(title_text='',
                         range=[0,100])
        fig.update_layout(title=dict(text='Pourcentage de publications [%]',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=20)))

    return fig
    """
