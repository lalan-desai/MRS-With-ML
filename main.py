import asyncio
import aiohttp
import pymongo

import json

key = '84c64481'
MAX_CONCURRENT_REQUESTS = 2000
TIMEOUT = 0
BATCH_SIZE = 2000

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["imdb"]
collection = db["content"]

async def fetch(session, movieID, apiKey):
    url = f'https://www.omdbapi.com/?i={movieID}&plot=full&apikey={apiKey}'

    async with session.get(url, timeout=TIMEOUT) as response:
        response_text = await response.text()
        try:
            data = json.loads(response_text)
            return data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

async def insert_movie_data(movieID, apiKey, session):
    try:
        data = await fetch(session, movieID, apiKey)
        
        if data and data.get("Response") == "True":
            return data
        else:
            return None
    except aiohttp.ClientError as e:
        print(f"Error fetching movie {movieID}: {e}")
        return None, 0

async def insert_batch_of_movies(movie_ids, api_key, session):
    
    tasks = [insert_movie_data(movie_id, api_key, session) for movie_id in movie_ids]
    movie_data_with_times = await asyncio.gather(*tasks)
    
    movies_to_insert = []
    
    for data in movie_data_with_times:
        if data:
            movies_to_insert.append(data)
    
    if movies_to_insert:
        collection.insert_many(movies_to_insert)
    

async def main():
    fromNumber = 500001
    toNumber =   750000  # Adjust to your desired range for testing
    
    session = aiohttp.ClientSession()
    
    try:
        for i in range(fromNumber, toNumber, BATCH_SIZE):
            batch_movie_ids = [f'tt{str(j).zfill(7)}' for j in range(i, min(i + BATCH_SIZE, toNumber))]
            print(f'Making requests for IMDb IDs {i} to {min(i + BATCH_SIZE - 1, toNumber)}...')
            await insert_batch_of_movies(batch_movie_ids, key, session)
        
    
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(main())
