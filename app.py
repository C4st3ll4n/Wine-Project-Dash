
# Data Libraries
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

# Visualization Libraries
#import plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
from plotly.offline import iplot

import dash
import dash_table
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import os 

from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA, TruncatedSVD
from nltk.corpus import stopwords
stop_words = set(stopwords.words("english"))

import cross_filt
from cross_filt import *
def dataset():
    data_path = 'data/wine_data_new.csv'
    ## Importing the dataset
    data = pd.read_csv(data_path, index_col=0)

    return data

df_train = dataset()

scatt = pd.read_csv("data/matrix_wines.csv", index_col=0)

scatt['harvest'] = scatt['harvest'].astype(str)
scatt['rating_cat'] = scatt['rating_cat'].astype(str)
#scatt['clusters'] = scatt['clusters'].astype(str)
df_train['rating_cat'] = df_train['rating_cat'].astype(str)

target_path = "assets/profiling1.html"


if os.path.exists(target_path): 
    pass
else: 
    profile = ProfileReport(df_train, title='Pandas Profiling Report')
    #profile = df_train.parallel_apply(profiling) #html={'style':{'full_width':True}}
    profile.to_file(output_file="assets/profiling1.html")

## CSS EXTERNAL FILE
external_stylesheets = ['https://codepen.io/kaburelabs/pen/xxGRXWa.css', 
                        'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']

## App Name
app_name='Dashboard'

## Defining the instance of dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = app_name

# server instance to run map when deploying
server = app.server

# Since I am adding callbacks to elements that don’t ~
# exist in the app.layout as they are spread throughout files
app.config.suppress_callback_exceptions = True


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import sklearn 

from wordcloud import WordCloud, STOPWORDS

stopwords = set(STOPWORDS)

newStopWords = ['fruit', "Drink", "black", 'wine', 'drink']


def create_header(some_string):
    header_style = {
        'background-color':'rgb(79, 152, 202)',
        'padding': '1.5rem',
        'display':'inline-block',
        'width':'100%'
        
       # 'border-style': 'dotted'
    }
    logo_trich = html.Img(
                    src='/assets/fundo_transp-b.png',
                    className='three columns',
                    style={
                        'height': 'auto',
                        'width': '140px', # 'padding': 1
                        'float': 'right', #'position': 'relative'
                        'margin-right': '66px', #'border-style': 'dotted'
                        'display':'inline-block'})

    title = html.H1(children=some_string, className='eight columns',
                    style={'margin':'0 0 0 36px',
                           'color':'#ffffff', 'font-size':'35px'})

    header = html.Header(html.Div([title, logo_trich]), style=header_style)

    return header


