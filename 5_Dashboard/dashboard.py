import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')
netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')

# Zusatzdaten
# Figur 1--------------------------------------------------------------------------------------------------------------

Typ_Disney = disney['type'].value_counts()
Typ_Netflix = netflix['type'].value_counts()

netflix_kleiner_teil_index = Typ_Netflix.idxmin()
netflix_kleiner_teil_wert = Typ_Netflix.min()
netflix_großer_teil_wert = Typ_Netflix.sum() - netflix_kleiner_teil_wert

disney_kleiner_teil_index = Typ_Disney.idxmin()
disney_kleiner_teil_wert = Typ_Disney.min()
disney_großer_teil_wert = Typ_Disney.sum() - disney_kleiner_teil_wert

# Figur 2--------------------------------------------------------------------------------------------------------------
# Disney Genres
disney_genres = disney['listed_in'].str.split(', ', expand=True).stack()
disney_genre_counts = disney_genres.value_counts().head(10)  # Filter the top 10 genres
disney_colorscale=[[0, '#BFF5FD'], [1, '#142864']]

# Netflix Genres
netflix_genres = netflix['listed_in'].str.split(', ', expand=True).stack()
netflix_genre_counts = netflix_genres.value_counts().head(10)  # Filter the top 10 genres
netflix_colorscale=[[0, '#E50914'], [1, '#141414']]

# Create subplots
fig2 = make_subplots(rows=1, cols=2, subplot_titles=('Top 10 Disney+ Genres', 'Top 10 Netflix Genres'))

# Add Disney+ data to subplot 1
fig2.add_trace(go.Bar(x=disney_genre_counts.index, y=disney_genre_counts.values,
                     marker=dict(color=disney_genre_counts.values, colorscale=disney_colorscale),
                     showlegend=False),
              row=1, col=1)

# Add Netflix data to subplot 2
fig2.add_trace(go.Bar(x=netflix_genre_counts.index, y=netflix_genre_counts.values,
                     marker=dict(color=netflix_genre_counts.values, colorscale=netflix_colorscale),
                     showlegend=False),
              row=1, col=2)

# Update layout
fig2.update_layout(title='<i><b>Top 10 Genre Contributions for Disney+ and Netflix</b></i>',
                  title_x=0.5,
                  font=dict(family='cursive', size=30, color='white'),
                  plot_bgcolor='rgba(0, 0, 0, 1)',  # Black background for Netflix
                  paper_bgcolor='rgba(0, 0, 0, 1)',  # Black background for Netflix
                  annotations=[dict(x=0.22, y=0.95, xref='paper', yref='paper',  # Disney+ annotation position
                                    text='<b>Disney+</b>', showarrow=False,
                                    font=dict(family='cursive', size=25, color='#BFF5FD')),
                               dict(x=0.78, y=0.95, xref='paper', yref='paper',  # Netflix annotation position
                                    text='<b>Netflix</b>', showarrow=False,
                                    font=dict(family='Open Sans', size=25, color='#E50914'))])

fig2.update_xaxes(tickangle=45, tickfont=dict(size=12, family='Droid Serif', color='white'))
fig2.update_yaxes(tickfont=dict(size=15, family='Droid Serif', color='white'))

# Figur 3--------------------------------------------------------------------------------------------------------------
# Disney data processing
disney_movies_data = disney[(disney['type'] == 'Movie') & (disney['release_year'] >= 1940) & (disney['release_year'] <= 2020)]
disney_tv_shows_data = disney[(disney['type'] == 'TV Show') & (disney['release_year'] >= 1940) & (disney['release_year'] <= 2020)]
disney_movies_by_year = disney_movies_data['release_year'].value_counts().sort_index()
disney_tv_shows_by_year = disney_tv_shows_data['release_year'].value_counts().sort_index()

# Netflix data processing
movies_data = netflix[(netflix['type'] == 'Movie') & (netflix['release_year'] >= 1940) & (netflix['release_year'] <= 2020)]
tv_shows_data = netflix[(netflix['type'] == 'TV Show') & (netflix['release_year'] >= 1940) & (netflix['release_year'] <= 2020)]
movies_by_year = movies_data['release_year'].value_counts().sort_index()
tv_shows_by_year = tv_shows_data['release_year'].value_counts().sort_index()

