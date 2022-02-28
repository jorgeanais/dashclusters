from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

app = Dash(__name__)

df = pd.read_csv("data/clustering_data.csv")
for col in df.columns[6:]:
    df[col] = df[col].map(str)


app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(df.columns.values[6:], "DBSCAN", id="algorithm-column"),
            ],
            style={"width": "48%", "display": "inline-block"},
        ),
        dcc.Graph(id="clusters-graphic", style={"width": "90vh", "height": "90vh"}),
    ]
)


@app.callback(Output("clusters-graphic", "figure"), Input("algorithm-column", "value"))
def update_figure(selected_algorithm):

    fig = px.scatter(
        df,
        x="x0",
        y="x1",
        color=selected_algorithm,
        hover_data=["y", selected_algorithm],
        log_x=False,
        size_max=55,
    )

    fig.update_layout(transition_duration=100)

    return fig


if __name__ == "__main__":
    app.run_server(debug=False, port=8080, host="0.0.0.0")