def create_footer():
    p = html.P(
        children=[
            html.Span('Developed By: '),
            html.A('trich.ai | Data Intelligence Solutions', 
                   style={'text-decoration':'none', 'color':'#ffffff'},
                   href='https://trich.ai', target='_blank')
        ], style={'float':'right', 'margin-top':'8px', 
                  'font-size':'18px', 'color':'#ffffff' }
    )

    span_style = {'horizontal-align': 'right', 
                  'padding-left': '1rem', 
                  'font-size':'15px', 
                  'vertical-align':'middle'}

    kaggle = html.A(
        children=[
            html.I([], className='fab fa-kaggle'),
            html.Span('Kaggle', style=span_style)
        ], style={'text-decoration': 'none', 'color':'#ffffff', 'margin-right':'20px'},
        href="https://www.kaggle.com/kabure/kernels",
        target='_blank')

    mapbox = html.A(
        children=[
            html.I([], className='fab fa-python'),
            html.Span('Dash Plotly', style=span_style)
        ], style={'text-decoration': 'none', 'color':'#ffffff', 'margin-right':'20px'},
        href='https://plot.ly/dash/', target='_blank')

    font_awesome = html.A(
        children=[
            html.I([], className='fa fa-font-awesome'),
            html.Span('Font Awesome', style=span_style)
        ], style={'text-decoration': 'none', 'color':'#ffffff', 'margin-right':'20px'},
        href='http://fontawesome.io/', target='_blank')

    datatables = html.A(
        children=[
            html.I([], className='fa fa-github'),
            html.Span('trich.ai\n Github', style=span_style)
        ], style={'text-decoration': 'none', 'color':'#ffffff', 'margin-right':'20px'},
        href='https://github.com/kaburelabs/', target='_blank')

    ul1 = html.Div(
        children=[
            html.Li(mapbox, style={'display':'inline-block', 'color':'#ffffff'}),
            html.Li(font_awesome, style={'display':'inline-block', 'color':'#ffffff'}),
            html.Li(datatables, style={'display':'inline-block', 'color':'#ffffff'}),
            html.Li(kaggle, style={'display':'inline-block', 'color':'#ffffff'}),
        ],
        style={'list-style-type': 'none', 'font-size':'30px'},
    )

    hashtags = 'plotly,dash,trich.ai'
    tweet = 'trich.ai Customers Churn Dashboard, a cool dashboard with Plotly Dash!'
    twitter_href = 'https://twitter.com/intent/tweet?hashtags={}&text={}'\
        .format(hashtags, tweet)
    twitter = html.A(
        children=html.I(children=[], className='fa fa-twitter'),
        title='Tweet me!', href=twitter_href, target='_blank')

    github = html.A(
        children=html.I(children=[], className='fa fa-github', style={'color':'black'}),
        title='Repo on GitHub',
        href='https://github.com/kaburelabs/Dash-app-Churn-Customer', target='_blank')

    li_right_first = {'line-style-type': 'none', 'display': 'inline-block'}
    li_right_others = {k: v for k, v in li_right_first.items()}
    li_right_others.update({'margin-left': '10px'})
    ul2 = html.Ul(
        children=[
            html.Li(twitter, style=li_right_first),
            html.Li(github, style=li_right_others),
        ],
        style={
            'position': 'fixed',
            'right': '1.5rem',
            'bottom': '75px',
            'font-size':'60px'
        }
    )
    div = html.Div([p, ul1, ul2])

    footer_style = {
        'font-size': '2.2rem',
        'background-color': 'rgb(79, 152, 202)',
        #'padding': '2.5rem',
        'margin-top': '3rem', 
        'display':'inline-block', 'padding':'16px 32px 8px'
    }
    footer = html.Footer(div, style=footer_style, className='twelve columns')
    return footer


app.layout = html.Div([
    create_header('Dashboard'),
    html.Div([
        dcc.Tabs(id="tabs-example",
                children=[
                        dcc.Tab(label='Data & Details', value='tab-1'),
                        dcc.Tab(label='Dataset Profilling', value='tab-2'),
                        dcc.Tab(label='Graphs & EDA', value='tab-3'),
                        dcc.Tab(label='Recommender System', value='tab-4'),
                        dcc.Tab(label='Model Explanability', value='tab-5')
                ], 
                value='tab-1'),
        html.Div(id='tabs-content-example')
    ], className='container'),
    create_footer()
], style={'margin':'0 auto'})

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
                    html.Div([
                        dcc.Upload([
                            'Drag and Drop or ',
                            html.A('Select a File')
                        ], style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center'
                    })
            ], className='row', style={'height':'70vh'}) 
    ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Data Profiling: '),
            html.Iframe(
                id='graph-1-tabs',
                src=app.get_asset_url('profiling1.html'),
                #src=app.get_asset_url('trich-dash.jpg'),
                #className='ten columns offset-by-one',
                style={ 'margin': '0 auto',
                        'width': '100%',
                        'height': '600px'}
                )            
        ], className='row', style={'height':'70vh'})

    elif tab == 'tab-3':
        return layout2

    elif tab == 'tab-4':
            return html.Div([html.Div([
                dcc.Dropdown(
                            id='dropdown-tab4',
                            options=[{'label': i, 'value': i} for i in df_train['country'].fillna('null').unique()],
                            value='US'),
                html.Div([
                        dcc.Graph(
                            id='graph-4-tabs', style={'margin':'0 auto'}, className='six columns'
                        ),
                        generate_html_table()
                ], )
            ], style={'margin':'0 auto'})])



