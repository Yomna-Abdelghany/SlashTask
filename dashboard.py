import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Load data
data = pd.read_csv("Cleaned_Amazon_Sale_Report.csv", encoding='latin1')
data['Date'] = pd.to_datetime(data['Date'])

# Verify column names
print(data.columns)

# Initialize Dash app with Bootstrap components
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Sales Insights Dashboard", className='text-center text-primary mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Label('Select Metric:'),
            dcc.Dropdown(
                id='metric-dropdown',
                options=[
                    {'label': 'Top Products', 'value': 'Product'},
                    {'label': 'Top Categories', 'value': 'Category'}
                ],
                value='Product',
                clearable=False,
                className='mb-4'
            ),
            html.Label('Select Sales Channel:'),
            dcc.Dropdown(
                id='sales-channel-dropdown',
                options=[{'label': 'All', 'value': 'All'}] + [{'label': channel, 'value': channel} for channel in data['Sales Channel '].unique()],
                value='All',
                clearable=False,
                className='mb-4'
            ),
            html.Label('Select Date Range:'),
            dcc.DatePickerRange(
                id='date-picker',
                start_date=data['Date'].min(),
                end_date=data['Date'].max(),
                display_format='YYYY-MM-DD',
                className='mb-4'
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart'), width=12)
    ])
], fluid=True)

# Define callbacks
@app.callback(
    Output('bar-chart', 'figure'),
    [
        Input('metric-dropdown', 'value'),
        Input('sales-channel-dropdown', 'value'),
        Input('date-picker', 'start_date'),
        Input('date-picker', 'end_date')
    ]
)
def update_bar_chart(selected_metric, selected_channel, start_date, end_date):
    # Filter data based on date range and sales channel
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    if selected_channel != 'All':
        filtered_data = filtered_data[filtered_data['Sales Channel '] == selected_channel]
    
    # Update top data based on selected metric
    if selected_metric == 'Product':
        top_data = filtered_data.groupby('SKU')['Amount'].sum().nlargest(10).reset_index()
        fig = px.bar(top_data, x='Amount', y='SKU', orientation='h', title=f'Top Selling Products in {selected_channel} channel from {start_date} to {end_date}')
    else:
        top_data = filtered_data.groupby('Category')['Amount'].sum().nlargest(10).reset_index()
        fig = px.bar(top_data, x='Amount', y='Category', orientation='h', title=f'Top Selling Categories in {selected_channel} channel from {start_date} to {end_date}')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)