# Inspect and Clean --------------------------------------
import pandas as pd
import numpy as np
import os
import plotly as pl

df = pd.read_csv(os.path.join(os.path.dirname(__file__), '/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles.csv'), sep=',')

print('Info:')
print(df.info())

print('--------------------------------------------------------------------')
print('Head:')
print(df.head())

print('--------------------------------------------------------------------')
print('Shape:')
print(df.shape)

print('--------------------------------------------------------------------')
print('Nullwerte?: ')
print(df.isna())

print('--------------------------------------------------------------------')
print('Fehlende Werte bei Direktoren: ')
nodirector = df[df['director'].isnull()]
print(nodirector)
AnzahlZellen = np.product(df.shape)
print("Anzahl Zellen: ", AnzahlZellen)
NullwertZellen = df.isnull().sum()
print("Anzahl der Nullwertzellen in jeder Spalte: ", NullwertZellen)
GesamtanzahlNullwertZellen = NullwertZellen.sum()
print("Gesamtanzahl der Nullwertzellen: ", GesamtanzahlNullwertZellen)

print('--------------------------------------------------------------------')
print('Leere Zellen in der Spalte: Director, ersetzten mit: unknown')
NeueDirektorenSpalte = df.fillna({'director': 'unknown'}, inplace=True)
print(NeueDirektorenSpalte)

print('--------------------------------------------------------------------')
print('Leere Zellen in der Spalte: Cast, ersetzten mit: unknown')
NeueCastSpalte = df.fillna({'cast': 'unknown'}, inplace=True)
print(NeueCastSpalte)

print('--------------------------------------------------------------------')
print('Leere Zellen in der Spalte: Country, ersetzten mit: unknown')
df['country'].fillna('unknown', inplace=True)
print(df['country'])


print('--------------------------------------------------------------------')

# -> Leere date-added, rating, duration Spalten lieber löschen, da sie die Diagramme zu sehr beeinflussen
            #print('Leere Zellen in der Spalte: Date_added, ersetzten mit: unknown')
            #NeueDate_AddedSpalte = df['date_added'].fillna('unknown')
            #print(NeueDate_AddedSpalte)
            #print('--------------------------------------------------------------------')
            #print('Leere Zellen in der Spalte: Rating, ersetzten mit: unknown')
            #NeueRatingSpalte = df['rating'].fillna('unknown')
            #print(NeueRatingSpalte)
            #print('--------------------------------------------------------------------')
            #print('Leere Zellen in der Spalte: Duration, ersetzten mit: unknown')
            #NeueDurationSpalte = df['duration'].fillna('unknown')
            #print(NeueDurationgSpalte)


print('Spalten, wo leere Zellen in date_added, rating sind, löschen')
df.dropna(subset=['date_added', 'rating'], inplace=True)
print(df.isnull().sum())
print(df.shape)

print('--------------------------------------------------------------------')
print('Date_added in separate Spalten splitten: Monat und Jahr')
df['month_added'] = df['date_added'].apply(lambda x:x.split(',')[0].split()[0])
df['year_added'] = df['date_added'].apply(lambda x:x.split(',')[1])
df.drop('date_added', axis=1, inplace=True)
df['year_added'] = df['year_added'].astype(int)
print(df.info())
print(df[['month_added', 'year_added']])
print(df.shape)

print('--------------------------------------------------------------------')
print('year_added kann unmöglich kleiner als release_year sein')
df.drop(df[df['year_added']<df['release_year']].index, inplace=True)
print(df.shape)

print('--------------------------------------------------------------------')
print('Wie viele typen gibt es:') #-> falsche Schreibweise?
print(df['type'].nunique())
Anzahl_Filme_je_Typ = df['type'].value_counts()
print(Anzahl_Filme_je_Typ)

print('--------------------------------------------------------------------')
print('Wie viele Direktoren gibt es:') 
print(df['director'].nunique())
Anzahl_Filme_je_Direktor = df['director'].value_counts()
print(Anzahl_Filme_je_Direktor)

