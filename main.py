import csv
import requests
import movie

def getURL(movieID, apiKEY):
    return 'https://www.omdbapi.com/?i='+ movieID +'&plot=full&apikey=' + apiKEY

# Open CSV file in write mode
with open('movies_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 'Plot', 'Language', 'Country', 'Awards', 'Poster', 'imdbRating', 'imdbVotes', 'imdbID']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Loop through movie IDs
    for i in range(1, 6):
        movieID = 'tt' + str(i).zfill(7)
        data = requests.get(getURL(movieID, 'e4deafa')).json()
        movieObject = movie.Movie.from_dict(data)
