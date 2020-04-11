import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
import altair as alt
import pandas as pd
import numpy as np

from src.stack import Stack

app = dash.Dash(__name__, assets_folder='assets',external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Tower of Hanoi'

stacks = []
inv_f = 0
moves = 0
left = []
middle = []
right = []
min_moves = 0
game_completion_f =0
final_answer = []

# Chloropleth plot for tab 1
def chart(disks, tower):
    
    num_disks = len(disks)
    
    width = np.zeros(10)

    for i in range(1,num_disks+1,1):
        width[-i] = disks[i-1]
    
    source = pd.DataFrame({'y': np.arange(10), 'x': width})

    left = alt.Chart(source).encode(
        y=alt.Y('y:O', 
                axis=None),
        x=alt.X('x:Q',
                axis=None,
                scale=alt.Scale(domain=(0, 10)),
                sort=alt.SortOrder('descending')),
    ).mark_bar().properties(width = 100, height = 150)

    right = alt.Chart(source).encode(
        y=alt.Y('y:O', 
                axis=None),
        x=alt.X('x:Q',
                axis=None,
                scale=alt.Scale(domain=(0, 10))),
    ).mark_bar().properties(width = 100, height = 150)
    
    return alt.concat(left, right, spacing=5).properties(title = tower+" Tower")

def update_stacks(from_selector, to_selector):
    
    global stacks
    global left
    global middle
    global right
    global moves
    global inv_f

    choices = [i.get_name() for i in stacks]
    
    for i in range(3):
        if str(from_selector) == choices[i]:
            from_stack = stacks[i]
            break

    for i in range(3):
        if str(to_selector) == choices[i]:
            to_stack = stacks[i]
            break
 
    if from_stack.is_empty():
        inv_f = 1

    elif (to_stack.is_empty()) | (from_stack.peek() < to_stack.peek()):
        disk = from_stack.pop()
        to_stack.push(disk)

        left = stacks[0].get_items()
        middle = stacks[1].get_items()
        right = stacks[2].get_items()
        moves = moves+1
        inv_f = 0
    else:
        inv_f = 1
    
    return left, middle, right

def initialize_stack(num_disks):
    global stacks
    global left
    global middle
    global right
    global moves
    global inv_f
    global min_moves
    global final_answer
    global game_completion_f

    stacks = []
    left_stack = Stack("Left")
    middle_stack = Stack("Middle")
    right_stack = Stack("Right")

    stacks.append(left_stack)
    stacks.append(middle_stack)
    stacks.append(right_stack)

    for i in range(num_disks, 0, -1):
        stacks[0].push(i)
    
    left = stacks[0].get_items()
    middle = stacks[1].get_items()
    right = stacks[2].get_items()
    moves = 0
    inv_f = 0
    min_moves = 2**num_disks - 1
    game_completion_f = 0
    final_answer = left

def check_completion():
    global right
    global final_answer
    global game_completion_f
    global moves

    if final_answer == right:
        game_completion_f = 1
        moves = 0
        return game_completion_f
    else:
        return game_completion_f

def get_moves():
    return moves

def get_flag():
    return inv_f

def get_left():
    return left

def get_middle():
    return middle

def get_right():
    return right

def get_min_moves():
    return min_moves

header_styles = {'font-family':'arial','font-size':'20px', 'width': '200px'}

err_styles = {'font-family':'arial','font-size':'12px', 'color': 'red', 'width': '200px'}

complete_style = {'font-family':'calibri','font-size':'24px', 'color': 'blue', 'width': '400px'}

app.layout = html.Div([ 
    # Adding Summary and Description of dashboard to the top of the page
    
    html.Div([dbc.Jumbotron([
                dbc.Container([
                      html.H2("Tower of Hanoi"),
                      dcc.Markdown('''
                                Rules of the game are:

                                - Start the game from the Left Tower with the required number of disks. Aim is to move all the disks to the Right Tower.
                                - Only a *lower* value disk can be placed on top of a *higher* value disk. Only 1 disk can be moved in any move.
                                - Try to complete the game in minimum number of moves
                                - The optimum number of moves is shown in "Min Moves" which depends on the number of disks.
                                '''),],
                              )], fluid = True
                            ),
            ]),

    html.Div([
    ### Add Tabs to the top of the page
        html.Div([

            html.Div([
                html.H2('Starting game :', 
                        style = header_styles),
                dbc.Label("Enter the number of Disks(1-10) to start"),
                dbc.FormGroup(
                [
                    dbc.Input(  
                                id = 'Num_disks',
                                type='number',
                                value = 3),
                    dbc.Button("Start game", id="reset", color="primary", active=False)
                ]),
            ], style={'display': 'inline-block', 'width': '50%', 'padding-right':'20px'}),
            html.Div([
                html.H2('Making Moves :',
                        style = header_styles),
                dbc.Form(
                    [
                        dbc.Label("Min Moves :"),
                        html.P(id = "min_moves", style = {'font-size':'15px','padding-left': '5px','padding-top': '12px'})
                    ], inline = True
                ),
                dbc.Form(
                    [
                        dbc.Label("Your Moves :"),
                        html.P(id = "your_moves", style = {'font-size':'15px', 'padding-left': '5px','padding-top': '12px'}),
                        
                    ], inline = True
                ),
                dbc.FormGroup(
                        [
                            dbc.Label("From tower:"),
                            dbc.RadioItems(
                                id="from_selector",
                                options=[
                                    {"label": "Left", "value": "Left"},
                                    {"label": "Middle", "value": "Middle"},
                                    {"label": "Right", "value": "Right"},
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
                                    {"label": "Right", "value": "Right"},
                        ],
                                inline=True,
                                value="Right",
                            ),
                        ]),
                dbc.Form([
                    dbc.Button("Make Move", id="move", color="primary", active = False),
                    html.P(id = "error_msg", style = err_styles)
                ])
            ],style={'display': 'inline-block', 'width': '50 %', 'border-width':'0'}),
        ], style= {'display': 'inline-block','width': '40%', 'padding-left': '20px', 'border-width':'0'}),

        html.Div([
            html.H2('Current state of 3 towers ',
                style=header_styles),
            html.Div([
                html.Div([ 
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='left_tower',
                        height='200',
                        width='300',
                        style={'border-width':'0'},
                        srcDoc = chart([], "Left").to_html()
                        )],
                        style={'display': 'inline-block', 'width': '33%','height': '30px', 'border-width':'0'}
                ),
                html.Div([
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='middle_tower',
                        height='200',
                        width='300',
                        style={'border-width': '0'},
                        srcDoc = chart([], "Middle").to_html()
                        )],
                        style={'display': 'inline-block', 'width': '33%','height': '30px', 'border-width':'0'}
            ),
                html.Div([
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='right_tower',
                        height='200',
                        width='300',
                        style={'border-width': '0'},
                        srcDoc = chart([], "Right").to_html()
                        )],
                        style= {'display': 'inline-block','width': '33%','height': '30px', 'border-width':'0'}
            )], id='Towers'),
                html.Div(id = "complete_msg", style = complete_style)], 
            style= {'display': 'inline-block','width': '60%'})
    
    ]),
    html.Div(0, id='num_moves', style={'display': 'none'}),
    html.Div(0, id='invalid_flag', style={'display': 'none'}),
    html.Div([], id='left_list', style={'display': 'none'}),
    html.Div([], id='middle_list', style={'display': 'none'}),
    html.Div([], id='right_list', style={'display': 'none'}),
    html.Div(id='moves_completed', style={'display': 'none'}),
    html.Div(id='game_started', style={'display': 'none'}),
    html.Div(id='game_complete', style={'display': 'none'})
    
])