operators = [['ge ', '>='], ['le ', '<='], ['lt ', '<'],
             ['gt ', '>'], ['ne ', '!='], ['eq ', '='],
             ['contains '], ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part
                # word operators need spaces after them in the filter string,
                                # but we don't want these later
                        return name, operator_type[0].strip(), value
    return [None] * 3


@app.callback(Output('table-sorting-filtering', 'data'),
[Input('table-sorting-filtering', "page_current"),
Input('table-sorting-filtering', "page_size"),
Input('table-sorting-filtering', 'sort_by'),
Input('table-sorting-filtering', 'filter_query')])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df_train.copy()
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                    dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
                    dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                    dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        if len(sort_by):
                dff = dff.sort_values(
                    [col['column_id'] for col in sort_by],
                    ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                    ],
                    inplace=False
            )
    page = page_current
    size = page_size

    return dff.iloc[page * size: (page + 1) * size].to_dict('records')

kmeans_elbow = pd.read_csv('data/elbow_method.csv')

@app.callback(Output('graph-4-tabs', 'figure'),
             [Input('dropdown-tab4', "value")])
def tf_idf_words(country_var):
    vectorizer = TfidfVectorizer(ngram_range = (1, 3), min_df=1, 
                                 stop_words='english', max_features=20,
                                 max_df=.5)

    print('valor dropwdown', country_var)

    X2 = vectorizer.fit_transform(df_train[(df_train.country == 'Portugal')]['description_desc']) 
   
    features = (vectorizer.get_feature_names()) 
    scores = (X2.toarray()) 
    
    # Getting top ranking features 
    sums = X2.sum(axis = 0) 
    data1 = [] 
    
    for col, term in enumerate(features): 
        data1.append( (term, sums[0,col] )) 

    ranking = pd.DataFrame(data1, columns = ['term','rank']) 
    words = (ranking.sort_values('rank', ascending = False))[:15]
    
    fig = px.line(kmeans_elbow, x='K_number', y='Distorcions')

    return fig


def generate_html_table(max_rows=10, n_clusters=4):
 
    df = pd.read_csv(f"data/clusters/clusters{n_clusters}.csv", index_col=0)

    return html.Div(
        [
            html.Div(
                html.Table(
                    # Header
                    [html.Tr([html.Th()])]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(
                                    dash_table.DataTable(
                                        columns=[{"name": i, "id": i} for i in df.columns],
                                        data=df.to_dict('rows')
                                    )
                                        
                                    )
                                
                            ]
                        )
                        #for i in range(min(len(df), max_rows))
                    ]
                ),
                style={"height": "300px", "overflowY": "scroll"},
            ),
        ],
        style={"height": "100%"}, className='six columns')


def _scatter_view(data, x_val, y_val, log):
    
    fig = px.scatter(data, x='price', y='points', 
                     title=f"Distribution of Wine Price and Ratings",
                     color=x_val, hover_name='variety', opacity=.4,
                     hover_data=['country'], height=600, 
                     log_x=log)

    fig.update_layout(showlegend=False, title_x=.5, 
                    #title=f"Distribution of {x_val} <br>by {color}",
                    xaxis_title=f"Price per Bottle (in USD)", 
                    yaxis_title=f"Points Range",
                    #xaxis={'type':'category'},
                    #margin=dict(t=100, l=50)
            )
    return fig

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'), #output the figure
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'), # price
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'), # points
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'), # log or not
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'), # log or not 
     #dash.dependencies.Input('crossfilter-year--slider', 'value') #year
])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type):
                 
    fig = _scatter_view(data=scatt, x_val=xaxis_column_name, 
                        y_val=yaxis_column_name, log=yaxis_type)

    return fig