# Figur 4--------------------------------------------------------------------------------------------------------------
countries_netflix = netflix['country'].str.split(', ', expand=True).stack()
countries_counts_netflix = countries_netflix.value_counts()

if 'unknown' in countries_counts_netflix.index:
    countries_counts_netflix = countries_counts_netflix.drop('unknown')

colorscale_netflix = [
    [0, '#FFE4C4'],  
    [0.025, '#FF0000'],  
    [0.2, '#8B0000'],    
    [1, '#000000'], 
]

countries_disney = disney['country'].str.split(', ', expand=True).stack()
countries_counts_disney = countries_disney.value_counts()

if 'unknown' in countries_counts_disney.index:
    countries_counts_disney = countries_counts_disney.drop('unknown')

colorscale_disney = [
    [0, '#BFF5FD'],    
    [0.7, '#113CCF'],
    [1, '#142864']
]

# Weltkarte erstellen und Länder darstellen für Netflix
fig4_netflix = go.Figure((go.Choropleth(
    locationmode='country names',
    locations=countries_counts_netflix.index,  
    z=countries_counts_netflix.values,  
    zmin=0,
    zmax=3500,
    colorscale=colorscale_netflix,
    autocolorscale=False,
    marker_line_color='darkgrey',  
    marker_line_width=1, 
    text=countries_counts_netflix.index,  
    hoverinfo='location+z',  
)))
fig4_netflix.update_layout(
    title='Netflix Content by Country',
    font=dict(family='Open Sans', color='#E50914', size=15),
    title_x=0.5,
    geo=dict(
        showframe=True,  
        showcoastlines=False,  
        projection_type='natural earth', 
        showland=True,  
        landcolor='rgb(217, 217, 217)',  
    ),
)

# Weltkarte erstellen und Länder darstellen für Disney+
fig4_disney = go.Figure((go.Choropleth(
    locationmode='country names',
    locations=countries_counts_disney.index,  
    z=countries_counts_disney.values,  
    zmin=0,
    zmax=1500,
    colorscale=colorscale_disney,
    autocolorscale=False,
    marker_line_color='darkgrey',  
    marker_line_width=1, 
    text=countries_counts_disney.index,  
    hoverinfo='location+z',  
)))
fig4_disney.update_layout(
    title='Disney+ Content by Country',
    font=dict(family='cursive', color='#113CCF', size=15),
    title_x=0.5,
    geo=dict(
        showframe=True,  
        showcoastlines=False,  
        projection_type='natural earth', 
        showland=True,  
        landcolor='white',  
        showocean=True,
        oceancolor='darkgrey',
    ),
)

# Dropdown-Menü-Optionen für alle Länder
all_countries = list(set(countries_counts_netflix.index) | set(countries_counts_disney.index))
all_countries.sort()  # Sortiere die Liste alphabetisch
all_countries.insert(0, 'All')  # Füge "All" am Anfang der Liste ein
dropdown_options = [{'label': country, 'value': country} for country in all_countries]

# Figur 5--------------------------------------------------------------------------------------------------------------
# Genres für Disney+ und Netflix zusammenführen und eindeutige Genres erhalten
genres_disney = disney['listed_in'].str.split(', ', expand=True).stack()
genres_netflix = netflix['listed_in'].str.split(', ', expand=True).stack()
all_genres = pd.concat([genres_disney, genres_netflix]).unique()

