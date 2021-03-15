import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import requests
import io


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dbc.Jumbotron([
            html.Div([
                html.H1("Image Classifier", className="jumbotron-heading justify-content-center"),
            ], className="text-center")
    ], className="mt-4"),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select File (JPG)')
                    ]),
                    style={
                        'width': '100%',
                        'height': '100px',
                        'lineHeight': '100px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'font-size': '17px'
                        # 'margin': '10px'
                    },
                    # Allow multiple files to be uploaded
                    multiple=False
                ),
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='output-data-upload', className="d-flex justify-content-center mt-4")
        ]),
        dbc.Col([
            html.Div(id='output-data-result', className="d-flex justify-content-center mt-4")
        ])
    ])
], className="container")


@app.callback(Output('output-data-upload', 'children'),
              Output('output-data-result', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    print("In: update output", flush=True)
    # for content in list_of_contents:
    # print(list_of_contents)
    image_html = []
    url = 'https://torch-serve-stackn-demo-cyb-60d7.studio-dev.local.stackn.dev/predictions/vgg11_scripted'
    pred_res = ""
    try:
        content_type, content_string = list_of_contents.split(',')
        print(content_type)
        contentb64_decode = base64.b64decode(content_string)
        file_obj = io.BytesIO(contentb64_decode)
        try:
            res = requests.put(url, data=file_obj)
        except Exception as e:
            print(e)
        print(res.text)

        image_html = html.Img(src='data:image/png;base64,{}'.format(content_string), width="90%")
        pred_res = html.Pre([res.text], style={'font-size': '20px'})
    except Exception as err:
        print("No image.")
        print(err)

    return image_html, pred_res


if __name__ == '__main__':
    app.run_server(debug=True)