print('--------------------------------------------------------------------')
print('Wie viele Länder gibt es:') 
print(df['country'].nunique())
Anzahl_Filme_je_Land = df['country'].value_counts()
print(Anzahl_Filme_je_Land)

print('--------------------------------------------------------------------')
print('Wie viele year_added gibt es:') 
print(df['year_added'].nunique())
Anzahl_Filme_je_year_added = df['year_added'].value_counts()
print(Anzahl_Filme_je_year_added)

print('--------------------------------------------------------------------')
print('Wie viele month_added gibt es:') #-> falsche Schreibweise?
print(df['month_added'].nunique())
Anzahl_Filme_je_month_added = df['month_added'].value_counts()
print(Anzahl_Filme_je_month_added)

print('--------------------------------------------------------------------')
print('Wie viele rating gibt es:') #-> falsche Schreibweise?
print(df['rating'].nunique())
Anzahl_Filme_je_rating = df['rating'].value_counts()
print(Anzahl_Filme_je_rating)


print('--------------------------------------------------------------------')
print('Duplikate:')
duplikate = df.duplicated(subset=['title'])
print(df[duplikate])
Anzahl_Duplikat = df[duplikate].shape[0]
print(Anzahl_Duplikat)

print('--------------------------------------------------------------------')
print('Auf einzigartige Werte die Spalten überprüfen:')
unique_countries = df['country'].unique()
print(unique_countries)

print('--------------------------------------------------------------------')
#Countries zerlegen in mehrere Spalten
df_copy = df.copy()
df_copy['country'] = df_copy['country'].str.split(',')
max_countries = df_copy['country'].apply(len).max()
for i in range(max_countries):
    df_copy[f'Country {i+1}'] = df_copy['country'].apply(lambda x: x[i] if len(x) > i else '')
for i in range(max_countries):
    df_copy[f'Country {i+1}'] = df_copy[f'Country {i+1}'].str.strip()
print(df_copy.head())

print('--------------------------------------------------------------------')
#Countries wieder zusammenführen -> aber Anzahl filme auf einzelne staaten untersuchen
country_columns = [f'Country {i+1}' for i in range(max_countries)]
df_countries = df_copy.melt(value_vars=country_columns, value_name='Movie_Count')
df_countries.dropna(subset=['Movie_Count'], inplace=True)
movies_per_country = df_countries['Movie_Count'].value_counts()
print(movies_per_country)

print('--------------------------------------------------------------------')
# Countries zerlegen in mehrere Spalten
df_copy_2 = df.copy()
df_copy_2['director'] = df_copy_2['director'].str.split(',')
max_directors = df_copy_2['director'].apply(len).max()
for i in range(max_directors):
    df_copy_2[f'director {i+1}'] = df_copy_2['director'].apply(lambda x: x[i] if len(x) > i else '')
for i in range(max_directors):
    df_copy_2[f'director {i+1}'] = df_copy_2[f'director {i+1}'].str.strip()
print(df_copy_2.head())

print('--------------------------------------------------------------------')
# directors wieder zusammenführen -> aber Anzahl filme auf einzelne Regisseure untersuchen
director_columns = [f'director {i+1}' for i in range(max_directors)]
df_directors = df_copy_2.melt(value_vars=director_columns, value_name='Director')
df_directors.dropna(subset=['Director'], inplace=True)
movies_per_director = df_directors['Director'].value_counts()
print(movies_per_director)

print('--------------------------------------------------------------------')
#Listed_in zerlegen in mehrere Spalten
df_copy3 = df.copy()
df_copy3['listed_in'] = df_copy3['listed_in'].str.split(',')
max_listed_in = df_copy3['listed_in'].apply(len).max()
for i in range(max_listed_in):
    df_copy3[f'listed_in {i+1}'] = df_copy3['listed_in'].apply(lambda x: x[i] if len(x) > i else '')
for i in range(max_listed_in):
    df_copy3[f'listed_in {i+1}'] = df_copy3[f'listed_in {i+1}'].str.strip()
