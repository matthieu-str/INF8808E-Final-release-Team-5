'''
Hover template
'''


# hover templet for Radar chart (1)
def get_hover_univ(x_freq, y_freq, universities):
    hovertext_master = [f'<b>Maîtrise</b><br><b>Université:</b> {uni}<br><b>No. de thèses:</b> {x_freq[uni] if uni in x_freq else 0}' for uni in universities]
    hovertext_doctorat = [f'<b>Doctorat</b><br><b>Université:</b> {uni}<br><b>No. de dissertations:</b> {y_freq[uni] if uni in y_freq else 0}' for uni in universities]
    return hovertext_master, hovertext_doctorat


# hover templet for Radar chart (2)
def get_hover_discipline():
    hovertemplate_master = '<b>Maîtrise</b><br><b>Discipline:</b> %{theta}<br><b>No. de thèses:</b> %{r}<extra></extra>'
    hovertemplate_doctorat = '<b>Doctorat</b><br><b>Discipline:</b> %{theta}<br><b>No. de dissertations:</b> %{r}<extra></extra>'
    return hovertemplate_master, hovertemplate_doctorat


def get_hover_stacked_area_chart(mode):
    if mode == 'count':
        hover_temp = '<b>%{customdata[1]}</b><br><b>Année:</b> %{x}<br><b>Nombre de publications:</b> %{y}<br><b>Les 5 disciplines les plus importantes:</b> %{customdata[0]}'
        return hover_temp
    else:
        hover_temp = '<b>%{customdata[1]}</b><br><b>Année:</b> %{x}<br><br><b>Pourc. de publications:</b> %{y}%<br><b>Les 5 disciplines les plus importantes:</b> %{customdata[0]}'
        return hover_temp


def get_hover_stacked_bar_chart():
    hover_temp = '<b>Nombre de publications:</b> %{x}<br><b>Discipline:</b> %{y}'
    return hover_temp


def get_hover_box_plot(name_text=None):
    if name_text is None:
        return "Année: %{x}<br>Nombre de Pages: %{y}<extra></extra>"
    return "Année: %{x}<br>Nombre de Pages: %{y}<br>Niveau d'études: " + name_text + "<extra></extra>"


def get_hover_sunburst_chart_langue():
    hover_temp = "<b>Étiquette:</b> %{label}<br><b>Nombre de publications:</b> %{value}<extra></extra>"
    return hover_temp


def get_hover_sunburst_chart_univ():
    hover_temp = "<b>Étiquette:</b> %{label}<br><b>Nombre de publications:</b> %{value}<extra></extra>"
    return hover_temp


def get_hover_back_to_back(cat, pop, doc, freq, grade, langue):
    hover_temp = f"<span> <b>Année: </b>{cat}<br> <b>Niveau d'étude: </b>{grade.title()}<br> <b>Langue: </b>{langue}<br> <b>No. de {doc} = </b>{pop}<br> <b>Pourcentage de {doc} = </b>{freq}%</span>"
    return hover_temp