# Text für Tab 1--------------------------------------------------------------------------------------------------------------
text1 = "Through the analysis and visualization of data from Netflix and Disney+, potential users gain valuable insights to aid in their decision-making between the two streaming platforms. This analysis considers various aspects, including the quantity and diversity of available content, enabling users to make well-informed choices."
text2 = "This dashboard is a project born out of pure passion for movies and series, as well as an interest in Netflix and Disney+."
text3 = "The dashboard provides a comprehensive overview of the content available on Netflix and Disney+, including the types of content, the number of releases by year, and the content produced in different countries. Additionally, the dashboard offers recommendations for movies and TV shows based on the user's preferences."
text4 = "Disney+ and Netflix are two of the most popular media and video streaming platforms globally. The tabular datasets contain listings of all the movies and TV shows available on Disney+ and Netflix until 2020, respectively, along with details such as titel, maturity ratings, release year, duration, etc."

       
# Dash- APP erstellen --------------------------------------------------------------------------------------------------------------
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout für Tab 1
tab1_layout = html.Div([
    html.Br(),
    html.Div([
    html.Label(text2, style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'font-style':'italic', 'font-size': '18px', 'font-weight': 'bold'}),
    html.Br(),  # Line break
    html.Br(),  # Line break
    html.Label(text1, style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'font-style':'italic', 'font-size': '17px'}),
    html.Br(),  # Line break
    html.Br(),  # Line break
    html.Label(text3, style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'font-style':'italic', 'font-size': '17px'}),
    html.Br(),  # Line break
    html.Br(),  # Line break
    html.Label(text4, style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'font-style':'italic', 'font-size': '17px'}),
], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '10px'}),

    html.Div([
        dcc.Graph(
            id='content-type-pie',
            figure={
                'data': [
                    go.Pie(labels=Typ_Netflix.index, values=[netflix_großer_teil_wert, netflix_kleiner_teil_wert], pull=[0, 0.1],
                        hoverinfo='label+percent', textinfo='value', textfont=dict(size=20, family='Open Sans'),
                        marker=dict(colors=['#E50914', '#141414'], line=dict(color='#000000', width=0)),
                        domain={'x':[0,0.55]}, showlegend=True, legendgroup='legend1'),
                    go.Pie(labels=Typ_Disney.index, values=[disney_großer_teil_wert, disney_kleiner_teil_wert], pull=[0, 0.1],
                        hoverinfo='label+percent', textinfo='value', textfont=dict(size=20, family='cursive'),
                        marker=dict(colors=['#BFF5FD', '#142864'], line=dict(color='#000000', width=0)),
                        domain={'x':[0.5,1]}, showlegend=True, legendgroup='legend2')
                ],
                'layout': go.Layout(
                    title='<i><b>Content type provided by Netflix and Disney+</b></i>',
                    title_font=dict(family='cursive', size=30, color='black'),
                    title_x=0.5,
                    annotations=[dict(text='<b>Netflix</b>', x=0.23, y=1.11, font_size=25, font_family='Open Sans', font_color= 'black', showarrow=False),
                                dict(text='<b>Disney+</b>', x=0.79, y=1.15, font_size=25, font_family='cursive', font_color='#142864', showarrow=False)],
                    legend=dict(
                        x=1,
                        y=1,
                        traceorder="normal",
                        font=dict(
                            family="Droid Serif",
                            size=15,
                            color="black"),
                        bgcolor="lightgrey",
                        title='Content Type'
                    )
                )
            }
        ),
    ], style={'width': '69%', 'height': '40vh', 'display': 'inline-block'}),
    html.Br(),
    html.Br(),
    dcc.Graph(figure=fig2, style={'width': '100%', 'height':'80vh', 'display': 'inline-block'}),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1('Number of Movie and TV Show Releases by Year', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'cursive','font-weight': 'bold', 'font-size': '30px'}),
        html.Div([
            html.Label('Select Platform:', style={'font-weight': 'bold', 'font-family': 'Droid Serif'}),
            dcc.Dropdown(
                id='platform-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Disney', 'value': 'Disney'},
                    {'label': 'Netflix', 'value': 'Netflix'}
                ],
                value='All',
                style={'width': '100%'}
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),
        html.Div([
            html.Label('Select Content:', style={'font-weight': 'bold', 'font-family': 'Droid Serif'}),
            dcc.Dropdown(
                id='type-dropdown',
                options=[
                    {'label': 'All', 'value': 'All'},
                    {'label': 'Movie', 'value': 'Movie'},
                    {'label': 'TV Show', 'value': 'TV Show'}
                ],
                value='All',
                style={'width': '100%'}
            ),
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        dcc.Graph(
            id='release-timeline',
            config={'displayModeBar': False},
            style={'height': '500px', 'width': '100%'}  
        ),
    ], style={'width': '100%', 'display': 'inline-block'}),

], style={'width': '100%'})



