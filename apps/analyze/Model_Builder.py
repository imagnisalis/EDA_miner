"""
    This module will be used to graphically create models.
    RapidMiner, Weka, Orange, etc, ain't got sh!t on us :)

    You should probably not write code here.
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate

import dash_cytoscape as cyto
import dash_bootstrap_components as dbc

from server import app
from utils import r, create_dropdown
from styles import cyto_stylesheet
from apps.analyze.models import pipeline_creator
from apps.analyze.models.graph_structures import Graph, GraphUtils, orders
from apps.analyze.models.graph_structures import node_options, ml_options

import dill


# TODO: Add divider for categories with huge lists
items = [
    [dbc.DropdownMenuItem(model["label"], id=f"add_{model['node_type']}",
                          n_clicks_timestamp=0)
     for model in ml_options
     if model["parent"] == category]
    for category in orders
]

# Layout definition for the initial setup
default_steps = [
    (0, "input_file", "Input data"),
    (1, "data_cleaner", "Data cleaning"),
    (2, "stdsc", "Standardization"),
    (3, "pca", "Principal Components Analysis"),
    (4, "linr", "Linear Regression"),
]

initial_graph = GraphUtils(default_steps).render_graph()


Model_Builder_Layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-graph',
        layout={'name': "preset"},
        style={"width": "98%", "height": "600px"},
        elements=initial_graph,
        stylesheet=cyto_stylesheet,
    ),


    dbc.Modal([
        dbc.ModalHeader("Pipelines exported:"),
        dbc.ModalBody("No pipeline exported.", id="model_specs"),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ml-auto")
        ),
    ], id="modal"),

])


SideBar_modelBuilder = [

    # Convert model
    html.Div([
        html.Button("Convert to model",
                    id="convert"),
    ], id="export_pipe_submenu"),

    # Remove nodes
    html.Div([
        html.Button("Remove a node", id="remove_node",
                    n_clicks_timestamp=0, ),
        dcc.Dropdown(options=[{"value": elem["data"]["id"],
                               "label": elem["data"]["label"]}
                              for elem in initial_graph[:-4]
                              if "parent" in elem["data"]],
                     id="delete_options"),
    ], id="remove_node_submenu"),

    # Connect selected nodes
    html.Div([
        html.Button("Connect selected nodes",
                    n_clicks_timestamp=0,
                    id="connect_selected_nodes"),
    ], id="connect_nodes_submenu"),


    # Add nodes (collapsible)
    html.Div([
        html.Button([
            html.Span('Add node'),
            html.I("", className="fa fa-caret-down"),
        ], id='button_collapse_add_node', n_clicks=0),
        # Stuff inside the collapsible
        html.Div(id='sidebar_collapsible_button_add_node', children=[
            dbc.DropdownMenu(
                label=f"Category: {category}", children=item,
                className="mb-3"
            ) for (category, item) in zip(orders, items)
        ]),
    ], id="add_nodes_submenu"),


    # Modify nodes (collapsible)
    html.Div([
        html.Button([
            html.Span('Node options'),
            html.I("", className="fa fa-caret-down"),
        ], id='button_collapse_modify_node', n_clicks=0),
        # Stuff inside the collapsible
        html.Div(id='sidebar_collapsible_button_modify_node', children=[
            html.Div(id="inspector", children=[
                html.Div([
                    *create_dropdown("Options", [
                        {"label": "No node selected", "value": "none"}
                    ], id="modify_option_dropdown"),
                    dcc.RadioItems(options=[
                        {"label": "No node selected", "value": "none"}
                    ], id="modify_node_params",
                       labelStyle={
                           'display': 'inline-block',
                           'margin': '5px'
                       }
                    )
                ])
            ]),


            html.Button("Update node", id="modify_node", n_clicks=0,
                        n_clicks_timestamp=0),
            dbc.Modal([
                dbc.ModalHeader("Model update:"),
                dbc.ModalBody("Model parameters were successfully updated."),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close2", className="ml-auto")
                ),
            ], id="modal2"),

        ]),
    ], id="modify_nodes_submenu"),


]


# TODO: These two callbacks can probably be condensed in a loop or combined
# When the sidebar button is clicked, collapse the div
@app.callback(Output('sidebar_collapsible_button_add_node', 'style'),
              [Input('button_collapse_add_node', 'n_clicks')],)
def button_toggle(n_clicks):
    if n_clicks is not None and n_clicks % 2 == 1:
        # Start with the menu open
        return {'display': 'none'}
    else:
        return {'display': 'block'}

# Same as above
@app.callback(Output('sidebar_collapsible_button_modify_node', 'style'),
              [Input('button_collapse_modify_node', 'n_clicks')])
def button_toggle(n_clicks):
    if n_clicks is not None and n_clicks % 2 == 1:
        # Start with the menu open
        return {'display': 'none'}
    else:
        return {'display': 'block'}


@app.callback(Output("cytoscape-graph", "elements"),
              [Input("remove_node", "n_clicks_timestamp"),
               Input("connect_selected_nodes", "n_clicks_timestamp"),
               Input("modify_node", "n_clicks_timestamp")]+[
                  Input(f"add_{node_options[model]['node_type']}",
                        "n_clicks_timestamp")
                  for model in node_options
              ],
              [State("cytoscape-graph", "elements"),
               State("delete_options", "value"),
               State("cytoscape-graph", "selectedNodeData"),
               State("modify_option_dropdown", "value"),
               State("modify_node_params", "value"),
               State("cytoscape-graph", "tapNodeData")])
def modify_graph(remove_clicked_time, connect_selected_time,
                 modify_node_time, *add_nodes):

    # This is necessary since Python cannot accept *args in the middle
    # of the function parameter list. The tapped node is used only for
    # altering parameters on the last-clicked node, while the selected
    # is used for connecting nodes. The modify_node_attribute refers to
    # the dropdown (sklearn kwarg) and modify_node_params is the value
    (elems, to_be_deleted, selected, modify_node_attribute,
            modify_node_params, tapped) = add_nodes[-6:]

    add_nodes = add_nodes[:-6]

    if all(x is None for x in [remove_clicked_time, connect_selected_time,
                               modify_node_time, *add_nodes]):
        if elems is not None:
            return elems
        else:
            return []

    G = Graph(elems)

    # Create list of tuples, e.g.: (time_clicked, add_xgb)
    add_node_list = [(add_node, f"add_{model}")
                     for (add_node, model) in zip(add_nodes, node_options)]

    # Sort buttons based on clicked time (most recent first)
    buttons_and_clicks = sorted([
        (remove_clicked_time, "remove"),
        (connect_selected_time, "connect"),
        (modify_node_time, "modify")
    ] + add_node_list, reverse=True)

    # Graph operations
    if buttons_and_clicks[0][1] == "remove":
        G.node_collection.remove_node(to_be_deleted)

    elif buttons_and_clicks[0][1] == "connect":
        G.edge_collection.add_edges(selected)

    elif buttons_and_clicks[0][1].startswith("add_"):
        # e.g.: (time_clicked, add_xgb) --> xgb
        G.node_collection.add_node(buttons_and_clicks[0][1][4:])

    elif buttons_and_clicks[0][1] == "modify":
        if tapped is not None:
            for node in G.node_collection.nodes:
                # iterate over all the nodes to find the appropriate one
                # TODO: The fact that is is necessary means that `Graph`
                #       should implement a __get__ method (or w/e it is)
                if node.id == tapped["id"]:
                    node.options["data"]["func_params"].update({modify_node_attribute: modify_node_params})

    return G.render_graph()


@app.callback(Output("inspector", "children"),
              [Input("cytoscape-graph", "tapNodeData")],
              [State("user_id", "children")])
def inspect_node(selected, user_id):

    if selected is None or "parent" not in selected:
        # No need to show info for parent nodes as
        # they are there just for show
        raise PreventUpdate()

    if len(selected):
        func = node_options[selected["node_type"]]["func"]
        arguments = list(func.modifiable_params.keys())

    return [
        html.Div([
            *create_dropdown("Options", [
                {"label": arg, "value": arg}
                for arg in arguments
            ], id="modify_option_dropdown"),
            dcc.RadioItems(options=[
                {"label": "No node selected", "value": "none"}
            ], id="modify_node_params",
               labelStyle={
                   'display': 'inline-block',
                   'margin': '5px'
               })
        ]),
    ]


@app.callback(
    Output("modal2", "is_open"),
    [Input("modify_node", "n_clicks"),
     Input("close2", "n_clicks")],
    [State("modal2", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


def stringify(val):
    # Since some values are either bool or none
    # we need to explicitly convert them
    if val is None:
        return "None"
    elif val is True:
        return "True"
    elif val is False:
        return "False"
    else:
        return str(val)

@app.callback(Output("modify_node_params", "options"),
              [Input("modify_option_dropdown", "value")],
              [State("cytoscape-graph", "tapNodeData")])
def update_radio_buttons_modify_params(value, selected):

    if selected is None or value is None:
        return [
            {"label": "No node selected", "value": "none"}
        ]

    if len(selected):
        func = node_options[selected["node_type"]]["func"]

    return [
        {"label": stringify(val), "value": val}
        for val in func.modifiable_params[value]
    ]


@app.callback(Output("delete_options", "options"),
              [Input("cytoscape-graph", "elements")],
              [State("user_id", "children")])
def inspect_node(elements, user_id):
    return [{
        "value": elem["data"]["id"],
        "label": elem["data"]["label"]
        } for elem in elements if (elem["data"].get("source") is None) and
                                  ("parent" in elem["data"])]


@app.callback([Output("modal", "is_open"),
               Output("model_specs", "children")],
              [Input("convert", "n_clicks"),
               Input("close", "n_clicks")],
              [State("cytoscape-graph", "elements"),
               State("cytoscape-graph", "stylesheet"),
               State("user_id", "children"),
               State("modal", "is_open")])
def convert_model(n_clicks, close, elements, layout, user_id, is_open):

    if user_id.startswith("python_generated_ssid"):
        # Trim id
        user_id = user_id.split("-")[-1]

    if n_clicks is None:
        return [False, [html.H5("No specs defined yet")]]

    else:
        # Keep elements that are either edges (have a source)
        # or elements that have a parent (nodes, not groups)
        elements = [elem for elem in elements if (("source" in elem["data"]) or
                                                  ("parent" in elem["data"]))]

        pipelines, classifiers = pipeline_creator.create_pipelines(elements,
                                                                   node_options)

        # Save pipelines to Redis (to be used in other modules)
        for pipe, clf in zip(pipelines, classifiers):
            r.set(f"{user_id}_pipeline_{clf}", dill.dumps(pipe))

        # TODO: Make this a modal
        #       https://dash-bootstrap-components.opensource.faculty.ai/l/components/modal
        return [not is_open, [html.P(f"{i+1}) {str(pipeline)}")
                for (i, pipeline) in enumerate(pipelines)]]
