"""
This module collects the layouts for connecting to the various APIs.

Functions:
    - success_message: Notify the user for successful connection.

Global variables:
    - debugger_layout: All inputs and the button used throughout the tab.
    - twitter_layout: 4 input fields and a button.
    - gsheets_layout: 2 input fields and a button. The rest are hidden.
    - reddit_layout: 2 input fields and a button. The rest are hidden.
    - quandl_layout: 2 input fields and a button. The rest are hidden.
    - spotify_layout: 2 input fields and a button. The rest are hidden.

Notes to others:
    You should probably not write code here, unless adding
    a new API connection.
"""

import dash_core_components as dcc
import dash_html_components as html


# These are all elements that are needed as callback inputs
# but if they disappear from one view then the callback stops
# working so they are inserted as hidden in every layout
debugger_layout = [
    dcc.Input(id="input1", type="text", value="", style={"display": "none"}),
    dcc.Input(id="input2", type="text", value="", style={"display": "none"}),
    dcc.Input(id="input3", type="text", value="", style={"display": "none"}),
    dcc.Input(id="input4", type="text", value="", style={"display": "none"}),
    html.Button("Connect!", id="connect_button", style={"display": "none"}),
]


def success_message(api):
    return [
        html.H4(f"Successfully got data from the {api} API."),
        html.Br(),
        *debugger_layout,
    ]


twitter_layout = [
    html.H5("Key"),
    dcc.Input(id="input1", type="text"),
    html.H5("Secret Key"),
    dcc.Input(id="input2", type="text"),
    html.H5("Access Token"),
    dcc.Input(id="input3", type="text"),
    html.H5("Access Token Secret"),
    dcc.Input(id="input4", type="text"),

    html.Button("Connect!", id="connect_button",
                style={"display": "inline"})
]

gsheets_layout = [
    html.H5("Credentials file path"),
    dcc.Input(id="input1", type="text"),
    html.H5("Secret Key"),
    dcc.Input(id="input2", type="text"),

    # debuggers
    dcc.Input(id="input3", type="text", style={"display": "none"}),
    dcc.Input(id="input4", type="text", style={"display": "none"}),

    html.Button("Connect!", id="connect_button",
                style={"display": "inline"})
]

reddit_layout = [
    html.H5("Client id"),
    dcc.Input(id="input1", type="text"),
    html.H5("Client secret"),
    dcc.Input(id="input2", type="text"),

    # debuggers
    dcc.Input(id="input3", type="text", style={"display": "none"}),
    dcc.Input(id="input4", type="text", style={"display": "none"}),

    html.Button("Connect!", id="connect_button",
                style={"display": "inline"})
]

quandl_layout = [
    html.H5("Quandl key"),
    dcc.Input(id="input1", type="text"),
    html.H5("Quandl tag"),
    dcc.Input(id="input2", type="text"),

    # debuggers
    dcc.Input(id="input3", type="text", style={"display": "none"}),
    dcc.Input(id="input4", type="text", style={"display": "none"}),

    html.Button("Connect!", id="connect_button",
                style={"display": "inline"})
]

spotify_layout = [
    html.H5("Client id"),
    dcc.Input(id="input1", type="text"),
    html.H5("Client secret"),
    dcc.Input(id="input2", type="text"),

    # debuggers
    dcc.Input(id="input3", type="text", style={"display": "none"}),
    dcc.Input(id="input4", type="text", style={"display": "none"}),

    html.Button("Connect!", id="connect_button",
                style={"display": "inline"}),
]
