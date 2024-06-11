import csv
import requests
import movie
import time
import threading

def getURL(movieID, apiKEY):
    return 'https://www.omdbapi.com/?i='+ movieID +'&plot=full&apikey=' + apiKEY

def get_movie_data(movieID, apiKEY):
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(f"{request_time} : Request for movie ID {movieID}")
    
    data = requests.get(getURL(movieID, apiKEY)).json()
    if data.get("Ratings") is not None:
        del data["Ratings"]  # Exclude Ratings field from the data dictionary
        return data
    else:
        print(f"No ratings found for movie ID {movieID}")
        return None

def write_movie_data(movieID, apiKEY, writer):
    row_dict = get_movie_data(movieID, apiKEY)
    writer.writerow(row_dict)

def main():
    # Open CSV file in write mode
    with open('movies_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre', 'Director', 'Writer', 'Actors', 
                      'Plot', 'Language', 'Country', 'Awards', 'Poster', 'Metascore', 'imdbRating', 'imdbVotes', 
                      'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production', 'Website', 'Response']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        threads = []
        for i in range(1, 1001):
            movieID = 'tt' + str(i).zfill(7)
            thread = threading.Thread(target=write_movie_data, args=(movieID, 'e4deafa', writer))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()