# def create_time_series(df, country):
#     return tf_idf_words(df, country)

# def create_time_series(df, country):
#     return tf_idf_words(df, country)

def tf_idf_words_t(df, country_var, variety, ngram, province):
    
    if ngram == 1:
        ngran_range=(1,2)
        title=(f"TfIdf Unigram for <br>{country_var}, {province}, {variety}")
    elif ngram == 2:
        ngran_range=(2,2) 
        title=(f"TfIdf Unigram for <br>{country_var}, {province}, {variety}")           
    elif ngram == 3:
        ngran_range=(3,3)
        title=(f"TfIdf Unigram for <br>{country_var}, {province}, {variety}")        

    vectorizer = TfidfVectorizer(ngram_range = ngran_range, min_df=1, 
                                 stop_words='english', max_features=10,
                                 max_df=500)

    #X2 = vectorizer.fit_transform(df_train.loc[(df_train.country == country_var)]['description']) 
    X2 = vectorizer.fit_transform(df['description_desc']) 
     
    features = (vectorizer.get_feature_names()) 
    scores = (X2.toarray()) 
    
    # Getting top ranking features 
    sums = X2.sum(axis = 0) 
    data1 = [] 
    
    for col, term in enumerate(features): 
        data1.append( (term, sums[0,col] )) 

    ranking = pd.DataFrame(data1, columns = ['term','rank']) 
    words = (ranking.sort_values('rank', ascending = False))[:15]
    
    fig = px.bar(words, x='term', y='rank', title=title, height=500)
    fig.update_layout(autosize=False, title_x=.5)
    return fig


@app.callback(
    dash.dependencies.Output('province-selector1', 'options'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')]
)
def update_tf_idf(clickData, xaxis_column_name, axis_type):

    country_name = clickData['points'][0]['customdata']
    hover = clickData['points'][0]['hovertext']

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass

    dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == hover)].copy()
    
    #[{'label': i, 'value': i} for i in fnameDict[name]]
    return [{'label': province, 'value': province} for province in dff['province'].unique()]


@app.callback(
    dash.dependencies.Output('province-selector1', 'value'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')]
)
def update_tf_idf(clickData):

    country_name = clickData['points'][0]['customdata']
    hover = clickData['points'][0]['hovertext']
    print(clickData)
    #print(clickData)
    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass
        
    dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == hover)].copy()
    
    #[{'label': i, 'value': i} for i in fnameDict[name]]
    return dff['province'].value_counts().index[0]


@app.callback(
    dash.dependencies.Output('fig-1', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('province-selector1', 'value')]
)
def update_tf_idf(clickData, xaxis_column_name, axis_type, provinces):

    country_name = clickData['points'][0]['customdata']
    hover = clickData['points'][0]['hovertext']

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass

    if provinces is list:
        isin_val = provinces
    else: 
        isin_val = [provinces]

    df = df_train[(df_train['country'] == country_name) & (df_train['variety'] == hover) & (df_train['province'].isin(isin_val))].copy()

    return tf_idf_words_t(df, country_name, hover, ngram=axis_type, province=provinces)



@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('table',  'page_size'),
     dash.dependencies.Input('table', "page_current"),
     dash.dependencies.Input('table', "filter_query"),
     dash.dependencies.Input('table', "sort_by")])
def update_x_timeseries(clickData, yaxis_column_name, axis_type, page_size, page_current, filter_query, sort_by):

    country_name = clickData['points'][0]['customdata']
    hover = clickData['points'][0]['hovertext']

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass

    dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == hover) ]
    filtering_expressions = filter_query.split(' && ')

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=True
        )
    else:
        # No sort is applied
        pass

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].sort_values('points').to_dict('records')

