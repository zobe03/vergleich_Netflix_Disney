import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Daten für die Weltkarte vorbereiten
netflix = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/netflix_titles_cleaned.csv')
disney = pd.read_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv')


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
fig_netflix = go.Figure((go.Choropleth(
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
fig_netflix.update_layout(
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
fig_disney = go.Figure((go.Choropleth(
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
fig_disney.update_layout(
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

# Dash-App erstellen
app = dash.Dash(__name__)

# Layout definieren
app.layout = html.Div([
    html.Div([
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
            dcc.Graph(id='choropleth-map-netflix', figure=fig_netflix),
        ])
    ], className='six columns'),
    html.Div([
        dcc.Graph(id='choropleth-map-disney', figure=fig_disney),
    ], className='six columns'),
], className='row')



# Callback-Funktionen für Dropdown-Menü
@app.callback(
    Output('choropleth-map-netflix', 'figure'),
    Output('choropleth-map-disney', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_dropdown(selected_country):
    fig_netflix_updated = fig_netflix
    fig_disney_updated = fig_disney

    if selected_country:
        if selected_country == 'All' or selected_country is None:
            return fig_netflix, fig_disney

        if selected_country in countries_counts_netflix.index:
            # Filtern der Daten für Netflix
            filtered_countries_counts_netflix = countries_counts_netflix[countries_counts_netflix.index == selected_country]

            fig_netflix_updated = go.Figure((go.Choropleth(
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
            locations = [selected_country] + associated_countries_counts_netflix.index.tolist()
            counts = [filtered_countries_counts_netflix[selected_country]] + associated_countries_counts_netflix.tolist()

            fig_netflix_updated.add_trace(go.Choropleth(
                locationmode='country names',
                locations=locations,
                z=counts,
                zmin=0,
                zmax=3500,
                colorscale=colorscale_netflix,
                autocolorscale=False,
                marker_line_color='darkgrey',
                marker_line_width=1,
                text=[f"Total count of content in {selected_country}: {counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations, counts, counts)],
                hoverinfo='text'
            ))

            fig_netflix_updated.update_layout(
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

            fig_netflix_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_netflix.index,  
                z=filtered_countries_counts_netflix.values,  
                zmin=0,
                zmax=3500,
                colorscale=colorscale_netflix,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=[f"Total count of content in {selected_country}: {counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations, counts, counts)],
                hoverinfo='text'  
            )))
            fig_netflix_updated.update_layout(
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

            fig_disney_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_disney.index,  
                z=filtered_countries_counts_disney.values,  
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=[f"Total count of content in {selected_country}: {counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations, counts, counts)],
                hoverinfo='text'  
            )))
            # Markiere alle Länder, die mit dem ausgewählten Land verbunden sind, auf der Karte als Scatter Plot
        
            disney_associated_countries = disney[disney['country'].str.contains(selected_country, na=False)]['country'].str.split(', ')
            disney_associated_countries_counts = disney_associated_countries.explode().value_counts()

            # Markiere das ausgewählte Land und die verbundenen Länder auf der Karte
            disney_locations = [selected_country] + disney_associated_countries_counts.index.tolist()
            disney_counts = [filtered_countries_counts_disney[selected_country]] + disney_associated_countries_counts.tolist()

            fig_disney_updated.add_trace(go.Choropleth(
                locationmode='country names',
                locations=disney_locations,
                z=disney_counts,
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',
                marker_line_width=1,
                text=[f"Total count of content in {selected_country}: {counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations, counts, counts)],
                hoverinfo='text'
            ))
            fig_disney_updated.update_layout(
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

            fig_disney_updated = go.Figure((go.Choropleth(
                locationmode='country names',
                locations=filtered_countries_counts_disney.index,  
                z=filtered_countries_counts_disney.values,  
                zmin=0,
                zmax=1500,
                colorscale=colorscale_disney,
                autocolorscale=False,
                marker_line_color='darkgrey',  
                marker_line_width=1, 
                text=[f"Total count of content in {selected_country}: {counts[0]}<br>{z} contant was co-produced with {location}" for location, count, z in zip(locations, counts, counts)],
                hoverinfo='text'  
            )))
            fig_disney_updated.update_layout(
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
        
        return fig_netflix_updated, fig_disney_updated

    # Wenn das ausgewählte Land nicht in den entsprechenden Ländern vorhanden ist, gib die ursprünglichen Karten zurück
    return fig_netflix, fig_disney

# App starten
if __name__ == '__main__':
    app.run_server(debug=True)
