import plotly.express as px
import pandas as pd
from preprocess import other_languages

def get_figure(df, y_axis, mode):

    df_count = df.groupby(by=['année', f'{y_axis}'], as_index=False).count()[['année', f'{y_axis}', 'discipline']]
    df_count.rename(columns={"discipline": "count"}, inplace=True)

    if y_axis == 'langue':
        year_min = df["année"].min()
        year_max = df["année"].max()
        df_count = other_languages(df_count, year_min, year_max)

    if mode == "percentage":
        count_tot = df_count.groupby(["année"], as_index=False).sum("count")
        count_tot.rename(columns={"count": "count_total"}, inplace=True)
        df_count = pd.merge(left=df_count, right=count_tot, how="left", on="année")
        df_count["percentage"] = 100 * df_count["count"] / df_count["count_total"]

    fig = px.area(df_count, x="année", y=f"{mode}", color=f"{y_axis}")

    fig.update_layout(height=600, width=1200)

    return fig