"""
This module defines the interface for fitting simple regression models.

Global Variables:
    - Regression_Options: Generate the layout of the dashboard.

Dash callbacks:
    - render_variable_choices_regression: Create a menu of dcc components \
                                          for the user to choose fitting \
                                          options.
    - fit_regression_model: Take user choices and, if all are present, fit \
                            the appropriate model.

Notes to others:
    Feel free to experiment as much as you like here, although you probably \
    want to write code elsewhere.
"""

from dash.dependencies import Input, Output, State
import dash_html_components as html
from dash.exceptions import PreventUpdate

from server import app
from utils import create_dropdown, mapping, get_data
from apps.analyze.utils import render_variable_choices



def Regression_Options(options):
    """
    Generate the layout of the dashboard.

    Args:
        options (list(dict)): Available datasets as options for `dcc.Dropdown`.

    Returns:
        A Dash element or list of elements.
    """

    return html.Div(children=[
        # Choose a dataset
        html.Div(create_dropdown("Available datasets", options,
                                 multi=False, id="dataset_choice_regression"),
                 className="horizontal_dropdowns"),

        # Choose an algorithm
        html.Div(create_dropdown("Choose algorithm type", options=[
            {'label': 'Linear Regression', 'value': 'linr'},
            {'label': 'SVM Regression', 'value': 'svr'},
            {'label': 'Decision Tree Regression', 'value': 'dtr'}
        ], multi=False, id="algo_choice_regression"),
         className="horizontal_dropdowns"),

        ## Two empty divs to be filled by callbacks
        # Available choices for fitting
        html.Div(id="variable_choices_regression"),

        # The results
        html.Div(id="training_results_regression"),
    ])


# Render dropdowns and other choices
render_variable_choices("regression")



@app.callback(
    Output("training_results_regression", "children"),
    [Input("xvars_regression", "value"),
     Input("yvars_regression", "value")],
    [State('algo_choice_regression', "value"),
     State("user_id", "children"),
     State("dataset_choice_regression", "value")])
def fit_regression_model(xvars, yvars, algo_choice_regression,
                         user_id, dataset_choice):
    """
    Take user choices and, if all are present, fit the appropriate model.

    Args:
        xvars (list(str)): predictor variables.
        yvars (str): target variable.
        algo_choice_regression (str): The choice of algorithm type.
        user_id: Session/user id.
        dataset_choice: Name of dataset.

    Returns:
        list: Dash element(s) with the results of model fitting.
    """


    df = get_data(dataset_choice, user_id)

    ## Make sure all variables have a value before fitting
    if any(x is None for x in [xvars, yvars, df, dataset_choice,
                               algo_choice_regression]):
        raise PreventUpdate()

    # We have the dictionary that maps keys to models so use that
    model = mapping[algo_choice_regression]()

    model.fit(df[xvars], df[yvars])

    # TODO: Add visualizations for the results.

    return [
        html.H4(f"Regression model scored: {model.score(df[xvars], df[yvars])}")
    ]
