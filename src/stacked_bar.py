import plotly.express as px
from preprocess import rename_languages

def get_figure(data, colored, domaine):
    data = data[data['domaine'] == domaine]
    if colored == 'range of pages':
        data = data[data['range of pages'] != '0']
    if colored == 'univ':
        top_9_universities=list(data.groupby(['univ']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)['univ'].head(9))
        data.loc[~data['univ'].isin(top_9_universities), 'univ'] = "Other universities"
    if colored == 'langue':
        data=rename_languages(data)
        top_languages=list(data.groupby(['langue']).size().reset_index(name='counts').sort_values(by='counts', ascending=False)['langue'].head(2))
        data.loc[~data['langue'].isin(top_languages), 'langue'] = "other languages"
    df_grouped = data.groupby(['discipline', colored]).size().unstack().fillna(0)

    # Reset the index to have 'discipline' as a column
    df_grouped = df_grouped.reset_index()

    # Calculate the total number of degrees for each discipline
    df_grouped['total'] = sum([df_grouped[col] for col in list(data[colored].unique())])

    # Sort the DataFrame based on the total number of degrees in descending order
    df_grouped = df_grouped.sort_values('total', ascending=True)

    # Create the stacked bar chart using Plotly Express
    fig = px.bar(df_grouped, y='discipline', x=list(data[colored].unique()), 
            title='Visualisation of the distribution of different variables for various disciplines', orientation='h',
             barmode='stack')
    # Update the x-axis label using plotly graph object
    fig.update_xaxes(title_text="Number of publications")
    # Update the y-axis label using plotly graph object
    fig.update_yaxes(title_text="Discipline")
    # Size of figure
    fig.update_layout(height=900, width=900)
    return fig
