import plotly.graph_objects as go
from operator import add
from hover_template import generate_hover_template_btb


def distribution_language(df,grade,doc):
    '''
    This function generates a back to back bar chart,where the x-axis represents the number of theses/dissertations, and y-axis shows years.
    The chart, shows back to back, the number of documents for a specific grade written in two langages 'French' and 'English'
    :param df: (pandas dataframe) the dataset we have, and from which we will choose the right columns for visualization
   :param grade: (str) the grade to visualize, can be 'maîtrise', or 'doctorat'
   :param doc (str) the name of the document for which we gonna visualize the number. it is 'dissertation' for 'maîtrise', and 'thèses'for 'doctorat'
   :return: (figure) the back to back bar chart
    '''
    categories = df['année'].unique().tolist()
    data_en = df[(df['grade'] == grade) & (df['langue'].isin(['en']))]
    data_fr = df[(df['grade'] == grade) & (df['langue'].isin(['fr']))]
    langue_fr = 'Français'
    langue_en ='Anglais'
    
    # Group by Year and Language and calculate the count
    language_counts_en = data_en.groupby(['année', 'langue']).size().reset_index(name='Count')
    language_counts_fr = data_fr.groupby(['année', 'langue']).size().reset_index(name='Count')
    en_pop = language_counts_en['Count'].tolist()
    fr_pop = language_counts_fr['Count'].tolist()
    s= list(map(add, en_pop, fr_pop))
    freq_en = [round((int(b)*100 / int(m)),2) for b,m in zip(en_pop, s)]
    freq_fr = [round((int(b)*100 / int(m)),2) for b,m in zip(fr_pop, s)]
    
    start_value = -max(fr_pop + en_pop)
    end_value = max(en_pop + fr_pop) 
    num_ticks = 11 - 1  # Subtract 1 to account for 0 as one of the values
    tick_values = []

    # Calculate tick values for values below 0
    negative_ticks = []
    negative_tick_range = abs(start_value)
    for i in range(num_ticks // 2):
        value = start_value + (i * negative_tick_range / (num_ticks // 2))
        negative_ticks.append(value)

    # Calculate tick values for values above 0
    positive_ticks = []
    positive_tick_range = end_value
    for i in range(num_ticks // 2 + 1):
        value = i * positive_tick_range / (num_ticks // 2)
        positive_ticks.append(value)

    # Combine the tick values
    tick_values = negative_ticks[::-1] + positive_ticks

    tick_values = [round(value / 100) * 100 for value in tick_values]

    fig = go.Figure()
    fig.add_trace(go.Bar(
      y=categories,
      x=en_pop,
      orientation='h',
      name='Anglais',
      hovertemplate= [generate_hover_template_btb(cat, pop, doc, freq,grade,langue_en) for cat, pop, freq in zip(categories, en_pop, freq_en)]

  ))
    fig.add_trace(go.Bar(
      y=categories,
      x=[-pop for pop in fr_pop],
      orientation='h',
      name='Français',
      hovertemplate= [generate_hover_template_btb(cat, pop, doc, freq,grade,langue_fr) for cat, pop, freq in zip(categories, fr_pop, freq_fr)]

  ))
    fig.update_layout(
      height=700,
      barmode='relative',
      xaxis=dict(
          title='Nombre de ' + doc,
          tickvals= tick_values,
          ticktext=[abs(val) for val in tick_values],
          title_font=dict(size=15)
      ),
      legend_title='Catégories de langues'
  )
    
    # Update the y-axis label using plotly graph object
    fig.update_layout(yaxis_title="")
    # Update the layout to remove the y-axis label
    fig.update_layout(title=dict(text='Année',
                                     xanchor='left',
                                     yanchor='top',
                                     font=dict(size=15),
                                     x=0.02,
                                     y=0.88))
    fig.add_annotation(text="Répartition de l'anglais et du français pour les " + doc,
                                     #x=0.15,
                                     y=1.1,
                                     showarrow=False,
                                     align='left',
                                     xref='paper',
                                     yref='paper',
                                     font=dict(size=18))
    fig.update_traces(hoverlabel=dict(namelength=0))
    return fig

def back_to_back(df,grade):
    '''
    This function generates a back to back bar chart,where the x-axis represents the number of theses/dissertations, and y-axis shows years.
    The chart, shows back to back, the number of documents for a specific grade written in two langages 'French' and 'English'. It calls another the distribution_language function above to display a chart depending on the grade
    :param df: (pandas dataframe) the dataset we have, and from which we will choose the right columns for visualization
    :param grade: (str) the grade to visualize, can be 'maîtrise', or 'doctorat'
    :return: (figure) the back to back bar chart
    '''
    if (grade == 'doctorat'):
        fig = distribution_language(df,'doctorat', 'thèses')
    else:
        fig = distribution_language(df,'maîtrise', 'dissertations')
    return fig  
