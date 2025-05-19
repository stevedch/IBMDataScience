# app.py - Full Dash Application for Automobile Sales Analysis

import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(url)

# Preprocessing
recession_df = df[df['Recession'] == 1]
no_recession_df = df[df['Recession'] == 0]

# App initialization
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Automobile Sales Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in sorted(df['Year'].unique())],
            value=2010
        )
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div(id='outputdiv', style={'padding': '10px', 'fontSize': '20px'}),

    dcc.Graph(id='sales_by_vehicle_type'),
    dcc.Graph(id='recession_stats'),
    dcc.Graph(id='yearly_stats')
])

# Callback for vehicle sales graph
@app.callback(
    Output('sales_by_vehicle_type', 'figure'),
    Input('year-dropdown', 'value')
)
def update_vehicle_sales(year):
    filtered_df = df[df['Year'] == year]
    vehicle_sales = filtered_df.groupby('Vehicle_Type')['Automobile_Sales'].sum().reset_index()
    fig = px.bar(vehicle_sales, x='Vehicle_Type', y='Automobile_Sales', color='Vehicle_Type',
                 title=f'Automobile Sales by Vehicle Type in {year}')
    return fig

# Callback for recession report
@app.callback(
    Output('recession_stats', 'figure'),
    Input('year-dropdown', 'value')
)
def update_recession_graph(year):
    recession_data = recession_df[recession_df['Year'] == year]
    if recession_data.empty:
        return px.bar(title=f"No recession data available for {year}")
    grouped = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
    fig = px.bar(grouped, x='Vehicle_Type', y='Automobile_Sales', color='Vehicle_Type',
                 title=f'Recession Report: Avg Sales by Vehicle Type ({year})')
    return fig

# Callback for yearly report
@app.callback(
    Output('yearly_stats', 'figure'),
    Input('year-dropdown', 'value')
)
def update_yearly_graph(year):
    data = df[df['Year'] == year].groupby('Month')['Automobile_Sales'].sum().reset_index()
    fig = px.line(data, x='Month', y='Automobile_Sales', title=f'Yearly Monthly Sales Trend in {year}')
    return fig

# Run the app locally
if __name__ == '__main__':
    app.run_server(debug=True)
