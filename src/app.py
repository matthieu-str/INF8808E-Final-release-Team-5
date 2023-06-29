import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import preprocess as preproc
from box_plot import overview_box_plot, mvd_box_plot
import callback
from template import external_css
import stacked_bar
import stacked_area_chart
from back_to_back_bar import back_to_back
from sunburstchart import sunburst
from radar_chart import init_figure, update_graph

# Create the Dash app
app = dash.Dash(__name__)

# Load the dataset and perform preprocessing
df = pd.read_csv("assets/data/thesesMemoiresQC2000-2022-v20230508-1.csv", na_values="?")
df = preproc.to_lowercase(df)
df = preproc.assign_and_range_pages(df)
df = preproc.rename_inclassable(df)
df = preproc.delete_unecessary_columns(df)
df = preproc.delete_duplicate_disciplines(df)


# Update labels of stacked bar chart
stackedbar_default_options = [
                        {'label': 'Sciences Humaines', 'value': 'sciences humaines'},
                        {'label': 'Sciences Naturelles', 'value': 'sciences naturelles'},
                        {'label': 'Programme individualisé ou inconnu', 'value': 'programme individualisé ou inconnu'}
                    ]
stacked_bar_down_options = [
                        {'label': "Niveau d'études", 'value': 'grade'},
                        {'label': 'Universités', 'value': 'univ'},
                        {'label': 'Langues', 'value': 'langue'},
                        {'label': 'Nombre de pages', 'value': 'range of pages'}
                    ]


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
                            html.Span("Accueil", title="Cliquez pour revenir à la page d'accueil"),
                            href="/",
                            className="navlink",
                            id="navlink-home",
                        ),
                        dcc.Link(
                            html.Span("Stacked Area Chart", title="Cliquez pour afficher les Stacked Area Chart page"),
                            href="/stacked-area",
                            className="navlink",
                            id="navlink-stacked-area",
                        ),
                        dcc.Link(
                            html.Span("Stacked Bar Chart", title="Cliquez pour afficher les Stacked Bar Charts"),
                            href="/stacked-bar",
                            className="navlink",
                            id="navlink-stacked-bar",
                        ),
                        dcc.Link(
                            html.Span("Radar Chart", title="Cliquez pour afficher les Radar Charts"),
                            href="/radar",
                            className="navlink",
                            id="navlink-radar",
                        ),
                        dcc.Link(
                            html.Span("Sunburst Chart", title="Cliquez pour afficher les Sunburst Charts"),
                            href="/sunburst",
                            className="navlink",
                            id="navlink-sunburst",
                        ),
                        dcc.Link(
                            html.Span("Back to Back Bar Chart", title="Cliquez pour afficher les Back to Back Bar Charts"),
                            href="/back-to-back-bar",
                            className="navlink",
                            id="navlink-back-to-back-bar",
                        ),
                        dcc.Link(
                            html.Span("Box Plot", title="Cliquez pour afficher les Box Plots"),
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
        html.P("Cette application Web a été développée en tant que projet dans le formidable cours INF8808E de Polytechnique Montréal."),
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
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return html.Div(
            className="home-content",
            children=[
                html.H1(
                    "Tracer les horizons du savoir : Un parcours visuel de la recherche en études supérieures au Québec",
                    className="title"
                ),
                html.P(
                    "PROJET INF8808E - 2023",
                    className="subtitle"
                ),
                html.H2(
                    "Les universités québécoises sont devenues des établissements réputés pour leur excellence académique, attirant un large éventail d'étudiants du monde entier. Notre projet vise à explorer visuellement la riche tapisserie des thèses et mémoires produits au sein de ces institutions. En analysant les tendances et les changements au fil du temps, nous visons à découvrir des informations précieuses sur le domaine des études supérieures. Le tableau de bord du projet fournit des informations sur la répartition des diplômes, les affiliations universitaires et les tendances disciplinaires de 2000 à 2022. Nos utilisateurs cibles sont les chercheurs, les administrateurs d'université, les bibliothèques, les institutions de financement, les consultants en recherche, les publications universitaires, les étudiants diplômés, les futurs étudiants et le grand public. En acquérant une meilleure compréhension du milieu de la recherche, les utilisateurs peuvent prendre des décisions éclairées, suivre les tendances émergentes et contribuer à l'avancement des connaissances au sein de la communauté universitaire québécoise.",
                    className="section-text"
                ),
                html.P(
                    "Les visualisations réalisées peuvent être classées en deux sections, la première étant consacrée aux tendances temporelles de l'évolution des publications au fil des ans et la seconde à la présentation de la répartition du nombre de publications à un niveau plus granulaire. Pour plus d'informations, lisez les sections ci-dessous.",
                    className="section-text"
                ),
                html.H2(
                    "Section 1",
                    className="section-title"
                ),
                html.P(
                    [
                        html.B("Stacked Area chart"),
                        ": affiche les tendances temporelles du nombre de publications en fonction de variables majeures telles que les domaines, les universités, les langues et les niveaux d'études. Ces informations peuvent être affichées en mode pourcentage ou comptage."
                    ],
                    className="section-text"
                ),
                html.P(
                    [
                        html.B("Back to back chart"),
                        ": présente l'évolution de la répartition des langues entre les années et les diplômes (maîtrise et doctorat) dans les universités québécoises entre 2000 et 2022."
                    ],
                    className="section-text"
                ),
                html.P(
                    [
                        html.B("Box plot"),
                        ": aussi appelé diagramme en boîte, montre l'évolution de la longueur des publications au fil des années en fonction des niveaux d'études, des domaines ou des langues."
                    ],
                    className="section-text"
                ),
                html.H2(
                    "Section 2",
                    className="section-title"
                ),
                html.P(
                    [
                        html.B("Stacked bar chart"),
                        ": donne un aperçu de la répartition des langues, des diplômes, des universités ou même du nombre de pages dans les différentes disciplines qui ont été catégorisées en fonction du domaine principal."
                    ],
                    className="section-text"
                ),
                html.P(
                    [
                        html.B("Radar chart"),
                        ": présente des informations relatives aux différents types de diplômes (Maîtrise et doctorat). Ces informations peuvent être visualisées sur différentes universités ou sur les plus importantes disciplines existantes."
                    ],
                    className="section-text"
                ),
                html.P(
                    [
                        html.B("Sunburst chart"),
                        ": vise à montrer la répartition des langues des documents en fonction des domaines ou des universités."
                    ],
                    className="section-text"
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
                    html.Button('Sélectionnez puis Cliquez ici', id="button"),
                    ]),
                html.Main(className='viz-container', children=[
                    dcc.Graph(id='stacked_area_chart', className='graph')
                ])
            ])
    elif pathname == "/stacked-bar":
        return html.Div(className="stacked-bar-content", children=[
            html.Header(children=[
                html.Div([ html.Label("Domaine : ", style=dict(fontWeight='bold')), 
                dcc.RadioItems(
                    id='checkbox-1',
                    options=stackedbar_default_options,
                    value=['sciences humaines']  # Set initial value for checkbox-1
                ),
                 ], style=dict(display='flex')
                 ),
                html.Div([ html.Label("Publications par : ", style=dict(fontWeight='bold')), 
                dcc.RadioItems(
                    id='checkbox-2',
                    options= stacked_bar_down_options,
                    value=['univ']  # Set initial value for checkbox-2
                )], style=dict(display='flex')),
                html.Button('Sélectionnez puis Cliquez ici', id="button")
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
                            figure=init_figure(df)
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Les 10 disciplines les plus importantes",
                    value="tab-discipline",
                    children=[
                        dcc.Graph(
                            id='radar-graph-discipline',
                            figure=update_graph(df,'discipline')
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
                            id='btb-graph',
                            figure=back_to_back(df,'maîtrise')
                        ),
                    ],
                ),
                dcc.Tab(
                    label="Distribution de l'anglais et du français pour les thèses",
                    value="tab-phd",
                    children=[
                        dcc.Graph(
                            id='btb-graph',
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
                            label="Vue d'ensemble",
                            value="tab-overview",
                            children=[
                                dcc.Dropdown(
                                    id="dropdown-value",
                                    options=[
                                        {"label": "Domaine", "value": "domaine"},
                                        {"label": "Langue", "value": "langue"},
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
                                        {"label": "Langue", "value": "langue"},
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

# Update radio buttons based on dropdown value (box plot)
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
                        {"label": "Tous", "value": "all"},
                        {"label": "Sciences Humaines", "value": "sciences humaines"},
                        {"label": "Sciences Naturelles", "value": "sciences naturelles"},
                        {"label": "Programme individualisé ou inconnu", "value": "programme individualisé ou inconnu"},
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
                        {"label": "Toutes", "value": "all"},
                        {"label": "Français", "value": "fr"},
                        {"label": "Anglais", "value": "en"},
                        {"label": "Autres", "value": "others"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    else:
        return html.Div()

# Update Overview tab content (box plot)
@app.callback(
    Output("overview-content", "children"),
    Input("dropdown-value", "value"),
    Input("radio-value", "value"),
)
def update_overview_content(dropdown_value, radio_value):
    filtered_df = df
    context_title =""
  
    if dropdown_value == "domaine":
        context_title = " dans tous les domaines"
        if radio_value != "all":
            filtered_df = filtered_df[filtered_df["domaine"] == radio_value]
            context_title = " dans les " + str(radio_value)
            if radio_value == "programme individualisé ou inconnu":
                context_title = " dans les programmes individualisés ou inconnus"

    elif dropdown_value == "langue":
        context_title = " rédigées dans toutes les langues"
        if radio_value == "fr":
            filtered_df = filtered_df[filtered_df["langue"] == "fr"]
            context_title = " rédigées en Français"
        elif radio_value == "en":
            filtered_df = filtered_df[filtered_df["langue"] == "en"]
            context_title = " rédigées en Anglais"
        elif radio_value == "others":
            filtered_df = filtered_df[df["langue"].isin(["es", "it", "de", "pt"])]
            context_title = " rédigées dans les autres langues"

    fig = overview_box_plot(filtered_df, context_title)

    return dcc.Graph(figure=fig)


# Update radio buttons based on dropdown value for "Maîtrise vs Doctorat" tab (box plot)
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
                        {"label": "Tous", "value": "all"},
                        {"label": "Sciences Humaines", "value": "sciences humaines"},
                        {"label": "Sciences Naturelles", "value": "sciences naturelles"},
                        {"label": "Programme individualisé ou inconnu", "value": "programme individualisé ou inconnu"},
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
                        {"label": "Toutes", "value": "all"},
                        {"label": "Français", "value": "fr"},
                        {"label": "Anglais", "value": "en"},
                        {"label": "Autres", "value": "others"},
                    ],
                    value="all",
                    className="radio",
                ),
            ]
        )
    else:
        return html.Div()


# Update Maîtrise vs Doctorat tab content (box plot)
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
        context_title = " dans tous les domaines"
        if radio_value != "all":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["domaine"] == radio_value
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["domaine"] == radio_value
            ]
            context_title = " dans les " + str(radio_value)
            if radio_value == "programme individualisé ou inconnu":
                context_title = " dans les programmes individualisés ou inconnus"
    elif dropdown_value == "langue":
        context_title = " rédigées dans toutes les langues"
        if radio_value == "fr":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "fr"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "fr"
            ]
            context_title = " rédigées en Français"
        elif radio_value == "en":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "en"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "en"
            ]
            context_title = " rédigées en Anglais"
        elif radio_value == "others":
            filtered_df_maitrise = filtered_df_maitrise[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]
            context_title = " rédigées dans les autres langues"

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
        figure = update_graph(df,dropdown_univ_discipline_value)
        return figure
    else:
        default_figure = init_figure(df)
        return default_figure 
# back to back
@app.callback(
    Output('btb-graph', 'figure'),
    [Input('button', 'n_clicks')],
    [State('btb-tabs', 'value')]
)
def update_back_to_back_graph(tab_value):
    if n_clicks is not None:
        if tab_value == "tab-master":
            figure = back_to_back(df, 'maîtrise')
        elif tab_value == "tab-phd":
            figure = back_to_back(df, 'doctorat')

    else:
        figure = back_to_back(df, 'maîtrise')
    figure.update_layout(staticPlot=True)
    return figure