#Starting the game
@app.callback(
    dash.dependencies.Output('game_started', 'children'),
    [dash.dependencies.Input('reset', 'n_clicks')],
    [dash.dependencies.State('Num_disks', 'value')]
    )
def update_game_start(n_clicks, Num_disks):
    if n_clicks is None:
        raise PreventUpdate

    initialize_stack(Num_disks)
    return 0

#Getting min moves
@app.callback(
    dash.dependencies.Output('min_moves', 'children'),
    [dash.dependencies.Input('game_started', 'children')]
    )
def update_min_moves(game_started):
    return get_min_moves() 

#Update moves
@app.callback(Output('moves_completed', 'children'),
                [dash.dependencies.Input('move', 'n_clicks')],
              [
                  dash.dependencies.State('from_selector', 'value'),
                  dash.dependencies.State('to_selector', 'value')
              ])
def finish_move(n_clicks, from_selector, to_selector):
    if n_clicks is None:
        raise PreventUpdate
    
    update_stacks(from_selector, to_selector)
    return 0

#Update moves
@app.callback(Output('num_moves', 'children'),
            [dash.dependencies.Input('game_started', 'children'),
            dash.dependencies.Input('moves_completed', 'children')])
def update_moves(game_started, moves_completed):
    return get_moves()

#Update flag
@app.callback(Output('invalid_flag', 'children'),
            [dash.dependencies.Input('game_started', 'children'),
            dash.dependencies.Input('moves_completed', 'children')])
