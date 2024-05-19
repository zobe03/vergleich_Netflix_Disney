import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')
Typ_Disney = disney['type'].value_counts()

netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')
Typ_Netflix = netflix['type'].value_counts()

netflix_kleiner_teil_index = Typ_Netflix.idxmin()
netflix_kleiner_teil_wert = Typ_Netflix.min()
netflix_großer_teil_wert = Typ_Netflix.sum() - netflix_kleiner_teil_wert

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

# Netflix (links)
fig.add_trace(go.Pie(labels=Typ_Netflix.index, values=[netflix_großer_teil_wert, netflix_kleiner_teil_wert], pull=[0, 0.1],
                      hoverinfo='label+percent', textinfo='value', textfont=dict(size=20, family='Open Sans'),
                      marker=dict(colors=['#E50914', '#141414'], line=dict(color='#000000', width=0)),
                      domain={'x':[0,0.48]}, showlegend=True, legendgroup='legend1'),
                      row=1, col=1)

# Disney+ (rechts)
disney_kleiner_teil_index = Typ_Disney.idxmin()
disney_kleiner_teil_wert = Typ_Disney.min()
disney_großer_teil_wert = Typ_Disney.sum() - disney_kleiner_teil_wert

fig.add_trace(go.Pie(labels=Typ_Disney.index, values=[disney_großer_teil_wert, disney_kleiner_teil_wert], pull=[0, 0.1],
                     hoverinfo='label+percent', textinfo='value', textfont=dict(size=20, family='cursive'),
                     marker=dict(colors=['#BFF5FD', '#142864'], line=dict(color='#000000', width=0)),
                     domain={'x':[0.48,1]}, showlegend=True, legendgroup='legend2'),
                     row=1, col=2)

fig.update_layout(title='<i><b>Content type provided by Netflix and Disney+</b></i>', 
                   title_font=dict(family='cursive', size=30, color='black'),
                   title_x=0.5,
                   annotations=[dict(text='<b>Netflix</b>', x=0.18, y=1.05, font_size=25, font_family='Open Sans', font_color= 'black', bgcolor='white', showarrow=False),
                                dict(text='<b>Disney+</b>', x=0.8, y=1.06, font_size=25, font_family='cursive', font_color='#142864', bgcolor='white', showarrow=False)],
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

fig.show()