# Layout für Tab 2
tab2_layout = html.Div([
    html.H1('Content by Country', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'Droid Serif','font-weight': 'bold', 'font-size': '40px'}),
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=dropdown_options,
            value=None,
            style={'width': '250px'}),  # Breite der Dropdown-Liste anpassen
        html.Label('Once you select a country, that country will be color-highlighted on the maps. You will see how many content were produced in that country. Other countries will also be color-highlighted to show how many content were co-produced with the selected country. For example, 803 content were produced in the United Kingdom, of which 278 content were co-produced with the United States. You can see this information by hovering over the United States on the map. If the colorscale disappears, it means that there are no content in the dataset that were filmed in that country for that platform.',
                   style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'font-style':'italic', 'display': 'block', 'margin-top': '10px'})
    ], style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}),
    
    html.Div([
        html.Div([
            dcc.Graph(id='choropleth-map-netflix', figure=fig4_netflix),
        ], className='six columns', style={'display': 'inline-block', 'width': '46%', 'height': '80vh'}),
        html.Div([
            dcc.Graph(id='choropleth-map-disney', figure=fig4_disney),
        ], className='six columns', style={'display': 'inline-block', 'width': '47%', 'height': '80vh'}),
    ], className='row', style={'width': '100%',  'center': 'center'}),
])




