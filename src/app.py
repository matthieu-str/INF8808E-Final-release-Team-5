import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import preprocess as preproc
import figs_viz
import helper
import callback
import template
from template import external_css

# Load the dataset
df = pd.read_csv("assets/data/thesesMemoiresQC2000-2022-v20230508-1.csv", na_values="?")
df = preproc.to_lowercase(df)
df = preproc.assign_and_range_pages(df)
df = preproc.delete_unecessary_columns(df)
df = preproc.delete_duplicate_disciplines(df)

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
                            html.Span("Home", title="Click to go back to the Home page"),
                            href="/",
                            className="navlink",
                            id="navlink-home",
                        ),
                        dcc.Link(
                            html.Span("Stacked Area Chart", title="Click to display the Stacked Area Chart page"),
                            href="/stacked-area",
                            className="navlink",
                            id="navlink-stacked-area",
                        ),
                        dcc.Link(
                            html.Span("Stacked Bar Chart", title="Click to display the Stacked Bar Charts"),
                            href="/stacked-bar",
                            className="navlink",
                            id="navlink-stacked-bar",
                        ),
                        dcc.Link(
                            html.Span("Radar Chart", title="Click to display the Radar Charts"),
                            href="/radar",
                            className="navlink",
                            id="navlink-radar",
                        ),
                        dcc.Link(
                            html.Span("Sunburst Chart", title="Click to display the Sunburst Charts"),
                            href="/sunburst",
                            className="navlink",
                            id="navlink-sunburst",
                        ),
                        dcc.Link(
                            html.Span("Back to Back Bar Chart", title="Click to display the Back to Back Bar Charts"),
                            href="/back-to-back-bar",
                            className="navlink",
                            id="navlink-back-to-back-bar",
                        ),
                        dcc.Link(
                            html.Span("Box Plots", title="Click to display the Box Plots"),
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
        html.P("This web app was developed as a project in the awesome INF8808E course at Polytechnique Montréal."),
    ],
)

# App layout
app.layout = html.Div(
    className="app-container",
    children=[
        dcc.Location(id="url", refresh=False),
        html.Header(navbar),
        html.Div(id="page-content"),
        footer,
    ],
    #style={"position": "relative", "min-height": "100vh"},
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
                html.H1("Welcome to the Home Page. More is Coming Soon ..."),
                # We will add the content for the Home page here
            ],
        )
    elif pathname == "/stacked-area":
        return html.Div(
            className="stacked-area-content",
            children=[
                html.H1("Stacked Area Chart Coming Soon ..."),
                # Add your content for the Stacked Area Chart page here
            ],
        )
    elif pathname == "/stacked-bar":
        return html.Div(
            className="stacked-bar-content",
            children=[
                html.H1("Stacked Bar Chart Coming Soon ..."),
                # Add your content for the Stacked Bar Chart page here
            ],
        )
    elif pathname == "/radar":
        return html.Div(
            className="radar-content",
            children=[
                html.H1("Radar Chart Coming Soon ..."),
                # Add your content for the Radar Chart page here
            ],
        )
    elif pathname == "/sunburst":
        return html.Div(
            className="sunburst-content",
            children=[
                html.H1("Sunburst Chart Coming Soon ..."),
                # Add your content for the Sunburst Chart page here
            ],
        )
    elif pathname == "/back-to-back-bar":
        return html.Div(
            className="back-to-back-bar-content",
            children=[
                html.H1("Back to Back Bar Chart Coming Soon ..."),
                # Add your content for the Back to Back Bar Chart page here
            ],
        )
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

    fig = px.box(filtered_df, x="année", y="pages")
    fig.update_layout(
        title="Box Plot of Number of Pages by Year",
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        showlegend=True,
    )

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
    filtered_df_maitrise = df[df['grade'] == 'maîtrise']
    filtered_df_doctorat = df[df['grade'] == 'doctorat']

    if dropdown_value == "domaine":
        if radio_value != "all":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["domaine"] == radio_value
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["domaine"] == radio_value
            ]
    elif dropdown_value == "langue":
        if radio_value == "fr":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "fr"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "fr"
            ]
        elif radio_value == "en":
            filtered_df_maitrise = filtered_df_maitrise[
                filtered_df_maitrise["langue"] == "en"
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                filtered_df_doctorat["langue"] == "en"
            ]
        elif radio_value == "others":
            filtered_df_maitrise = filtered_df_maitrise[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]
            filtered_df_doctorat = filtered_df_doctorat[
                df["langue"].isin(["es", "it", "de", "pt"])
            ]

    fig = go.Figure()
    fig.add_trace(
        go.Box(
            x=filtered_df_maitrise["année"],
            y=filtered_df_maitrise["pages"],
            name="Maîtrise",
        )
    )
    fig.add_trace(
        go.Box(
            x=filtered_df_doctorat["année"],
            y=filtered_df_doctorat["pages"],
            name="Doctorat",
        )
    )

    fig.update_layout(
        title="Comparison of Number of Pages by Year for Maîtrise and Doctorat",
        xaxis_title="Year",
        yaxis_title="Number of Pages",
        boxmode="group",
        showlegend=True,
    )

    return dcc.Graph(figure=fig)
