import plotly.express as px
import pandas as pd
from preprocess import other_languages, other_univ, rename_languages, rename_inclassable, get_top_univ
from hover_template import get_hover_stacked_area_chart


def get_figure(df, y_axis, mode):
    '''
    This function generates the stacked area figure, with its different y-axis and mode possibilities.
    :param df: (pandas dataframe) data to visualize after basic pre-processing
    :param y_axis: (str) y-axis to visualize, can be 'univ', 'domaine', 'langue' or 'grade'
    :param mode: (str) mode of the chart, can be 'count' for counting the number of publications or 'percentage' for normalized values.
    :return: (figure) the stacked area chart
    '''
    titles = {'univ': 'Université',
              'domaine': 'Domaine',
              'langue': 'Langue',
              'grade': "Niveau d'études"}

    df_count = df.groupby(by=['année', f'{y_axis}'], as_index=False).count()[['année', f'{y_axis}', 'discipline']]
    df_count.rename(columns={"discipline": "count"}, inplace=True)

    if y_axis == 'univ':
        top_univ = get_top_univ(df_count, n=5)
        df_count = other_univ(df_count, True, top_univ)
        df = other_univ(df, False, top_univ)

    if y_axis == 'domaine':
        df_count = rename_inclassable(df_count)
        df = rename_inclassable(df)

    if y_axis == 'langue':
        df_count = other_languages(df_count, True)
        df_count = rename_languages(df_count)
        df = other_languages(df, False)
        df = rename_languages(df)

    if mode == "percentage":
        count_tot = df_count.groupby(["année"], as_index=False).sum("count")
        count_tot.rename(columns={"count": "count_total"}, inplace=True)
        df_count = pd.merge(left=df_count, right=count_tot, how="left", on="année")
        df_count["percentage"] = round(100 * df_count["count"] / df_count["count_total"], 2)

    top_disciplines = df.groupby(['année', f'{y_axis}'])['discipline'].apply(
        lambda x: '<br>' + '<br>'.join([
            f'{i} ({round(j, 2)}{"%" if mode=="percentage" else ""})' for i, j in zip(
                x.value_counts().nlargest(5).index,
                (x.value_counts().nlargest(5)/x.value_counts().sum()*100 if mode=="percentage" else x.value_counts().nlargest(5).values)
            )
        ])
    ).reset_index()

    df_count = pd.merge(df_count, top_disciplines, on=['année', f'{y_axis}'])
    df_count.rename(columns={'discipline': 'd'}, inplace=True)
    hover_data = {f'{y_axis}': False, "d": True}
    df_count = df_count.sort_values(y_axis, ascending=False)
    fig = px.area(df_count,
                  x="année",
                  y=f"{mode}",
                  color=f"{y_axis}",
                  labels={f'{y_axis}': f'{titles[y_axis]}'},
                  custom_data=['d'],
                  hover_data=hover_data
                  )
    fig.update_traces(hovertemplate=get_hover_stacked_area_chart(mode))
    fig.update_layout(legend_traceorder='reversed')
    fig.update_layout(height=600, width=1200)
    fig.update_xaxes(title_text="Année", title_font=dict(size=15))
    fig.add_annotation(text=f'Evolution du nombre de publications par {titles[y_axis].lower()} en fonction du temps',
                       # x = 0.95,
                       y = 1.2,
                       showarrow=False,
                       font=dict(size=16),
                       align='left',
                       xref='paper',
                       yref='paper')
    fig.update_layout(margin=dict(t=100))

    if mode == 'count':
        fig.update_yaxes(title_text='')
        fig.update_layout(title=dict(text='Nombre de publications',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=15),
                                     y=0.88))
    elif mode == 'percentage':
        fig.update_yaxes(title_text='',
                         range=[0,100])
        fig.update_layout(title=dict(text='Pourcentage de publications [%]',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=15),
                                     y=0.88))
    fig.update_traces(hoverlabel=dict(namelength=0))    

    return fig
