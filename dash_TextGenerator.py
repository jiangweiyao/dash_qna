import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from transformers import pipeline

text_generator = pipeline("text-generation")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('The Huggingface Text Generator'),
    html.Hr(),
    html.Strong('Instructions: Get the text generator start by typing a few sentences on what you want it to generate. Next, select the length you would like in the slider bar. Finally, click "Generate" to summarize the text.'),
    html.Hr(),

    html.Div([
        html.Div([
            html.H3('Text Input:'),
            dcc.Textarea(
                id='text-input',
                placeholder='Input your text here',
                value="""Blood for the blood god and skulls for the skull throne. Today, we march into battle for Khorne!
""",
                rows=2,
                style={'width': '50%'}
                ),
            html.Br()
        ], className="six columns"),

        html.Hr(),   

        html.Div([
        html.H3("Generate Length of Text:"),
        dcc.Slider(
            id='srange',
            marks={i: '{}'.format(i) for i in range(30, 201,10)},
            min=30,
            max=200,
            value=50
        ),
            html.Br(),
            html.Button('Summarize', id='button'),
            html.H3(id='button-1'),
            html.Br(), 

        ], className="six columns"),

        html.Hr(),

        html.Div([
            html.H2('Generated Text:'),
            html.H5(id='output')
        ], className="six columns")


    ], className="row")
])


@app.callback(
        Output('output', 'children'),
        [Input('button', 'n_clicks')],
        [State('text-input', 'value'),
            State('srange', 'value')])
def compute(n_clicks, text, srange):
    #print(f"Your range is {srange[0]} to {srange[1]}")
    text = text_generator(text, max_length=srange, do_sample=True)
    print(text[0].get('generated_text'))
    return(text[0].get('generated_text'))


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()