@app.callback(
    dash.dependencies.Output('fig-2', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('province-selector1', 'value')]
)
def update_tf_idf(clickData, xaxis_column_name, axis_type, province):

    country_name = clickData['points'][0]['customdata']
    hover = clickData['points'][0]['hovertext']

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass
 
    # print(country_name == 'General')
    
    fig = px.scatter(df_train[(df_train['country'] == country_name) & (df_train['variety'] == hover) & (df_train['province'].isin([province]))],
                     x='price', y='points', color='rating_cat', opacity=.5,
                     hover_name='winery',hover_data=['title', 'country'], 
                     log_x=True, height=500, title="Distribution clusters")
    fig.update_layout(showlegend=False)
    return fig

import random

@app.callback(
    dash.dependencies.Output('inf-1', 'children'),
    [dash.dependencies.Input('fig-2', 'hoverData')]
)
def update_tf_idf(clickData):
    # if not clickData:
    #     return dash.no_update

    country_name = clickData['points'][0]['customdata'][1]
    title_name = clickData['points'][0]['customdata'][0]
    #hover = clickData['points'][0]['hovertext']

    print("click selector: ", clickData)
    print('country selector aspects:', country_name)
    print('title selector aspects:', title_name)

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass
    print()
    print('teste df train', df_train[df_train['title'] == title_name])
    print(df_train[(df_train['country'] == country_name)]['title'])
    dff = df_train[(df_train['country'] == country_name) & (df_train['title'] == title_name)]
    print('teste dff', dff)
    var_aspects=dff['aspects'].values
    wineries=dff['winery'].nunique()
    # print('aspects selector', dff)

    return html.Div([
        html.Div([
            html.Div(
                children=[
                    html.H5(style={'textAlign':'center','padding':'.1rem',
                                    'fontSize':'22px'}, className='title',
                                        children=f"Some Informations for the Wine title"),                                     
                    html.H3(id='display-5', style={'textAlign':'center', 'fontSize':'22px', 
                                    'fontWeight':'bold','color':'#4f98ca'},
                                    children=[html.P(style={'padding':'.5rem'},
                                                     children=f"{title_name}")])
                                        ], className='row'),], className='twelve columns'),
           html.Div([
                    html.Div(
                        children=[
                            html.H3(id='display-6', style={'textAlign':'center','fontWeight':'bold','color':'#272727'},
                                    children=[html.P(style={'padding':'.5rem'},
                                                     children=len(var_aspects))]
                                        ),
                            html.H5(style={'textAlign':'center','color':'#272727','padding':'.1rem'},
                                            children="Reviews")                                        
                                    ], className='four columns', style={'display':'inline-block'}),


                        html.Div(
                            children=[
                                html.H3(id='display-7', style={'textAlign':'center',
                                            'fontWeight':'bold','color':'#272727'},
                                        children=[html.P(style={'padding':'.5rem'},
                                                        children=wineries)]),
                                html.H5(style={'textAlign':'center','color':'#272727','padding':'.1rem'},
                                                children="Wineries")                                        
                                        ], className='four columns', style={'display':'inline-block'}),
                        html.Div(
                            children=[
                                html.H3(id='display-8', style={'textAlign':'center',
                                        'fontWeight':'bold','color':'#272727'},
                                        children=[html.P(style={'padding':'.5rem'},
                                                        children=dff['taster_name'].nunique())]),
                                html.H5(style={'textAlign':'center','color':'#272727','padding':'.1rem'},
                                                children="Tasters")                                        
                                        ], className='four columns', style={'display':'inline-block'}),
            ], className='six columns'),
                    html.Div(
                        children=[
                            html.H5(style={'textAlign':'center','color':'#272727','padding':'.1rem', 'fontSize':'18px'},
                                            children="Principal Wine Aspects"),     
                            html.H3(id='display-9', style={'textAlign':'center', 'fontSize':'21px',
                                    'fontWeight':'bold','color':'#272727'},
                                    children=[html.P(style={'padding':'.5rem'},
                                                     children=var_aspects[random.randrange(len(var_aspects))])]),
                                   
                                    ], className='six columns', style={'display':'inline-block'})
                                    
                    ], className='row', style={'backgroundColor':'#effffb', 'padding':'12px 36px'}
                                )
                                #'display':'inline'
                                # ] )
                #                         html.P(style={'padding':'.5rem'},
                #   children=f"{var_aspects[random.randrange(len(var_aspects))]}")

