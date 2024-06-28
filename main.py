import pymongo
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor, as_completed
import cloudscraper

# Initialize Cloudscraper instance
scraper = cloudscraper.create_scraper()

# Connect to the SQLite database
db_path = "C:\\Users\\lalan\\OneDrive\\Desktop\\IMDB"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to list all IDs
cursor.execute("SELECT id FROM filtered_titles")
table = cursor.fetchall()

# Extract IMDb IDs
imdb_ids = [row[0] for row in table]

# Close the database connection
conn.close()

key = '84c64481'

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mrs_with_ml"]
collection = db["filtered"]

def fetch(movieID, apiKey):
    url = f'https://www.omdbapi.com/?i={movieID}&plot=full&apikey={apiKey}'
    try:
        # Use cloudscraper instance for making the request
        response = scraper.gmet(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching movie {movieID}: {e}")
        return None

def main():
    batch_size = 100  # Adjust batch size as per your needs
    MAX_WORKERS = 100
    total_ids = len(imdb_ids)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i in range(0, total_ids, batch_size):
            batch_ids = imdb_ids[i:i+batch_size]
            
            # Print the range of requests being processed
            start_index = i + 1
            end_index = min(i + batch_size, total_ids)
            print(f"Processing requests {start_index} to {end_index} out of {total_ids}")
            
            future_to_movieID = {executor.submit(fetch, movie_id, key): movie_id for movie_id in batch_ids}
            
            for future in as_completed(future_to_movieID):
                movie_id = future_to_movieID[future]
                try:
                    data = future.result()
                    if data and data.get("Response") == "True":
                        collection.insert_one(data)
                    else:
                        print(f"No valid data found for movie {movie_id}")
                except Exception as e:
                    print(f"Exception for movie {movie_id}: {e}")

if __name__ == "__main__":
    main()
