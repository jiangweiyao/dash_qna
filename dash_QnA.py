import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from transformers import pipeline
import pandas as pd

nlp = pipeline("question-answering")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('The Huggingface Extractive Question and Answering System '),
    html.Hr(),
    html.Strong('Instructions: Paste the text you would like to search in the "Text Input" box. Next, write the question you would like to ask in the "Question Input" box. Select the top number of answers you would like in the slider bar. Finally, click "Search" to search for the top answers.'),
    html.Hr(),

    html.Div([
        html.Div([
            html.H3('Text Input:'),
            dcc.Textarea(
                id='text-input',
                placeholder='Input your text here',
                value='''David Howell Petraeus AO, MSC (/pɪˈtreɪ.əs/; born November 7, 1952) is a retired United States Army general and public official. He served as Director of the Central Intelligence Agency from September 6, 2011, until his resignation on November 9, 2012. Prior to his assuming the directorship of the CIA, Petraeus served 37 years in the United States Army. His last assignments in the Army were as commander of the International Security Assistance Force (ISAF) and commander, U.S. Forces – Afghanistan (USFOR-A) from July 4, 2010, to July 18, 2011. His other four-star assignments include serving as the 10th commander, U.S. Central Command (USCENTCOM) from October 13, 2008, to June 30, 2010, and as commanding general, Multi-National Force – Iraq (MNF-I) from February 10, 2007, to September 16, 2008. As commander of MNF-I, Petraeus oversaw all coalition forces in Iraq.

Petraeus has a B.S. degree from the United States Military Academy, from which he graduated in 1974 as a distinguished cadet (top 5% of his class). In his class were three other future four-star generals, Martin Dempsey, Walter L. Sharp and Keith B. Alexander. He was the General George C. Marshall Award winner as the top graduate of the U.S. Army Command and General Staff College class of 1983. He subsequently earned an M.P.A. in 1985 and a Ph.D. degree in international relations in 1987 from the Woodrow Wilson School of Public and International Affairs at Princeton University. He later served as assistant professor of international relations at the United States Military Academy and also completed a fellowship at Georgetown University.

Petraeus has repeatedly stated that he has no plans to run for elected political office. On June 23, 2010, President Barack Obama nominated Petraeus to succeed General Stanley McChrystal as commanding general of the International Security Assistance Force in Afghanistan, technically a step down from his position as Commander of United States Central Command, which oversees the military efforts in Afghanistan, Pakistan, Central Asia, the Arabian Peninsula, and Egypt.

On June 30, 2011, Petraeus was unanimously confirmed as the Director of the CIA by the U.S. Senate 94–0. Petraeus relinquished command of U.S. and NATO forces in Afghanistan on July 18, 2011, and retired from the U.S. Army on August 31, 2011. On November 9, 2012, he resigned from his position as director of the CIA, citing his extramarital affair with his biographer Paula Broadwell, which was reportedly discovered in the course of an FBI investigation. In January 2015, officials reported the FBI and Justice Department prosecutors had recommended bringing felony charges against Petraeus for allegedly providing classified information to Broadwell while serving as director of the CIA. Eventually, Petraeus pleaded guilty to one misdemeanor charge of mishandling classified information. ''',
                rows=10,
                style={'width': '50%'}
                ),
            html.Br()
        ], className="six columns"),

        html.Hr(),   

        html.Div([
            html.H3('Question Input:'),
            dcc.Textarea(
                id='question-input',
                placeholder='Input your question here',
                value='Was Petraeus confirmed by the Senate?',
                rows=2,
                style={'width': '50%'}
                ),  
        
            html.Br(),
            html.H3('Number of Top Answers (Ranked):'),
            dcc.Slider(
                id='topn',
                min=1,
                max=10,
                marks={i: '{}'.format(i) for i in range(1, 11)},
                step=1,
                value=3
            ),
            html.Br(),
            html.Button('Search', id='button'),
            html.H3(id='button-1'),
            html.Br(), 

        ], className="six columns"),

        html.Hr(),

        html.Div([
            html.H2('Top Answers:'),
            html.Div(id='output')
        ], className="six columns")


    ], className="row")
])

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


@app.callback(
        Output('output', 'children'),
        [Input('button', 'n_clicks')],
        [State('question-input', 'value'),
            State('text-input', 'value'),
            State('topn', 'value')])
def compute(n_clicks, question, text, topn):
    print(f"The question is: {question}. \n You want the top {topn} answers.")

    df = pd.DataFrame(nlp(question=question, context=text, topk = topn, handle_impossible_answer=False))

    return generate_table(df)
    #return(f"The question is: {question}. \n You want the top {topn} answers.")

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server()
