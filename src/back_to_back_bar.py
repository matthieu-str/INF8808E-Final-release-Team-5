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
  start_value = - max(fr_pop+en_pop)
  end_value = max(en_pop+fr_pop)
  num_ticks = 11-1 # Subtract 1 to account for 0 as one of the values
  tick_values = []
  tick_range = end_value - start_value
  for i in range(num_ticks):
    value = start_value + (i * tick_range / num_ticks)
    tick_values.append(value)
    tick_values = [round(value / 100) * 100 for value in tick_values]
  
  fig = go.Figure()
  fig.add_trace(go.Bar(
    y=categories,
    x=en_pop,
    orientation='h',
    name='English',
    marker_color='purple',
    hovertext=[f'{cat} <br>  No. of {doc} = {pop} <br>  Percentage of Thesis = {freq}%'  for pop, cat,freq in zip(en_pop,categories,freq_en)],
    hovertemplate='%{hovertext}<extra></extra>'
))
  fig.add_trace(go.Bar(
    y=categories,
    x=[-pop for pop in fr_pop],
    orientation='h',
    name='French',
    marker_color='green',
    hovertext=[f'{cat} <br>  No. of {doc} = {pop} <br>  Percentage of Thesis = {freq}%'  for pop, cat,freq in zip(fr_pop,categories,freq_fr)],
    hovertemplate='%{hovertext}<extra></extra>'
))
  fig.update_layout(
    barmode='relative',
    title='Distribution of English And French for ' + doc,
    xaxis=dict(
        title='',
        tickvals= tick_values,
        ticktext=[abs(val) for val in tick_values]
    ),
    yaxis=dict(
        title=None
    )
)
  return fig

def back_to_back(df,grade):
  if (grade == 'doctorat'):
    fig = distribution_language(df,'doctorat', 'Thesis')
  else:
    fig = distribution_language(df,'maîtrise', 'Dissertation')
  return fig  
    


