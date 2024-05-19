import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')
netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')

# Disney Genres
disney_genres = disney['listed_in'].str.split(', ', expand=True).stack()
disney_genre_counts = disney_genres.value_counts().head(10)  # Filter the top 10 genres
disney_colorscale=[[0, '#BFF5FD'], [1, '#142864']]

# Netflix Genres
netflix_genres = netflix['listed_in'].str.split(', ', expand=True).stack()
netflix_genre_counts = netflix_genres.value_counts().head(10)  # Filter the top 10 genres
netflix_colorscale=[[0, '#E50914'], [1, '#141414']]

# Create subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=('Top 10 Disney+ Genres', 'Top 10 Netflix Genres'))

# Add Disney+ data to subplot 1
fig.add_trace(go.Bar(x=disney_genre_counts.index, y=disney_genre_counts.values,
                     marker=dict(color=disney_genre_counts.values, colorscale=disney_colorscale),
                     showlegend=False),
              row=1, col=1)

# Add Netflix data to subplot 2
fig.add_trace(go.Bar(x=netflix_genre_counts.index, y=netflix_genre_counts.values,
                     marker=dict(color=netflix_genre_counts.values, colorscale=netflix_colorscale),
                     showlegend=False),
              row=1, col=2)

# Update layout
fig.update_layout(title='<i><b>Top 10 Genre Contributions for Disney+ and Netflix</b></i>',
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

fig.update_xaxes(tickangle=45, tickfont=dict(size=12, family='Droid Serif', color='white'))
fig.update_yaxes(tickfont=dict(size=15, family='Droid Serif', color='white'))

fig.show()
