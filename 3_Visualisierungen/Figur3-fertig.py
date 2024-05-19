import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load Disney and Netflix data
disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')
netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')

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

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.Div([
        html.H1('Number of Movie and TV Show Releases by Year', style={'text-align': 'center', 'font-style': 'italic', 'font-family':'cursive','font-weight': 'bold', 'font-size': '30px'}),
        html.Div([
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
        ], style={'padding': '20px', 'text-align': 'center'}),
        dcc.Graph(
            id='release-timeline',
            config={'displayModeBar': False},
            style={'height': '500px'}  
        ),
    ])
])

# Define callback to update scatter plot based on dropdown selection
@app.callback(
    Output('release-timeline', 'figure'),
    [Input('platform-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_timeline(selected_platform, selected_type):
    fig = go.Figure()
    
    if selected_platform == 'Disney' or selected_platform == 'All':
        if selected_type == 'Movie' or selected_type == 'All':
            # Add Disney+ movies
            fig.add_trace(go.Scatter(x=disney_movies_by_year.index, y=disney_movies_by_year.values, 
                                     mode='lines+markers', name='Disney+ Movies', 
                                     line=dict(color='#142864', width=2), 
                                     marker=dict(color='#142864'), 
                                     legendgroup='Disney+'))
        if selected_type == 'TV Show' or selected_type == 'All':
            # Add Disney+ TV shows
            fig.add_trace(go.Scatter(x=disney_tv_shows_by_year.index, y=disney_tv_shows_by_year.values, 
                                     mode='lines+markers', name='Disney+ TV Shows', 
                                     line=dict(color='#BFF5FD', width=2), 
                                     marker=dict(color='#BFF5FD'), 
                                     legendgroup='Disney+'))
    
    if selected_platform == 'Netflix' or selected_platform == 'All':
        if selected_type == 'Movie' or selected_type == 'All':
            # Add Netflix movies
            fig.add_trace(go.Scatter(x=movies_by_year.index, y=movies_by_year.values, 
                                     mode='lines+markers', name='Netflix Movies', 
                                     line=dict(color='#E50914', width=2), 
                                     marker=dict(color='#E50914'), 
                                     legendgroup='Netflix'))
        if selected_type == 'TV Show' or selected_type == 'All':
            # Add Netflix TV shows
            fig.add_trace(go.Scatter(x=tv_shows_by_year.index, y=tv_shows_by_year.values, 
                                     mode='lines+markers', name='Netflix TV Shows', 
                                     line=dict(color='#141414', width=2), 
                                     marker=dict(color='#141414'), 
                                     legendgroup='Netflix'))
    
    # Update layout
    fig.update_layout(
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
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
