import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

from transformers import pipeline

summarizer = pipeline("summarization")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('The Huggingface Summarizer'),
    html.Hr(),
    html.Strong('Instructions: Paste the text you would like to summarize in the "Text Input" box. Next, select the minimum and maximum summary length you would like in the slider bar. Finally, click "Summarize" to summarize the text.'),
    html.Hr(),

    html.Div([
        html.Div([
            html.H3('Text Input:'),
            dcc.Textarea(
                id='text-input',
                placeholder='Input your text here',
                value=""" New York (CNN)When Liana Barrientos was 23 years old, she got married in Westchester County, New York.
A year later, she got married again in Westchester County, but to a different man and without divorcing her first husband.
Only 18 days after that marriage, she got hitched yet again. Then, Barrientos declared "I do" five more times, sometimes only within two weeks of each other.
In 2010, she married once more, this time in the Bronx. In an application for a marriage license, she stated it was her "first and only" marriage.
Barrientos, now 39, is facing two criminal counts of "offering a false instrument for filing in the first degree," referring to her false statements on the
2010 marriage license application, according to court documents.
Prosecutors said the marriages were part of an immigration scam.
On Friday, she pleaded not guilty at State Supreme Court in the Bronx, according to her attorney, Christopher Wright, who declined to comment further.
After leaving court, Barrientos was arrested and charged with theft of service and criminal trespass for allegedly sneaking into the New York subway through an emergency exit, said Detective
Annette Markowski, a police spokeswoman. In total, Barrientos has been married 10 times, with nine of her marriages occurring between 1999 and 2002.
All occurred either in Westchester County, Long Island, New Jersey or the Bronx. She is believed to still be married to four men, and at one time, she was married to eight men at once, prosecutors say.
Prosecutors said the immigration scam involved some of her husbands, who filed for permanent residence status shortly after the marriages.
Any divorces happened only after such filings were approved. It was unclear whether any of the men will be prosecuted.
The case was referred to the Bronx District Attorney\'s Office by Immigration and Customs Enforcement and the Department of Homeland Security\'s
Investigation Division. Seven of the men are from so-called "red-flagged" countries, including Egypt, Turkey, Georgia, Pakistan and Mali.
Her eighth husband, Rashid Rajput, was deported in 2006 to his native Pakistan after an investigation by the Joint Terrorism Task Force.
If convicted, Barrientos faces up to four years in prison.  Her next court appearance is scheduled for May 18.
""",
                rows=10,
                style={'width': '50%'}
                ),
            html.Br()
        ], className="six columns"),

        html.Hr(),   

        html.Div([
        html.H3("Minimum and Maximum Summary Character Length:"),
        dcc.RangeSlider(
            id='srange',
            marks={i: '{}'.format(i) for i in range(30, 201,10)},
            min=30,
            max=200,
            value=[30, 130]
        ),
            html.Br(),
            html.Button('Summarize', id='button'),
            html.H3(id='button-1'),
            html.Br(), 

        ], className="six columns"),

        html.Hr(),

        html.Div([
            html.H2('Summary:'),
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
    summary = summarizer(text, max_length=srange[1], min_length=srange[0])
    print(summary[0].get('summary_text'))
    return(summary[0].get('summary_text'))


if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()