def update_flags(game_started, moves_completed):
    return get_flag()

#Check completion
@app.callback(Output('game_complete', 'children'),
            [dash.dependencies.Input('moves_completed', 'children')])
def check_complete(moves_completed):
    return check_completion()


#Updating local with global lists
@app.callback(
    dash.dependencies.Output('left_list', 'children'),
    [dash.dependencies.Input('game_started', 'children'),
    dash.dependencies.Input('moves_completed', 'children')]
    )
def update_left_local(reset, moves_completed):
    # print(get_left(), "updating local")
    return get_left()

@app.callback(
    dash.dependencies.Output('middle_list', 'children'),
    [dash.dependencies.Input('game_started', 'children'),
    dash.dependencies.Input('moves_completed', 'children')]
    )
def update_middle_local(reset, moves_completed):
    return get_middle()

@app.callback(
    dash.dependencies.Output('right_list', 'children'),
    [dash.dependencies.Input('game_started', 'children'),
    dash.dependencies.Input('moves_completed', 'children')]
    )
def update_right_local(reset, moves_completed):
    return get_right()

# Resetting towers with local values
@app.callback(
    dash.dependencies.Output('left_tower', 'srcDoc'),
    [dash.dependencies.Input('left_list', 'children')]
    )
def reset_left_tower(left_list):
    # print(left_list, "updating plot")
    return chart(left_list, "Left").to_html()

@app.callback(
    dash.dependencies.Output('middle_tower', 'srcDoc'),
    [dash.dependencies.Input('middle_list', 'children')]
    )
def reset_middle_tower(middle_list):
    # print(middle_list)
    return chart(middle_list, "Middle").to_html()

@app.callback(
    dash.dependencies.Output('right_tower', 'srcDoc'),
    [dash.dependencies.Input('right_list', 'children')]
    )
def reset_right_tower(right_list):
    # print(right_list)
    return chart(right_list, "Right").to_html()

# Updating user moves
@app.callback(
    dash.dependencies.Output('your_moves', 'children'),
    [dash.dependencies.Input('num_moves', 'children')]
    )
def update_user_moves(num_moves):
    return num_moves

# Updating error message
@app.callback(
    dash.dependencies.Output('error_msg', 'children'),
    [dash.dependencies.Input('invalid_flag', 'children')]
    )
def update_error_msg(invalid_flag):
    if invalid_flag == 1:
        return "Invalid move / Try again"
    else:
        return ""

# Updating completion message
@app.callback(
    dash.dependencies.Output('complete_msg', 'children'),
    [dash.dependencies.Input('game_complete', 'children')],
    [dash.dependencies.State('num_moves', 'children')]
    )
def update_complete_msg(game_complete, num_moves):
    if game_complete == 1:
        return "Hurray!! you have completed the game in "+str(num_moves+1)+" moves"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