# Layout für Tab 3
tab3_layout = html.Div([
    html.H2('Recommendations'),
    html.P('Inhalt für Tab 3...'),
    html.H1(
        'Film & TV Show Recommendation', 
        style={
            'text-align': 'center',
            'font-style': 'italic',
            'font-family': 'cursive',
            'font-weight': 'bold',
            'font-size': '30px', 
            'color': 'white'
        }
    ),
    html.Div([
        html.Label('Select Content Type:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='content-type-dropdown',
            options=[
                {'label': 'Movie', 'value': 'Movie'},
                {'label': 'TV Show', 'value': 'TV Show'}
            ],
            value='Movie',
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Genre:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='genre-dropdown',
            options=[{'label': genre, 'value': genre} for genre in all_genres],                    
            value=all_genres[1],
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Age Limit:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='selected-age',
            options=[
                {'label': 'ALL', 'value': 'ALL'},
                {'label': 'Unrated', 'value': 'unrated'},
                {'label': '0-6', 'value': '0-6'},
                {'label': '7-12', 'value': '7-12'},
                {'label': '13-16', 'value': '13-16'},
                {'label': '17+', 'value': '17+'},
                {'label': '17- with Parental Guidance', 'value': '17- PG'}
            ],
            value='ALL',
            style={'width': '100%', 'color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        html.Label('Select Column:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Dropdown(
            id='column-dropdown',
            options=[
                {'label': 'None', 'value': 'None'},
                {'label': 'Title', 'value': 'title'},
                {'label': 'Description', 'value': 'description'},
            ],
            value='None',
            style={'width': '100%', 'color': 'black', 'background-color': 'white', 'margin-right': '10px'}
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Div([
        html.Label('Search:', style={'font-weight': 'bold', 'font-family': 'Droid Serif', 'color': 'white'}),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search...',
            style={'width': '100%', 'height':'30px','color': 'black', 'background-color': 'white'}
        ),
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    html.Br(),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Disney+', style={'color':'black', 'text-align':'center', 'font-family':'cursive'},children=[
            html.Br(),
            html.Div([
                html.H2('Disney+', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'cursive','font-weight': 'bold', 'font-size': '25px', 'color': 'white'}),
                dash_table.DataTable(
                    id='disney-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Duration', 'id': 'duration'},
                        {'name': 'Release Year', 'id': 'release_year'}
                    ],
                    style_table={'width': '99%', 'overflowX': 'auto', 'border': '2px solid darkgrey', 'background': 'rgba(0, 0, 0, 0.7)'},
                    style_cell={'minWidth': '50px', 'maxWidth': '100px', 'whiteSpace': 'normal', 'color': 'white', 'border': '1px solid darkgrey', 'background': 'transparent', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                    style_data_conditional=[
                        {   
                            'if' : {'row_index': 'odd'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
                        },
                        {
                            'if':{'row_index': 'even'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.7)',
                        },
                        {
                            'if': {'column_id': 'description'},
                            'maxWidth': '300px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        {
                            'if': {'column_id': 'title'},
                            'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                    ],    
                ),
                ], style={'width': '99.6%', 'display': 'inline-block', 'vertical-align': 'top', 'border': '2px solid transparent', 'background': 'linear-gradient(to right, #BFF5FD, #142864)'}),
            ]),
        dcc.Tab(label='Netflix', style={'color':'black', 'font-family':'Open Sans', 'text-align':'center'},  children=[
            html.Br(),
            html.Div([
                html.H2('Netflix', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'Open Sans','font-weight': 'bold', 'font-size': '25px', 'color': 'white'}),
                dash_table.DataTable(
                    id='netflix-table',
                    columns=[
                        {'name': 'Title', 'id': 'title'},
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Duration', 'id': 'duration'},
                        {'name': 'Release Year', 'id': 'release_year'}
                    ],
                    style_table={'width': '99%', 'overflowX': 'auto', 'border': '2px solid darkgrey', 'background': 'rgba(0, 0, 0, 0.7)'},
                    style_cell={'minWidth': '50px', 'maxWidth': '100px', 'whiteSpace': 'normal', 'color': 'white', 'border': '1px solid darkgrey', 'background': 'transparent', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                    style_data_conditional=[
                        {   
                            'if' : {'row_index': 'odd'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.4)',
                        },
                        {
                            'if':{'row_index': 'even'},
                            'backgroundColor': 'rgba(0, 0, 0, 0.7)',
                        },
                        {
                            'if': {'column_id': 'description'},
                            'maxWidth': '300px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                        {
                            'if': {'column_id': 'title'},
                            'maxWidth': '150px',
                            'overflow': 'hidden',
                            'textOverflow': 'ellipsis',
                        },
                    ],
                ),
            ], style={'width': '99.6%', 'display': 'inline-block', 'vertical-align': 'top', 'border': '2px solid transparent', 'background': 'linear-gradient(to right, #000000, #E50914)'}),
        ]),
    ], style={'backgroundColor': 'black', 'color': 'white', 'fontWeight': 'bold', 'border': '1px solid darkgrey', 'borderRadius': '5px'})
], style={'backgroundColor': 'black'})

# Layout für das gesamte Dashboard mit Tabs
app.layout = html.Div([
    html.H1('Stream Duel: Netflix and Disney+', style={'textAlign': 'center', 'fontFamily': 'Droid Serif', 'fontSize': 40, 'color': 'black', 'fontStyle': 'italic', 'fontWeight': 'bold'}),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Content, Genre annd more!!!', value='tab-1'),
        dcc.Tab(label='Content by Country', value='tab-2'),
        dcc.Tab(label='Recommendation', value='tab-3')
    ]),
    html.Div(id='tabs-content')
])

# Callback zum Aktualisieren des Inhalts basierend auf dem ausgewählten Tab
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab1_layout
    elif tab == 'tab-2':
        return tab2_layout
    elif tab == 'tab-3':
        return tab3_layout

# Callback für die Aktualisierung des Zeitstrahls basierend auf den ausgewählten Plattform- und Inhaltsfiltern
@app.callback(Output('release-timeline', 'figure'),
              [Input('platform-dropdown', 'value'),
               Input('type-dropdown', 'value')])
def update_timeline(selected_platform, selected_type):
    fig3 = go.Figure()
    
    if selected_platform == 'Disney' or selected_platform == 'All':
        if selected_type == 'Movie' or selected_type == 'All':
            # Add Disney+ movies
            fig3.add_trace(go.Scatter(x=disney_movies_by_year.index, y=disney_movies_by_year.values, 
                                     mode='lines+markers', name='Disney+ Movies', 
                                     line=dict(color='#142864', width=2), 
                                     marker=dict(color='#142864'), 
                                     legendgroup='Disney+'))
        if selected_type == 'TV Show' or selected_type == 'All':
            # Add Disney+ TV shows
            fig3.add_trace(go.Scatter(x=disney_tv_shows_by_year.index, y=disney_tv_shows_by_year.values, 
                                     mode='lines+markers', name='Disney+ TV Shows', 
                                     line=dict(color='#BFF5FD', width=2), 
                                     marker=dict(color='#BFF5FD'), 
                                     legendgroup='Disney+'))
    
    if selected_platform == 'Netflix' or selected_platform == 'All':
        if selected_type == 'Movie' or selected_type == 'All':
            # Add Netflix movies
            fig3.add_trace(go.Scatter(x=movies_by_year.index, y=movies_by_year.values, 
                                     mode='lines+markers', name='Netflix Movies', 
                                     line=dict(color='#E50914', width=2), 
                                     marker=dict(color='#E50914'), 
                                     legendgroup='Netflix'))
        if selected_type == 'TV Show' or selected_type == 'All':
            # Add Netflix TV shows
            fig3.add_trace(go.Scatter(x=tv_shows_by_year.index, y=tv_shows_by_year.values, 
                                     mode='lines+markers', name='Netflix TV Shows', 
                                     line=dict(color='#141414', width=2), 
                                     marker=dict(color='#141414'), 
                                     legendgroup='Netflix'))
    
    # Update layout
    fig3.update_layout(
        title_x=0.5,
        title_font=dict(size=30, family='cursive', color='black'),
        xaxis_title='Release Year',
        yaxis_title='Number of Releases',
        font=dict(family='Droid Serif'),
        plot_bgcolor='darkgrey',
        showlegend=True,
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(tickangle=45, tickfont=dict(size=12, family='Droid Serif'), linecolor='black', linewidth=1.5, range=[1940, 2020.5]),
        yaxis=dict(tickfont=dict(size=12, family='Droid Serif'), linecolor='black', linewidth=1.5),
        legend=dict(
            x=1.025,
            y=1,
            traceorder="normal",
            font=dict(
                family="Droid Serif",
                size=15,
                color="black"),
            bgcolor="lightgrey",
            title='Platform & Content Type'
        )
    )
    
    return fig3

# Callback-Funktionen für Dropdown-Menü
@app.callback(
    Output('choropleth-map-netflix', 'figure'),
    Output('choropleth-map-disney', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_dropdown(selected_country):
    fig4_netflix_updated = fig4_netflix
    fig4_disney_updated = fig4_disney

    if selected_country:
        if selected_country == 'All' or selected_country is None:
            return fig4_netflix, fig4_disney

        if selected_country in countries_counts_netflix.index:
            # Filtern der Daten für Netflix
            filtered_countries_counts_netflix = countries_counts_netflix[countries_counts_netflix.index == selected_country]

            fig4_netflix_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_netflix.index,  
                z=filtered_countries_counts_netflix.values,  
                zmin=0,
                zmax=3500,
                colorscale=colorscale_netflix,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=filtered_countries_counts_netflix.index,  
                hoverinfo='location+z',  
            )))

            # Markiere alle Länder, die mit dem ausgewählten Land verbunden sind, auf der Karte als Scatter Plot
            associated_countries_netflix = netflix[netflix['country'].str.contains(selected_country, na=False)]['country'].str.split(', ')
            associated_countries_counts_netflix = associated_countries_netflix.explode().value_counts()

            # Markiere das ausgewählte Land und die verbundenen Länder auf der Karte
            locations_netflix = [selected_country] + associated_countries_counts_netflix.index.tolist()
            counts_netflix = [filtered_countries_counts_netflix[selected_country]] + associated_countries_counts_netflix.tolist()

            fig4_netflix_updated.add_trace(go.Choropleth(
                locationmode='country names',
                locations=locations_netflix,
                z=counts_netflix,
                zmin=0,
                zmax=3500,
                colorscale=colorscale_netflix,
                autocolorscale=False,
                marker_line_color='darkgrey',
                marker_line_width=1,
                text=[f"Total count of content in {selected_country}: {counts_netflix[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations_netflix, counts_netflix, counts_netflix)],
                hoverinfo='text'
            ))

            fig4_netflix_updated.update_layout(
                title=f'Netflix Content in {selected_country} & associated countries',
                font=dict(family='Open Sans', color='#E50914', size=15),
                title_x=0.5,
                geo=dict(
                    showframe=True,  
                    showcoastlines=False,  
                    projection_type='natural earth', 
                    showland=True,  
                    landcolor='rgb(217, 217, 217)',  
                ),
            )
        else:
            # Filtern der Daten für Netflix
            filtered_countries_counts_netflix = countries_counts_netflix[countries_counts_netflix.index == selected_country]

            fig4_netflix_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_netflix.index,  
                z=filtered_countries_counts_netflix.values,  
                zmin=0,
                zmax=3500,
                colorscale=colorscale_netflix,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=filtered_countries_counts_netflix.index,  
                hoverinfo='location+z',  
            )))
            fig4_netflix_updated.update_layout(
                title=f'Netflix Content in {selected_country} & associated countries',
                font=dict(family='Open Sans', color='#E50914', size=15),
                title_x=0.5,
                geo=dict(
                    showframe=True,  
                    showcoastlines=False,  
                    projection_type='natural earth', 
                    showland=True,  
                    landcolor='rgb(217, 217, 217)',  
                ),
            )

    
        if selected_country in countries_counts_disney.index:
            # Filtern der Daten für Disney+
            filtered_countries_counts_disney = countries_counts_disney[countries_counts_disney.index == selected_country]

            fig4_disney_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_disney.index,  
                z=filtered_countries_counts_disney.values,  
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=filtered_countries_counts_disney.index,  
                hoverinfo='location+z', 
            )))
            # Markiere alle Länder, die mit dem ausgewählten Land verbunden sind, auf der Karte als Scatter Plot
        
            disney_associated_countries = disney[disney['country'].str.contains(selected_country, na=False)]['country'].str.split(', ')
            disney_associated_countries_counts = disney_associated_countries.explode().value_counts()

            # Markiere das ausgewählte Land und die verbundenen Länder auf der Karte
            disney_locations = [selected_country] + disney_associated_countries_counts.index.tolist()
            disney_counts = [filtered_countries_counts_disney[selected_country]] + disney_associated_countries_counts.tolist()

            fig4_disney_updated.add_trace(go.Choropleth(
                locationmode='country names',
                locations=disney_locations,
                z=disney_counts,
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',
                marker_line_width=1,
                text=[f"Total count of content in {selected_country}: {disney_counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(disney_locations, disney_counts, disney_counts)],
                hoverinfo='text'
            ))
            fig4_disney_updated.update_layout(
                title=f'Disney+ Content in {selected_country} & associated countries',
                font=dict(family='cursive', color='#113CCF', size=15),
                title_x=0.5,
                geo=dict(
                    showframe=True,  
                    showcoastlines=False,  
                    projection_type='natural earth', 
                    showland=True,  
                    landcolor='white',  
                    showocean=True,
                    oceancolor='darkgrey',
                ),
            )
        else:
            filtered_countries_counts_disney = countries_counts_disney[countries_counts_disney.index == selected_country]
            
            fig4_disney_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_disney.index,  
                z=filtered_countries_counts_disney.values,  
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=filtered_countries_counts_disney.index,  
                hoverinfo='location+z',   
            )))
            fig4_disney_updated.update_layout(
                title=f'Disney+ Content in {selected_country} & associated countries',
                font=dict(family='cursive', color='#113CCF', size=15),
                title_x=0.5,
                geo=dict(
                    showframe=True,  
                    showcoastlines=False,  
                    projection_type='natural earth', 
                    showland=True,  
                    landcolor='white',  
                    showocean=True,
                    oceancolor='darkgrey',
                ),
            )
        
        return fig4_netflix_updated, fig4_disney_updated

    # Wenn das ausgewählte Land nicht in den entsprechenden Ländern vorhanden ist, gib die ursprünglichen Karten zurück
    return fig4_netflix, fig4_disney