@app.callback(
    dash.dependencies.Output('display-1', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_tf_idf(clickData,):

    if clickData['points'][0]['customdata'] != 'General':
        country_name = clickData['points'][0]['customdata']
        variety_name = clickData['points'][0]['hovertext']
        country_name = ''.join(country_name)
#        dff = df_train[df_train['country'] == country_name]            
        title=f'{country_name}, {variety_name}'

        return html.P(style={'padding':'.5rem'},
                      children=title)
    else:
        dff = df_train
        title="Total reviews (No country specific)"
          
        return html.P(style={'padding':'.5rem'},
                        children=title)



@app.callback(
    dash.dependencies.Output('display-2', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def _update_display(clickData,):

    if clickData['points'][0]['customdata'] != 'General':
        country_name = clickData['points'][0]['customdata']
        variety_name = clickData['points'][0]['hovertext']
        country_name = ''.join(country_name)

        dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == variety_name)]
        title=f'{len(dff)}'
        return html.P(style={'padding':'.5rem'},
                    children=title)
       
    else:
        dff = df_train
        title=f'{len(dff)}'
        return html.P(style={'padding':'.5rem'},
                    children=title)


@app.callback(
    dash.dependencies.Output('display-3', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_tf_idf(clickData,):

    if clickData['points'][0]['customdata'] != 'General':
        country_name = clickData['points'][0]['customdata']
        variety_name = clickData['points'][0]['hovertext']
        country_name = ''.join(country_name)
        dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == variety_name)]
        title=f"{dff['winery'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                children=title)
    else:
        dff = df_train
        title=f"{dff['winery'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                        children=title)


@app.callback(
    dash.dependencies.Output('display-4', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_tf_idf(clickData,):

    if clickData['points'][0]['customdata'] != 'General':
        country_name = clickData['points'][0]['customdata']
        variety_name = clickData['points'][0]['hovertext']
        country_name = ''.join(country_name)
        dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == variety_name)]
        title=f"{dff['title'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                children=title)
    else:
        dff = df_train
        title=f"{dff['title'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                children=title)


@app.callback(
    dash.dependencies.Output('display-10', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_tf_idf(clickData, ):

    if clickData['points'][0]['customdata'] != 'General':
        country_name = clickData['points'][0]['customdata']
        variety_name = clickData['points'][0]['hovertext']
        country_name = ''.join(country_name)
        dff = df_train[(df_train['country'] == country_name) & (df_train['variety'] == variety_name)]
        title=f"{dff['province'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                children=title)
    else:
        dff = df_train
        title=f"{dff['province'].nunique()}"
        return html.P(style={'padding':'.5rem'},
                children=title)

@app.callback(
    dash.dependencies.Output('title-table', 'children'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'clickData')])
def update_tf_idf(clickData):

    country_name = clickData['points'][0]['customdata']
    variety_name = clickData['points'][0]['hovertext']

    if type(country_name) == list:
        country_name = ''.join(country_name)
    else:
        pass

    dff = df_train[df_train['country'] == country_name]


    return html.P(style={'padding':'.5rem', 'margin':''},
                  children=f'Table Data for: {country_name}, {variety_name}')


if __name__ == '__main__':
    app.run_server(debug=True)

