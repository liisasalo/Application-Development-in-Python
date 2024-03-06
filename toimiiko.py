# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 16:59:15 2024

@author: Liisa
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:39:56 2024

@author: Liisa
"""

### BAN438 Exam - candidate no. 74

import dash
from dash import dcc, html, Dash
#from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta

dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css'
load_figure_template('bootstrap')

# Listing needed columns
columns = ['BASE_CUR', 
           'Base Currency', 
           'Unit Multiplier',
           'TIME_PERIOD', 
           'OBS_VALUE']

# Importing data
df = pd.read_csv('EXR.csv', usecols = columns, sep = '[;]', engine = 'python')
df.head()

# Renaming columns
df = df.rename(columns={'BASE_CUR': 'label', 
                        'TIME_PERIOD': 'date', 
                        'OBS_VALUE': 'value'})

# Changing to lowercase
df.columns= df.columns.str.lower()
df.head()

# Checking variable types
df.info()

# Removing commas in value column 
df['value'] = df['value'].replace(',','', regex=True)

# Converting values to float
df['value'] = df['value'].astype(float)

# Changing ate to datetime
df['date'] = pd.to_datetime(df['date'])

df.head()

# Creating a new data set to get last two days for exchange rates
df_last2 = df[df['date'] > '2023-04-26']
df_last2 = df_last2.sort_values('label')

# Renaming columns
df_last2 = df_last2.rename(columns={'label': 'code', 
                        'base currency': 'currency', 
                        'OBS_VALUE': 'exchange rate'})

# Dropping unnecessary column
df_last2.drop(['unit multiplier'], axis = 1, inplace = True)

# Changing date to string to make it look nicer in the table
df_last2['date'] = df_last2['date'].astype(str)

df_last2

# Setting date as index
df.set_index('date', inplace = True)

### Feature 1: table

# Taking wanted columns for table
subset = df_last2.loc[:, ['currency', 'code', 'date', 'value']]

table = dbc.Table.from_dataframe(
    subset, striped=True, bordered=True, hover=True, index=False
)
subset

### Line plot, simple

#Practising making a simple line before implementing it into the app.

# Creating a function to make a line plot

def line_plot(currency, df = df_withindex):
    
    # Extract subsets from data
    subset = df[df['label'].isin(currency)]

    # Create line plot
    fig = px.line(
        subset,
        x = 'date',
        y = 'value',
        color = 'label',
        hover_name = 'label',
    )

    fig.update_layout(
        title = f'Exchange rates for {currency} over time, daily',
        title_x = 0.5,
        yaxis_title = None,
        xaxis_title = None,
        legend_title_text = None
    )
    
    return fig
    
    
fig = line_plot(['AUD'])
#fig.show()

### Line plot, if-sentences

#Improving the line plot above by adding if-sentences.

def line_plot(currency, timeperiod, df = df):
    
    if timeperiod == 'monthly':

        # Create subset dataframe for monthly averages for each currency
        df = df.groupby('label').resample('M').mean().reset_index()
        subset = df[df['label'].isin(currency)]
        
    elif timeperiod == 'yearly':
        df = df.groupby('label').resample('Y').mean().reset_index()
        subset = df[df['label'].isin(currency)]
        
    else:    
        df = df.groupby('label').resample('D').mean().reset_index()
        subset = df[df['label'].isin(currency)]

    # Create line plot
    fig = px.line(
        subset,
        x = 'date',
        y = 'value',
        color = 'label',
        hover_name = 'label',
    )

    fig.update_layout(
        title = f'Exchange rates for {currency} over time, {timeperiod}',
        title_x = 0.5,
        yaxis_title = None,
        xaxis_title = None,
        legend_title_text = None
    )
    
    return fig

fig = line_plot(['AUD'], 'daily')
#fig.show()

### Currency converter

#Practising making a currency converter function before implementing it into the app.

# Creating a function to convert currencies
def currency_converter(currency, amount, df = df):
    
    exchange_rate = df[df['label']== currency]['value'].sort_index().tail(1)
    
    convert = float(exchange_rate) * int(amount)
    
    return convert

currency_converter('EUR', 10)

### Dropdown menu for choosing currency

# Creating a dropdown menu where user can choose a specific currency
currencies = []

for i in df['label'].unique():
    currencies.append({'label' : i, 'value' : i})

options_currencies = dcc.Dropdown(
    options = currencies,
    multi = False,
    id = 'currency_options'
)

### Dropdown for choosing currency, duplicate

#I decided to create a duplicate of the dropdown menu above. Chaining my inputs into just one dropdown didn't work so I added this in order to make my app work.

# Creating a dropdown menu where user can choose a specific currency
currencies = []

for i in df['label'].unique():
    currencies.append({'label' : i, 'value' : i})

options_currencies2 = dcc.Dropdown(
    options = currencies,
    multi = False,
    id = 'currency_options2'
)

### Dropdown menu for choosing amount

# Creating a dropdown menu where user can choose an amount to convert
amount = []

for i in range(0, 550, 50):
    amount.append({'label' : i, 'value' : i})

options_amount = dcc.Dropdown(
    options = amount,
    multi = False,
    id = 'amount'
)

### Buttons for choosing time period

#These buttons allow user to choose if the currency rate is plotted with daily, monthly or yearly rates.

# Creating a dropdown menu where user can choose multiple countries
time_periods = [{'label' : 'daily', 'value' : 'daily'},
                {'label' : 'monthly', 'value' : 'monthly'},
                {'label' : 'yearly', 'value' : 'yearly'}]
                

options_timeperiods = dcc.RadioItems(
    options = time_periods,
    id = 'timeperiod'
)

### Header card

#I decided to make a header card since it looks neat. I used the exam from 2022 as a model.

# Header for the page
header = dbc.Card(
    children = [  

        # Main title on first row
        dbc.Row([
            dbc.Col(html.H2('BAN438 Application Development in Python', style = {'textAlign' : 'center'}))
        ]),
        
        # Details on second row
        dbc.Row([
            dbc.Col(html.P('Exam - candidate number 74', style = {'textAlign' : 'center'}))
        ]),
    ], 
    body = True 
)

### App

load_figure_template('lux')
app = Dash(__name__, external_stylesheets = [dbc.themes.LUX, dbc_css])
server = app.server

app.layout = dbc.Container(
    children = [
        
         # Header card
        dbc.Row(dbc.Col(header, width = 16)),
        html.Br(), 
        
        # Feature 1: Table
        dbc.Row(dbc.Col(children = [
            html.H2('Feature 1: Table'),
            table], width = 16)),
        
            html.Br(), 
        
        # Feature 2: Currency converter
        # Input 1
        dbc.Row(dbc.Col(children = [
            html.H2('Feature 2: Currency converter'),
            html.Br(),
            html.Label('Select currency:'),
            html.Br(),
            options_currencies2], width = 6)),
        
        html.Br(),
        
        # Input 2
        dbc.Row(dbc.Col(children = [
            html.Label('Select amount:'),
            html.Br(),
            options_amount], width = 6)),
        
        html.Br(),
        html.Br(),
        
        # Output 
        dbc.Row(dbc.Col(html.H2(children = '',    
            id = 'exchange_rate', 
        ))),
        
        html.Br(), 
        
        # Feature 3: Line plot with different time periods
        # Input 1
        dbc.Row(dbc.Col(children = [
            html.H2('Feature 3: Line plot with different time periods available'),
            html.Br(),
            html.Label('Select currency:'),
            html.Br(),
            options_currencies], width = 6)),
        
        html.Br(), 
        
        # Input 2
        dbc.Row(dbc.Col(options_timeperiods, width = 4)),
        html.Br(),
        
        # Output 
        dbc.Row(dcc.Graph(id = 'line_plot'))
        
        
    ],
    className = 'dbc'
)

# Making a callback function for the user to interactively change currency and amount
@app.callback(
    Output('exchange_rate', 'children'),
    Input('currency_options2', 'value'),
    Input('amount', 'value'),
)

# Implementing the currency converter function I made above
def currency_converter(currency, amount, df = df):
    
    exchange_rate = df[df['label']== currency]['value'].sort_index().tail(1)
    convert = float(exchange_rate) * int(amount)
    
    
    return f'{amount} {currency} is {round(convert,2)} in Norwegian krones.'

#------------------------------------------------------------------------------

# Making a callback funtion for the user to interactively choose currency and time period for the line plot
@app.callback(
    Output('line_plot', 'figure'),
    Input('currency_options', 'value'),
    Input('timeperiod', 'value'),
)

# Implementing the line plot function I made above
def line_plot(currency, timeperiod, df = df):
    
    if timeperiod == 'monthly':

        # Create subset dataframe for monthly averages for each currency
        df = df.groupby('label').resample('M').mean().reset_index()
        subset = df[df['label'].isin([currency])]
        
    elif timeperiod == 'yearly':
        df = df.groupby('label').resample('Y').mean().reset_index()
        subset = df[df['label'].isin([currency])]
        
    else:    
        df = df.groupby('label').resample('D').mean().reset_index()
        subset = df[df['label'].isin([currency])]

    # Create line plot
    fig = px.line(
        subset,
        x = 'date',
        y = 'value',
        color = 'label',
        hover_name = 'label',
    )

    fig.update_layout(
        title = f'Exchange rates for {currency} over time, {timeperiod}',
        title_x = 0.5,
        yaxis_title = None,
        xaxis_title = None,
        legend_title_text = None
    )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug = True)



