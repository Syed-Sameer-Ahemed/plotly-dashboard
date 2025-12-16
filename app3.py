import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# ----------------------------
# Sample Data
# ----------------------------
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [12000, 15000, 17000, 16000, 20000, 22000],
    "Profit": [3000, 4000, 4500, 4200, 6000, 6500],
    "Region": ["East", "West", "East", "North", "South", "West"]
}
df = pd.DataFrame(data)

# ----------------------------
# CARD STYLE (MUST BE HERE)
# ----------------------------
def card_style():
    return {
        "border": "1px solid #ddd",
        "borderRadius": "10px",
        "padding": "20px",
        "width": "250px",
        "textAlign": "center",
        "boxShadow": "2px 2px 10px rgba(0,0,0,0.1)",
        "backgroundColor": "#ffffff"
    }

# ----------------------------
# Dash App Initialization
# ----------------------------
app = dash.Dash(__name__)
app.title = "Sales Dashboard"

# ----------------------------
# Layout
# ----------------------------
app.layout = html.Div(
    style={"fontFamily": "Arial", "padding": "20px", "backgroundColor": "#f4f6f9"},
    children=[

        html.H1(
            "📊 Sales & Profit Dashboard",
            style={"textAlign": "center", "marginBottom": "30px"}
        ),

        html.Div(
            style={"width": "300px", "margin": "auto"},
            children=[
                html.Label("Select Region"),
                dcc.Dropdown(
                    id="region-dropdown",
                    options=[{"label": r, "value": r} for r in df["Region"].unique()],
                    value="East",
                    clearable=False
                )
            ]
        ),

        html.Br(),

        html.Div(
            style={"display": "flex", "justifyContent": "space-around"},
            children=[
                html.Div(id="total-sales", style=card_style()),
                html.Div(id="total-profit", style=card_style())
            ]
        ),

        html.Br(),

        dcc.Graph(id="sales-line-chart"),
        dcc.Graph(id="profit-bar-chart")
    ]
)

# ----------------------------
# Callback
# ----------------------------
@app.callback(
    [
        Output("sales-line-chart", "figure"),
        Output("profit-bar-chart", "figure"),
        Output("total-sales", "children"),
        Output("total-profit", "children")
    ],
    Input("region-dropdown", "value")
)
def update_dashboard(selected_region):

    filtered_df = df[df["Region"] == selected_region]

    sales_fig = px.line(
        filtered_df,
        x="Month",
        y="Sales",
        title=f"Sales Trend - {selected_region}",
        markers=True
    )

    profit_fig = px.bar(
        filtered_df,
        x="Month",
        y="Profit",
        title=f"Profit Distribution - {selected_region}"
    )

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()

    return (
        sales_fig,
        profit_fig,
        [html.H4("Total Sales"), html.H2(f"₹ {total_sales:,}")],
        [html.H4("Total Profit"), html.H2(f"₹ {total_profit:,}")]
    )

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)