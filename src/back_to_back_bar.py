import plotly.graph_objects as go
from operator import add
def distribution_language(df,grade,doc):
  categories = df['année'].unique().tolist()
  data_en = df[(df['grade'] == grade) & (df['langue'].isin(['en']))]
  data_fr = df[(df['grade'] == grade) & (df['langue'].isin(['fr']))]
  
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
  tick_range = end_value - start_value

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
    #marker_color='blue',
    hovertext=[f'{cat} <br>  No. de {doc} = {pop} <br>  Pourcentage de {doc} = {freq}%'  for pop, cat,freq in zip(en_pop,categories,freq_en)],
    hovertemplate='%{hovertext}<extra></extra>'
))
  fig.add_trace(go.Bar(
    y=categories,
    x=[-pop for pop in fr_pop],
    orientation='h',
    name='Français',
    #marker_color='Red',
    hovertext=[f'{cat} <br>  No. de {doc} = {pop} <br>  Pourcentage de {doc} = {freq}%'  for pop, cat,freq in zip(fr_pop,categories,freq_fr)],
    hovertemplate='%{hovertext}<extra></extra>'
))
  fig.update_layout(
    height=700,
    barmode='relative',
    title="Répartition de l'anglais et du français pour les " + doc,
    xaxis=dict(
        title='Nombre de ' + doc,
        tickvals= tick_values,
        ticktext=[abs(val) for val in tick_values],
        #range=[-max(en_pop + fr_pop), max(en_pop + fr_pop)]
    ),
    yaxis=dict(
        title="Année"
    )
)
  return fig

def back_to_back(df,grade):
  if (grade == 'doctorat'):
    fig = distribution_language(df,'doctorat', 'Thèses')
  else:
    fig = distribution_language(df,'maîtrise', 'Dissertations')
  return fig  
    


