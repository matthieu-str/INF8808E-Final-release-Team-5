import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import preprocess as preproc
from box_plot import overview_box_plot, mvd_box_plot
import helper
import callback
import template
from template import external_css
import stacked_bar
import stacked_area_chart
from back_to_back_bar import back_to_back, distribution_language
from sunburstchart import sunburst
from radar_chart import init_figure, update_graph


# Load the dataset
df = pd.read_csv("assets/data/thesesMemoiresQC2000-2022-v20230508-1.csv", na_values="?")
df = preproc.to_lowercase(df)
df = preproc.assign_and_range_pages(df)
df = preproc.delete_unecessary_columns(df)
df = preproc.delete_duplicate_disciplines(df)

# Update labels of stacked bar chart
stackedbar_default_options = [
                        {'label': 'Sciences Humaines', 'value': 'sciences humaines'},
                        {'label': 'Sciences Naturelles', 'value': 'sciences naturelles'},
                        {'label': 'Programme individualisé ou inconnu', 'value': 'inclassable'}
                    ]
stacked_bar_down_options = [
                        {'label': "Niveau d'études", 'value': 'grade'},
                        {'label': 'Universités', 'value': 'univ'},
                        {'label': 'Langues', 'value': 'langue'},
                        {'label': 'Nombre de pages', 'value': 'range of pages'}
                    ]

# Create the Dash app
app = dash.Dash(__name__)

