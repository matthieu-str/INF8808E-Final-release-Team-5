def update_navlink_styles(pathname):
    "Helper function to render the navigation links"
    
    styles = [{"backgroundColor": "grey", "border-radius": "30px"} for _ in range(7)]
    if pathname == "/":
        styles[0]["backgroundColor"] = "blue"
    elif pathname == "/stacked-area":
        styles[1]["backgroundColor"] = "blue"
    elif pathname == "/stacked-bar":
        styles[2]["backgroundColor"] = "blue"
    elif pathname == "/radar":
        styles[3]["backgroundColor"] = "blue"
    elif pathname == "/sunburst":
        styles[4]["backgroundColor"] = "blue"
    elif pathname == "/back-to-back-bar":
        styles[5]["backgroundColor"] = "blue"
    elif pathname == "/box-plots":
        styles[6]["backgroundColor"] = "blue"
    return styles
