'''
    This file contains some helper functions to help display some figures.
'''
import plotly.graph_objects as go

def update_box_layout(fig, title_text, showlegend=True):
  '''
    return Box plots of the number of pages per year for all grades.
  '''  
  fig.update_layout(
        title={
            'text': title_text,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
            },
        xaxis_title="Année",
        yaxis_title="Nombre de Pages",
        hovermode='x unified',
        showlegend=showlegend)
  return fig