# Callback-Funktion für die Aktualisierung der Disney-Tabelle basierend auf den ausgewählten Filtern
@app.callback(
    Output('disney-table', 'data'),
    [Input('content-type-dropdown', 'value'),
     Input('genre-dropdown', 'value'),
     Input('selected-age', 'value'),
     Input('search-input', 'value'),
     Input('column-dropdown', 'value')]
)
def update_disney_table(selected_content_type, selected_genre, selected_age, search_value, column):
    try:
        if selected_age == '0-6':
            rating = ['V-Y']
        elif selected_age == '7-12':
            rating = ['TV-Y7', 'TV-Y7-FV']
        elif selected_age == '13-16':
            rating = ['PG-13', 'TV-14']
        elif selected_age == '17+':
            rating = ['NC-17']
        elif selected_age == '17- PG':
            rating = ['PG', 'TV-PG', 'R']
        elif selected_age == 'unrated':
            rating = ['NR', 'UR']
        else:
            rating = ['NR', 'UR', 'TV-G', 'G', 'PG', 'PG-13', 'TV-PG', 'R', 'NC-17', 'TV-14', 'TV-Y7', 'TV-Y7-FV', 'V-Y']

        if selected_content_type == 'Movie':
            data_disney = disney[(disney['type'] == 'Movie') & 
                                 (disney['listed_in'].str.contains(selected_genre)) & 
                                 (disney['rating'].isin(rating))]
        else:
            data_disney = disney[(disney['type'] == 'TV Show') & 
                                 (disney['listed_in'].str.contains(selected_genre)) & 
                                 (disney['rating'].isin(rating))]
        
        if search_value and column != 'None':
            filtered_data = data_disney[data_disney[column].str.contains(search_value, case=False, na=False)]
            return filtered_data[['title', 'description', 'duration', 'release_year']].to_dict('records')
        else:
            return data_disney[['title', 'description', 'duration', 'release_year']].to_dict('records')
    except Exception as e:
        return []
    
