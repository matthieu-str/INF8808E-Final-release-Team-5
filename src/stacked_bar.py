from preprocess import rename_languages
from hover_template import get_hover_stacked_bar_chart
import plotly.express as px

Variable_options = {'grade': "des niveaux d'études", 'univ': 'des universités', 'langue': 'des langues',
                    'range of pages': 'du nombre de pages'}

def get_figure(data, colored, domaine):
    data = data[data['domaine'] == domaine]
    if colored == 'range of pages':
        data = data[data['range of pages'] != '0']
    if colored == 'univ':
        top_5_universities=list(data.groupby(['univ']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)['univ'].head(5))
        data.loc[~data['univ'].isin(top_5_universities), 'univ'] = "Autres universités"
    if colored == 'langue':
        data=rename_languages(data)
        top_languages=list(data.groupby(['langue']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)['langue'].head(2))
        data.loc[~data['langue'].isin(top_languages), 'langue'] = "autres langues"
    df_grouped = data.groupby(['discipline', colored]).size().unstack().fillna(0)

    # Reset the index to have 'discipline' as a column
    df_grouped = df_grouped.reset_index()

    # Calculate the total number of degrees for each discipline
    df_grouped['total'] = sum([df_grouped[col] for col in list(data[colored].unique())])

    # Sort the DataFrame based on the total number of degrees in descending order
    df_grouped = df_grouped.sort_values('total', ascending=True)

    # Create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, y='discipline', x=list(data[colored].unique()), orientation='h',
             barmode='stack')
    fig.update_traces(hovertemplate=get_hover_stacked_bar_chart())
    # Update the x-axis label using plotly graph object
    fig.update_xaxes(title_text="Nombre de publications",title_font=dict(size=15))
    # Update the y-axis label using plotly graph object
    fig.update_layout(yaxis_title="")
    # Update the layout to remove the y-axis label
    fig.update_layout(title=dict(text='Discipline',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=15),
                                     x=0.13,
                                     y=0.95))
    fig.add_annotation(text="Visualisation de la distribution "+Variable_options[colored]+" dans les disciplines du domaine "+domaine,
                                     #x=0.15,
                                     y=1.09,
                                     showarrow=False,
                                     align='left',
                                     xref='paper',
                                     yref='paper',
                                     font=dict(size=18))
    # Size and title of figure
    fig.update_layout(height=800, width=1200, legend_title='Catégories '+Variable_options[colored])
    return fig