print(df_copy3.head())
print('--------------------------------------------------------------------')
# listed_in wieder zusammenführen -> aber Anzahl filme auf einzelne kategorien untersuchen
listed_in_columns = [f'listed_in {i+1}' for i in range(max_listed_in)]
df_listed_in = df_copy3.melt(value_vars=listed_in_columns, value_name='Listed_in')
df_listed_in.dropna(subset=['Listed_in'], inplace=True)
movies_per_listed_in = df_listed_in['Listed_in'].value_counts()
print(movies_per_listed_in)


print('--------------------------------------------------------------------')
print(df['year_added'].describe())
print(df['release_year'].describe())

print('--------------------------------------------------------------------')
import pycountry

print('Plausibilität der Länder überprüfen:')
def is_valid_country(country_name):
    if pd.isna(country_name) or country_name.lower() in ['unknown'] + ['russia']:
        return True
    try:
        pycountry.countries.lookup(country_name)
        return True
    except LookupError:
        return False


invalid_countries = df['country'].apply(lambda x: [country.strip() for country in str(x).split(',') if country.strip() != 'unknown' and not is_valid_country(country.strip())])

print('Nicht plasible Länder')
if len(invalid_countries[invalid_countries.apply(len) > 0]) == 0:
    print('Alle Länder sind plausibel')
else:
    print(invalid_countries[invalid_countries.apply(len) > 0])

print(df['listed_in'])
# Genres sortieren für dropdown Disney
def rewrite_genres(genres):
    rewritten_genres = []
    for genre in genres:
        if genre in ['Action-Adventure', 'Survival', 'Spy/Espionage', 'Superhero', 'Mystery']:
            rewritten_genres.append('Action & Adventure')
        elif genre == 'Anime Features':
            rewritten_genres.append('Anime')
        elif genre in ['Kids', 'Family']:
            rewritten_genres.append('Children & Family')
        elif genre == 'Parody':
            rewritten_genres.append('Comedy')
        elif genre in ['Music', 'Musical', 'Dance', 'Concert Film']:
            rewritten_genres.append('Music & Musicals')
        elif genre in ['Romantic Comedy', 'Romance']:
            rewritten_genres.append('Romantic')
        elif genre in ['Fantasy', 'Science Fiction']:
            rewritten_genres.append('Sci-Fi & Fantasy')
        elif genre in ['Disaster']:
            rewritten_genres.append('Thriller')
        elif genre in ['Crime', 'Police/Cop']:
            rewritten_genres.append('Crime')
        elif genre in ['Historical', 'Biographical', 'Docuseries']:
            rewritten_genres.append('Documentary')
        elif genre in ['Soap Opera / Melodrama']:
            rewritten_genres.append('Drama')
        elif genre in ['Animals & Nature', 'Travel', 'Medical']:
            rewritten_genres.append('Science & Nature')
        elif genre in ['Anthology', 'Reality', 'Variety', 'Game Show / Competition', 'Series', 'Movies', 'Western']:
            rewritten_genres.append('Entertainment')
        elif genre in ['Lifestyle', 'Coming of Age']:
            rewritten_genres.append('Culture & Lifestyle')
        elif genre in ['Talk Show']:
            rewritten_genres.append('Stand-Up Comedy & Talk Shows')
        elif genre in ['Buddy']:
            rewritten_genres.append('Teen')
        else:
            rewritten_genres.append(genre)
    unique_genres = list(set(rewritten_genres))
    return ', '.join(unique_genres)

# Umschreibung für Gruppierung
df['listed_in'] = df['listed_in'].str.split(', ').apply(rewrite_genres)
disney_genre = df['listed_in'].str.split(', ', expand=True).stack()
disney_genre_counts = disney_genre.value_counts()
# Ausgabe der Anzahl von Genres
print("Anzahl der Genres:", disney_genre_counts)


df.to_csv('/Users/student/Desktop/2Semester/Data Visualization/Abgabe/1_Datensets/disney_plus_titles_cleaned.csv', index=False)