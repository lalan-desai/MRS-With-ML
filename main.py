import requests
import time
import threading
import logging
import pymongo

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API key
apiKey = 'e4deafa'

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["movie_database"]
collection = db["movies"]

def getURL(movieID):
    return 'https://www.omdbapi.com/?i='+ movieID +'&plot=full&apikey=' + apiKey

# Function to get data from API
def get_movie_data(movieID):
    request_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    logging.info(f"{request_time} : Request for movie ID {movieID}")
    print(f"{request_time} : Request for movie ID {movieID}")
    try:
        response = requests.get(getURL(movieID))
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        
        if data.get("Response") == "True":
            
            return data
        else:
            logging.warning(f"No data found for movie ID {movieID}")
            return None
    except requests.RequestException as e:
        logging.error(f"Error retrieving data for movie ID {movieID}: {e}")
        return None

# Function to write movie data to MongoDB
def insert_movie_data(movieID):
    data = get_movie_data(movieID)
    if data:
        collection.insert_one(data)

# Main function
def main():
    threads = []
    for i in range(1, 1001):
        movieID = 'tt' + str(i).zfill(7)
        thread = threading.Thread(target=insert_movie_data, args=(movieID,))
        thread.start()
        threads.append(thread)
        # time.sleep(0.1)  # Sleep for 0.1 second between requests
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
