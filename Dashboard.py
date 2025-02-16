import dash
from dash import dcc, html, Input, Output, dash_table
import sqlite3
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)
app.title = "Path Congestion History"

def get_data(query, params=None):
    conn = sqlite3.connect("energy_data.db")
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

app.layout = html.Div([
    html.H1("Path Congestion History Dashboard"),
    html.Div([
        dcc.Dropdown(id='path-dropdown', options=[], multi=True, placeholder="Select Paths (Source -> Sink)"),
        dcc.RangeSlider(1, 12, 1, value=[1, 12], marks={i: f'{pd.to_datetime(f"2020-{i:02d}-01").strftime("%b %Y")}' for i in range(1, 13)}, id='month-slider'),
        dcc.Input(id='top-x', type='number', placeholder='Top X Paths', min=1, value=5)
    ]),
    dcc.Graph(id='monthly-congestion-bar'),
    dcc.Graph(id='hourly-congestion-bar'),
    dash_table.DataTable(id='most-congested-paths')
])

@app.callback(Output('path-dropdown', 'options'), Input('top-x', 'value'))
def load_paths(_):
    df = get_data("SELECT DISTINCT [Settlement Location] FROM DA_LMP_MONTHLY")
    return [{'label': loc, 'value': loc} for loc in df['Settlement Location']]

@app.callback(Output('monthly-congestion-bar', 'figure'), Input('path-dropdown', 'value'), Input('month-slider', 'value'))
def update_bar_chart(paths, month_range):
    if not paths:
        return px.bar()
    query = "SELECT * FROM DA_LMP_MONTHLY WHERE [Settlement Location] IN ({}) AND strftime('%m', MONTH) BETWEEN ? AND ?".format(','.join(['?']*len(paths)))
    df = get_data(query, params=paths + [str(month_range[0]).zfill(2), str(month_range[1]).zfill(2)])
    df['MONTH'] = pd.to_datetime(df['MONTH']).dt.strftime('%b %Y')
    fig = px.bar(df, x='MONTH', y='MCC', color='Settlement Location', barmode='group')
    return fig

@app.callback(Output('hourly-congestion-bar', 'figure'), Input('monthly-congestion-bar', 'clickData'), Input('path-dropdown', 'value'))
def update_hourly_chart(clickData, paths):
    if not clickData or not paths:
        return px.bar()
    selected_month = pd.to_datetime(clickData['points'][0]['x']).strftime('%Y-%m')
    query = "SELECT Interval, [Settlement Location], MCC FROM DA_LMP_HOURLY WHERE substr(Interval, 7, 4) || '-' || substr(Interval, 1, 2) = ? AND [Settlement Location] IN ({})".format(','.join(['?']*len(paths)))
    df = get_data(query, params=[selected_month] + paths)
    df['Interval'] = pd.to_datetime(df['Interval'], format='%m/%d/%Y %H:%M:%S', errors='coerce').dt.strftime('%Y-%m-%d %H:%M')
    fig = px.bar(df, x='Interval', y='MCC', color='Settlement Location', barmode='group')
    return fig

@app.callback(Output('most-congested-paths', 'data'), Input('top-x', 'value'), Input('month-slider', 'value'))
def update_most_congested(top_x, month_range):
    query = "SELECT [Settlement Location], SUM(MCC) as MCC FROM DA_LMP_MONTHLY WHERE strftime('%m', MONTH) BETWEEN ? AND ? GROUP BY [Settlement Location] ORDER BY MCC DESC LIMIT ?"
    df = get_data(query, params=[str(month_range[0]).zfill(2), str(month_range[1]).zfill(2), top_x])
    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