# Callback-Funktion für die Aktualisierung der Netflix-Tabelle basierend auf den ausgewählten Filtern
@app.callback(
    Output('netflix-table', 'data'),
    [Input('content-type-dropdown', 'value'),
     Input('genre-dropdown', 'value'),
     Input('selected-age', 'value'),
     Input('search-input', 'value'),
     Input('column-dropdown', 'value')]
)
def update_netflix_table(selected_content_type, selected_genre, selected_age, search_value, column):
    try:
        if selected_age == '0-6':
            rating = ['V-Y']
        elif selected_age == '7-12':
            rating = ['TV-Y7', 'TV-Y7-FV']
        elif selected_age == '13-16':
            rating = ['PG-13', 'TV-14']
        elif selected_age == '17+':
            rating = ['NC-17']
        elif selected_age == '17- PG':
            rating = ['PG', 'TV-PG', 'R']
        elif selected_age == 'unrated':
            rating = ['NR', 'UR']
        else:
            rating = ['NR', 'UR', 'TV-G', 'G', 'PG', 'PG-13', 'TV-PG', 'R', 'NC-17', 'TV-14', 'TV-Y7', 'TV-Y7-FV', 'V-Y']

        if selected_content_type == 'Movie':
            data_netflix = netflix[(netflix['type'] == 'Movie') & 
                                   (netflix['listed_in'].str.contains(selected_genre)) & 
                                   (netflix['rating'].isin(rating))]
        else:
            data_netflix = netflix[(netflix['type'] == 'TV Show') & 
                                   (netflix['listed_in'].str.contains(selected_genre)) & 
                                   (netflix['rating'].isin(rating))]
        
        if search_value and column != 'None':
            filtered_data = data_netflix[data_netflix[column].str.contains(search_value, case=False, na=False)]
            return filtered_data[['title', 'description', 'duration', 'release_year']].to_dict('records')
        else:
            return data_netflix[['title', 'description', 'duration', 'release_year']].to_dict('records')
    except Exception as e:
        return []

if __name__ == '__main__':
    app.run_server(debug=True)



