const axios = require('axios');
const { MongoClient } = require('mongodb');

const key = '84c64481';
const MAX_CONCURRENT_REQUESTS = 100;
const TIMEOUT = 0;
const BATCH_SIZE = 5;

const mongoUrl = 'mongodb://localhost:27017';
const dbName = 'mrs_with_ml';
const collectionName = 'temp';

async function fetch(movieID, apiKey) {
    const url = `http://www.omdbapi.com/?i=${movieID}&plot=full&apikey=${apiKey}`;
    
    try {
        const response = await axios.get(url, { timeout: TIMEOUT });
        return response.data;  // Return the fetched data
    } catch (error) {
        console.error(`Error fetching movie ${movieID}: ${error.message}`);
        return null;
    }
}

async function insertBatchOfMovies(movieIDs, apiKey, client, db) {
    const bulkOps = [];

    for (const movieID of movieIDs) {
        const data = await fetch(movieID, apiKey);  // Wait for fetch to complete
        
        if (data && data.Response === "True") {
            bulkOps.push({
                insertOne: {
                    document: {
                        _id: movieID,  // Assuming movieID is unique and used as _id
                        ...data  // Insert fetched data into document
                    }
                }
            });
        } else {
            console.error(`Failed to fetch data for movie ${movieID}`);
        }
    }

    try {
        const result = await db.collection(collectionName).bulkWrite(bulkOps);
        console.log(`Inserted ${result.insertedCount} documents`);
    } catch (error) {
        console.error(`Error inserting documents: ${error.message}`);
    }
}

async function main() {
    const fromNumber = 561104;
    const toNumber = 800999;
    
    const client = new MongoClient(mongoUrl);
    try {
        await client.connect();
        const db = client.db(dbName);
        
        for (let i = fromNumber; i < toNumber; i += BATCH_SIZE) {
            const batchMovieIDs = Array.from({ length: BATCH_SIZE }, (_, index) => `tt${String(i + index).padStart(7, '0')}`);
            console.log(`Making requests for IMDb IDs ${i} to ${Math.min(i + BATCH_SIZE - 1, toNumber)}...`);
            await insertBatchOfMovies(batchMovieIDs, key, client, db);
        }
    } catch (error) {
        console.error(`Error in main function: ${error.message}`);
    } finally {
        await client.close();
    }
}

main().catch(console.error);
