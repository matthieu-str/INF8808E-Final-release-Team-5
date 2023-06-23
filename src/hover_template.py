## hover templet for Radar chart 
def get_hover_univ(x_freq, y_freq, universities):
    hovertext_master = [f'<b>Maîtrise</b><br>Université: {uni}<br>No. de thèses: {x_freq[uni] if uni in x_freq else 0}' for uni in universities]
    hovertext_doctorat = [f'<b>Doctorat</b><br>Université: {uni}<br>No. de dissertations: {y_freq[uni] if uni in y_freq else 0}' for uni in universities]
    return hovertext_master, hovertext_doctorat

def get_hover_discipline():
    hovertemplate_master = '<b>Maîtrise</b><br>Discipline: %{theta}<br>No. de thèses: %{r}<extra></extra>'
    hovertemplate_doctorat = '<b>Doctorat</b><br>Discipline: %{theta}<br>No. de dissertations: %{r}<extra></extra>'
    return hovertemplate_master, hovertemplate_doctorat
    
def get_hover_stacked_bar_chart(): 
    hover_temp = 'Nombre de publications: %{x}<br>Discipline: %{y}'
    return hover_temp

def get_hover_box_plot(name_text=None):
    if name_text is None: 
        return "Year: %{x}<br>Number of Pages: %{y}<extra></extra>"
    return "Year: %{x}<br>Number of Pages: %{y}<br>Grade: "+ name_text + "<extra></extra>"

def get_hover_sunburst_chart_langue():
    hover_temp = "<b>%{label}</b><br><b>Count:</b> %{value}<extra></extra>"
    return hover_temp
def get_hover_sunburst_chart_univ():
    hover_temp = "<b>%{label}</b><br><b>Count:</b> %{value}<extra></extra>"
    return hover_temp
