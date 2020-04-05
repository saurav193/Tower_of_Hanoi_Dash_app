import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np

app = dash.Dash(__name__, assets_folder='assets',external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app for DSCI 532 group - 103'

# Chloropleth plot for tab 1
def chart(disks, tower):
    
    num_disks = len(disks)
    
    width = np.zeros(num_disks+5)

    for i in range(1,num_disks+1,1):
        width[-i] = disks[i-1]
    
    source = pd.DataFrame({'y': np.arange(num_disks+5), 'x': width})

    left = alt.Chart(source).encode(
        y=alt.Y('y:O', 
                axis=None),
        x=alt.X('x:Q',
                title='population',
                axis=None,
                sort=alt.SortOrder('descending')),
    ).mark_bar().properties(width = 100)

    right = alt.Chart(source).encode(
        y=alt.Y('y:O', 
                axis=None),
        x=alt.X('x:Q',
                axis=None,
                title='population'),
    ).mark_bar().properties(width = 100)
    
    return alt.concat(left, right, spacing=5).properties(title = tower+" Tower")

header_styles = {'font-family':'arial','font-size':'20px', 'width': '500px'}

app.layout = html.Div([ 
    # Adding Summary and Description of dashboard to the top of the page
    
    html.Div([dbc.Jumbotron([
                dbc.Container([
                      html.H2("Tower of Hanoi game"),
                      dcc.Markdown('''
                    Using this App, play the tower or hanoi game.
                                '''),],
                              )],
                                fluid=True,
                            ),
            ]),

    html.Div([
    ### Add Tabs to the top of the page
        html.Div([

            html.Div([
                html.H2('Starting game :', 
                        style = header_styles),
                dbc.Label("Enter number of Disks to start"),
                dbc.FormGroup(
                [
                    dbc.Input(placeholder="A number from 3-8...",
                                id = 'Num_disks',
                                type='number',
                                value = 3),
                    dbc.Button("Start game", id="reset", color="primary", active=True)
                ])
            ], style={'display': 'inline-block', 'width': '50%', 'border-width':'0'}),
            html.Div([
                html.H2('Making Moves :',
                        style = header_styles),
                dbc.FormGroup(
                        [
                            dbc.Label("From tower:"),
                            dbc.RadioItems(
                                id="from_selector",
                                options=[
                                    {"label": "Left", "value": "Left"},
                                    {"label": "Middle", "value": "Middle"},
                                    {"label": "'Right'", "value": "Right"},
                                ],
                                inline=True,
                                value="Left",
                            )
                        ]),
                dbc.FormGroup(
                        [
                            dbc.Label("To tower:"),
                            dbc.RadioItems(
                                id="to_selector",
                                options=[
                                    {"label": "Left", "value": "Left"},
                                    {"label": "Middle", "value": "Middle"},
                                    {"label": "'Right'", "value": "Right"},
                        ],
                                inline=True,
                                value="Right",
                            ),
                        ]),
                dbc.Form([
                    dbc.Button("Make Move", id="move", color="primary"),
                    html.P(id = "error_message")
                ])
            ],style={'display': 'inline-block', 'width': '50 %', 'border-width':'0'}),
        ], style= {'display': 'inline-block','width': '30%','height': '363px', 'padding-left': '20px', 'border-width':'0'}),

        html.Div(id='Towers', style= {'display': 'inline-block','width': '70%', 'padding-left': '20px', 'border-width':'0'}),
    
    ])

])

# Function to update tabs on clicking
@app.callback(Output('Towers', 'children'),
              [
                  Input('from_selector', 'value'),
                  Input('to_selector', 'value')
              ])
def render_content(from_selector, to_selector):
    """
    This functions updates the values of the tab in our dashboard based on the click on a particular tab
    ---------------------

    Arguments :
    tab - The value of the tab input from the callback function.
    ---------------------

    Returns :
    A html div containing the all the updated plots

    """
    left = []
    middle = []
    right = []

    return html.Div([
        html.H2('Current state of 3 towers ',
                style=header_styles),
        html.Div([ 
            html.Iframe(
                sandbox='allow-scripts',
                id='left_tower',
                height='300',
                width='300',
                style={'border-width':'0'},
                ################ The magic happens here
                srcDoc = chart(left, "Left").to_html()
                ################ The magic happens here
                )],
                style={'display': 'inline-block', 'width': '33%','height': '30px', 'border-width':'0'}
        ),
            html.Div([
                html.Iframe(
                sandbox='allow-scripts',
                id='middle_tower',
                height='300',
                width='300',
                style={'border-width': '0'},
                ################ The magic happens here
                srcDoc = chart(middle, "Middle").to_html()
                ################ The magic happens here
                )],
                style={'display': 'inline-block', 'width': '33%','height': '30px', 'border-width':'0'}
        ),
            html.Div([
                html.Iframe(
                sandbox='allow-scripts',
                id='right_tower',
                height='300',
                width='300',
                style={'border-width': '0'},
                ################ The magic happens here
                srcDoc = chart(right, "Right").to_html()
                ################ The magic happens here
            )],
            style= {'display': 'inline-block','width': '33%','height': '30px', 'border-width':'0'}
        )            
    ])


@app.callback(
    dash.dependencies.Output('left_tower', 'srcDoc'),
    [dash.dependencies.Input('reset', 'n_clicks')],
    [dash.dependencies.State('Num_disks', 'value')]
    )
def update_left_tower(n_clicks, Num_disks):
    """
    This functions updates the scatter plot in tab 1 with user input from drop-down menu received from callback
    ----------------

    Arguments : 
    xaxis_column_name - name of the factor in the with which the plot of avg. hate crime vs factor needs to be created
    ----------------

    Returns :
    A function call to the plot creation function with user input of x-axis.

    """
    disks = list(np.linspace(Num_disks,1,Num_disks))
    updated_plot = chart(disks, "Left").to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('middle_tower', 'srcDoc'),
    [dash.dependencies.Input('reset', 'n_clicks')]
    )
def update_middle_tower(n_clicks):
    disks = []
    updated_plot = chart(disks, "Middle").to_html()
    return updated_plot

@app.callback(
    dash.dependencies.Output('right_tower', 'srcDoc'),
    [dash.dependencies.Input('reset', 'n_clicks')]
    )
def update_right_tower(n_clicks):
    disks = []
    updated_plot = chart(disks, "Right").to_html()
    return updated_plot


if __name__ == '__main__':
    app.run_server(debug=True)