# Navbar
navbar = html.Nav(
    className="navbar",
    children=[
        html.Div(
            className="navbar-container",
            children=[
                html.Div(
                    className="navlink-container",
                    children=[
                        dcc.Link(
                            html.Span("Home", title="Cliquez pour revenir à la page d'accueil"),
                            href="/",
                            className="navlink",
                            id="navlink-home",
                        ),
                        dcc.Link(
                            html.Span("Stacked Area Chart", title="Cliquez pour afficher Stacked Area Chart page"),
                            href="/stacked-area",
                            className="navlink",
                            id="navlink-stacked-area",
                        ),
                        dcc.Link(
                            html.Span("Stacked Bar Chart", title="Cliquez pour afficher Stacked Bar Charts"),
                            href="/stacked-bar",
                            className="navlink",
                            id="navlink-stacked-bar",
                        ),
                        dcc.Link(
                            html.Span("Radar Chart", title="Cliquez pour afficher Radar Charts"),
                            href="/radar",
                            className="navlink",
                            id="navlink-radar",
                        ),
                        dcc.Link(
                            html.Span("Sunburst Chart", title="Cliquez pour afficher Sunburst Charts"),
                            href="/sunburst",
                            className="navlink",
                            id="navlink-sunburst",
                        ),
                        dcc.Link(
                            html.Span("Back to Back Bar Chart", title="Cliquez pour afficher Back to Back Bar Charts"),
                            href="/back-to-back-bar",
                            className="navlink",
                            id="navlink-back-to-back-bar",
                        ),
                        dcc.Link(
                            html.Span("Box Plot", title="Cliquez pour afficher the Box Plots"),
                            href="/box-plots",
                            className="navlink",
                            id="navlink-box-plots",
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Footer
footer = html.Footer(
    className="footer",
    children=[
        html.P("Cette application Web a été développée en tant que projet dans le cadre du cours INF8808E de Polytechnic Montréal."),
    ],
)

# App layout

#image_path = "assets/header.jpg"

def welcome_page():
    return html.Div(className='welcome-page-container', children=[
        html.Div(className='content', children=[
            html.Div(className='welcome-title', children=[
                'Études supérieures dans les universités québécoises entre 2000 et 2022'
            ])
        ]),
    ])


app.layout = html.Div(
    className="app-container",
    children=[
        dcc.Location(id="url", refresh=False),
        html.Header([
            welcome_page(),  
            navbar,
        ]),
        html.Div(id="page-content"),
        footer,
    ],
)

#for css in external_css:
    #app.css.append_css({"external_url": css})

app.css.external_stylesheets = external_css

# Update active navlink color
@app.callback(
    Output("navlink-home", "style"),
    Output("navlink-stacked-area", "style"),
    Output("navlink-stacked-bar", "style"),
    Output("navlink-radar", "style"),
    Output("navlink-sunburst", "style"),
    Output("navlink-back-to-back-bar", "style"),
    Output("navlink-box-plots", "style"),
    Input("url", "pathname"),
)
def update_navlink_styles(pathname):
    return callback.update_navlink_styles(pathname)

# Update page content based on URL pathname
# Update page content based on URL pathname
# Update page content based on URL pathname
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            className="home-content",
            children=[
                html.H1(
                    "Tracer les horizons du savoir : Un parcours visuel de la recherche supérieure au Québec"),
                
                html.H3("Les universités du Québec sont devenues des pôles d'excellence académique renommés, attirant un large éventail d'étudiants du monde entier. Notre projet s'efforce d'explorer visuellement la riche mosaïque de thèses et de mémoires produits au sein de ces institutions. En analysant les tendances et les changements au cours temps, nous visons à découvrir des informations précieuses sur le paysage des études supérieures.Le tableau de bord du projet fournit des informations sur la répartition des diplômes, les affiliations universitaires et les modèles disciplinaires de 2000 à 2022. Nos utilisateurs cibles comprennent les chercheurs, les administrateurs universitaires, les bibliothèques, les institutions de financement, les chercheurs consultants, publications académiques, étudiants diplômés, futurs étudiants et grand public. En acquérant une meilleure compréhension du paysage de la recherche, les utilisateurs peuvent prendre des décisions éclairées, suivre les tendances émergentes et contribuer à l'avancement des connaissances dans la communauté universitaire québécoise.") ,
                 
                html.H3(
                    "Instructions", className="instructions"),
                html.P(
                    "1. Cliquez sur Stacked Area Chart pour voir combien chaque université a contribué au domaine de recherche entre 2000 et 2022, les changements dans le nombre de thèses et de mémoires au cours de cette période, ainsi que les changements dans la répartition de l'anglais et du français pour la rédaction de thèses et de mémoires et le top 5 des disciplines pour chaque domaine universitaire et la langue utilisée au fil des années."),
                html.P(
                    "2. Cliquez sur Stacked Bar Chart pour voir si une langue particulière a été préférée dans une discipline donnée, et s'il y a une corrélation entre le nombre de pages et la discipline, et pour visualiser quelles universités ont fait le plus de contributions dans chacune discipline et domaine principal."),
                html.P(
                 "3. Cliquez sur Radar Chart pour voir quelles universités contribuent le plus grand nombre de thèses et mémoires, et quelles sont les 10 principales disciplines représentées dans les thèses et mémoires"
                ), 
               html.P(
                 "4. Cliquez sur Sunburst Chart pour voir si la langue des textes varie selon qu'ils sont dans différents grands domaines et différentes universités, le nombre de thèses et mémoires répartis entre disciplines et grands domaines, et quelles universités ont le plus contribué dans chaque discipline et domaine majeur."
                ),
               html.P(
                 "5. Cliquez sur Back to Back Bar Chart pour visualiser la répartition du français et de l'anglais pour les masters et doctorats."
                ),
               html.P(
                 "6. Cliquez sur Box Plot pour visualiser si la longueur des documents a changé au fil du temps ou pour la maîtrise vs le doctorat."
                ),



            ]
        )
    elif pathname == "/stacked-area":
        return html.Div(
            className="stacked-area-content", children=[
                html.Header(children=[
                    html.Div([html.Label("Publications par : ", style=dict(fontWeight='bold')),
                              dcc.RadioItems(
                                  id='stacked-area-checkbox-1',
                                  options=[{'label': 'Universités', 'value': 'univ'},
                                           {'label': 'Domaines', 'value': 'domaine'},
                                           {'label': 'Langues', 'value': 'langue'},
                                           {'label': "Niveau d'études", 'value': 'grade'}],
                                  value=['univ']),  # Set initial value for stacked-area-checkbox-1
                              ], style=dict(display='flex')),
                    html.Div([html.Label("Mode : ", style=dict(fontWeight='bold')),
                              dcc.RadioItems(
                                  id='stacked-area-checkbox-2',
                                  options=[{'label': 'Compte', 'value': 'count'},
                                           {'label': 'Pourcentage', 'value': 'percentage'}],
                                  value=['count']),  # initial value for stacked-area-checkbox-2
                            ], style=dict(display='flex')),
                    html.Button('Cliquez ici', id="button"),
                    ]),
                html.Main(className='viz-container', children=[
                    dcc.Graph(id='stacked_area_chart', className='graph')
                ])
            ])
    elif pathname == "/stacked-bar":
        return html.Div(className="stacked-bar-content", children=[
            html.Header(children=[
                html.Div([ html.Label("Domaine: ", style=dict(fontWeight='bold')), 
                dcc.RadioItems(
                    id='checkbox-1',
                    options=stackedbar_default_options,
                    value=['sciences humaines']  # Set initial value for checkbox-1
                ),
                 ], style=dict(display='flex')
                 ),
                html.Div([ html.Label("Variable: ", style=dict(fontWeight='bold')), 
                dcc.RadioItems(
                    id='checkbox-2',
                    options= stacked_bar_down_options,
                    value=['univ']  # Set initial value for checkbox-2
                )], style=dict(display='flex')),
                html.Button('Cliquez ici', id="button")
            ]),
            html.Main(className='viz-container', children=[
                dcc.Graph(id='stacked_bar', className='graph')
            ])
        ])
    elif pathname == "/radar":
        return html.Div(className="Rader-content", children=[ dcc.Tabs(
            id="radar-tabs",
            value="tab-univ",
            children=[
                dcc.Tab(
                    label="Universités",
                    value="tab-univ",
                    children=[
                        dcc.Graph(
                            id='radar-graph-univ',
                            figure=init_figure()
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Les 10 disciplines les plus importantes",
                    value="tab-discipline",
                    children=[
                        dcc.Graph(
                            id='radar-graph-discipline',
                            figure=update_graph('discipline')
                        ),
                    ],
                ),
            ],
        ),
    ])
    elif pathname == "/sunburst":
        return html.Div(
            className="sunburst-content",
            children=[dcc.Tabs(
                id="sunburst-tabs",
                value="tab1",
                children=[
                    dcc.Tab(
                        label='Langues',
                        value='tab1',
                        children=[
                            dcc.Graph(
                                id="sunburst-langue",
                                figure=update_sunburst_chart('langue')
                            )
                        ],
                    ),
                    dcc.Tab(
                        label='Universités',
                        value='tab2',
                        children=[
                            dcc.Graph(
                                id="sunburst-univ",
                                figure=update_sunburst_chart('univ')
                            )
                        ],
                    ),
                ],
            ),
            ],
        )
    elif pathname == "/back-to-back-bar":
        return html.Div(className="btb-content", children=[dcc.Tabs(
            id="btb-tabs",
            value="tab-master",
            children=[
                dcc.Tab(
                    label="Distribution de l'anglais et du français pour la dissertation",
                    value="tab-master",
                    children=[
                        dcc.Graph(
                            id='btb-graph-master',
                            figure=back_to_back(df,'maîtrise')
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Distribution de l'anglais et du français pour les thèses",
                    value="tab-phd",
                    children=[
                        dcc.Graph(
                            id='btb-graph-phd',
                            figure= back_to_back(df, 'doctorat')
                        ),
                    ],
                ),
            ],
        ),
        ])
    elif pathname == "/box-plots":
        return html.Div(
            className="box-plots-content",
            children=[
                dcc.Tabs(
                    id="box-plots-tabs",
                    value="tab-overview",
                    children=[
                        dcc.Tab(
                            label="Overview",
                            value="tab-overview",
                            children=[
                                dcc.Dropdown(
                                    id="dropdown-value",
                                    options=[
                                        {"label": "Domaine", "value": "domaine"},
                                        {"label": "Language", "value": "langue"},
                                    ],
                                    value="domaine",
                                    className="dropdown",
                                ),
                                html.Div(id="radio-container"),
                                html.Div(id="overview-content"),
                            ],
                        ),
                        dcc.Tab(
                            label="Maîtrise vs Doctorat",
                            value="tab-maitrise-doctorat",
                            children=[
                                dcc.Dropdown(
                                    id="dropdown-value-maitrise-doctorat",
                                    options=[
                                        {"label": "Domaine", "value": "domaine"},
                                        {"label": "Language", "value": "langue"},
                                    ],
                                    value="domaine",
                                    className="dropdown",
                                ),
                                html.Div(id="radio-container-maitrise-doctorat"),
                                html.Div(id="maitrise-doctorat-content"),
                            ],
                        ),
                    ],
                ),
            ],
        )
    else:
        # Return a 404 page or redirect to the Home page
        return html.Div(
            className="404-content",
            children=[
                html.H1("404 - Page Not Found"),
                dcc.Link("Go back to Home", href="/"),
            ],
        )

# Update radio buttons based on dropdown value
@app.callback(
    Output("radio-container", "children"),
    Input("dropdown-value", "value"),
)
def update_radio_buttons(dropdown_value):
    if dropdown_value == "domaine":
        return html.Div(
            [
                # html.H3("Domaine"),
                dcc.RadioItems(
                    id="radio-value",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Sciences Humaines", "value": "sciences humaines"},
                        {"label": "Sciences Naturelles", "value": "sciences naturelles"},
                        {"label": "Inclassable", "value": "inclassable"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    elif dropdown_value == "langue":
        return html.Div(
            [
                # html.H3("Langue"),
                dcc.RadioItems(
                    id="radio-value",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Français", "value": "fr"},
                        {"label": "Anglais", "value": "en"},
                        {"label": "Others", "value": "others"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    else:
        return html.Div()

# Update Overview tab content
@app.callback(
    Output("overview-content", "children"),
    Input("dropdown-value", "value"),
    Input("radio-value", "value"),
)
def update_overview_content(dropdown_value, radio_value):
    filtered_df = df

    if dropdown_value == "domaine":
        if radio_value != "all":
            filtered_df = filtered_df[filtered_df["domaine"] == radio_value]
    elif dropdown_value == "langue":
        if radio_value == "fr":
            filtered_df = filtered_df[filtered_df["langue"] == "fr"]
        elif radio_value == "en":
            filtered_df = filtered_df[filtered_df["langue"] == "en"]
        elif radio_value == "others":
            filtered_df = filtered_df[df["langue"].isin(["es", "it", "de", "pt"])]

    fig = overview_box_plot(filtered_df)

    return dcc.Graph(figure=fig)


# Update radio buttons based on dropdown value for "Maîtrise vs Doctorat" tab
@app.callback(
    Output("radio-container-maitrise-doctorat", "children"),
    Input("dropdown-value-maitrise-doctorat", "value"),
)
def update_radio_buttons_maitrise_doctorat(dropdown_value):
    if dropdown_value == "domaine":
        return html.Div(
            [
                # html.H3("Domaine"),
                dcc.RadioItems(
                    id="radio-value-maitrise-doctorat",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Sciences Humaines", "value": "sciences humaines"},
                        {"label": "Sciences Naturelles", "value": "sciences naturelles"},
                        {"label": "Inclassable", "value": "inclassable"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    elif dropdown_value == "langue":
        return html.Div(
            [
                # html.H3("Langue"),
                dcc.RadioItems(
                    id="radio-value-maitrise-doctorat",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "Français", "value": "fr"},
                        {"label": "Anglais", "value": "en"},
                        {"label": "Others", "value": "others"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    else:
        return html.Div()


# Update Maîtrise vs Doctorat tab content
@app.callback(
    Output("maitrise-doctorat-content", "children"),
    Input("dropdown-value-maitrise-doctorat", "value"),
    Input("radio-value-maitrise-doctorat", "value"),
)
def update_maitrise_doctorat_content(dropdown_value, radio_value):
    
    context_title = ""
    filtered_df_maitrise = df[df['grade'] == 'maîtrise']
    filtered_df_doctorat = df[df['grade'] == 'doctorat']

    if dropdown_value == "domaine":
        context_title = " in all domaines"
        if radio_value != "all":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["domaine"] == radio_value
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["domaine"] == radio_value
            ]
            context_title = " in " + str(radio_value)
            if radio_value == "inclassable":
                context_title = " in other and personalized domaines"
    elif dropdown_value == "langue":
        context_title = " written in all languages"
        if radio_value == "fr":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "fr"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "fr"
            ]
            context_title = " written in French (en Français)"
        elif radio_value == "en":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "en"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "en"
            ]
            context_title = " written in English (en Anglais)"
        elif radio_value == "others":
            filtered_df_maitrise = filtered_df_maitrise[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]
            context_title = " written in other languages"

    fig = mvd_box_plot(filtered_df_maitrise, filtered_df_doctorat, context_title)

    return dcc.Graph(figure=fig)

# Stacked area chart
@app.callback(
    Output('stacked_area_chart', 'figure'),
    [Input('button', 'n_clicks')],
    [State('stacked-area-checkbox-1', 'value'),
     State('stacked-area-checkbox-2', 'value')]
)
def update_stacked_area_chart(n_clicks, checkbox1_value, checkbox2_value):
    if n_clicks is not None:
        print(f"Checkbox 1 value: {checkbox1_value}")
        print(f"Checkbox 2 value: {checkbox2_value}")
        figure = stacked_area_chart.get_figure(df, checkbox1_value, checkbox2_value)
        return figure
    else:
        default_figure = stacked_area_chart.get_figure(df, 'univ', 'count')
        return default_figure

# Sunburst chart
@app.callback(
    Output('sunburstchart', 'figure'),
    [Input('button', 'n_clicks')],
    [State('langue-univ-value', 'value')]
)
def update_sunburst_chart(langue_univ_value):
    figure = sunburst(df, langue_univ_value)
    return figure
    
# Stacked bar chart
@app.callback(
    Output('stacked_bar', 'figure'),
    [Input('button', 'n_clicks')],
    [State('checkbox-1', 'value'),
     State('checkbox-2', 'value')]
)
def update_stacked_bar(n_clicks, checkbox1_value, checkbox2_value):
    if n_clicks is not None:
        print(f"Checkbox 1 value: {checkbox1_value}")
        print(f"Checkbox 2 value: {checkbox2_value}")
        figure = stacked_bar.get_figure(df, checkbox2_value, checkbox1_value)
        return figure
    else:
        default_figure = stacked_bar.get_figure(df, 'univ', 'sciences humaines')
        return default_figure
        
# Radar chart    
@app.callback(
    Output('radar-graph-univ', 'figure'),  # Change id to 'radar-graph-univ'
    [Input('button', 'n_clicks')],
    [State('dropdown-univ-discipline', 'value')]
)
def update_radar_chart(n_clicks, dropdown_univ_discipline_value):
    if n_clicks is not None:
        figure = update_graph(dropdown_univ_discipline_value)
        return figure
    else:
        default_figure = init_figure()
        return default_figure    
