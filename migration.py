import pymongo
import pymysql
from pymongo import MongoClient

# MongoDB connection details
mongo_client = MongoClient('mongodb://127.0.0.1:27017/')
mongo_db = mongo_client['movie_database']
mongo_collection = mongo_db['movies']

# MySQL connection details
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = 'Un13buvdsm'
mysql_db = 'mrs'

# Connect to MySQL
mysql_conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db)
mysql_cursor = mysql_conn.cursor()

# Query MongoDB and insert records into MySQL
mongo_data = mongo_collection.find({
    'imdbVotes': {'$not': {'$eq': 'N/A'}},
    'year': {'$not': {'$eq': 'None'}},
    'imdbRating': {'$not': {'$eq': 'N/A'}}
}, {'_id': 0, 'imdbID': 1, 'Title': 1, 'Year': 1, 'Genre': 1, 'Director': 1, 'Writer': 1, 'Actors': 1, 'Plot': 1, 'Language': 1, 'Poster': 1, 'imdbVotes': 1, 'imdbRating': 1})

for document in mongo_data:
    # Convert 'imdbVotes' and 'imdbRating' to numeric types
    try:
        document['imdbVotes'] = int(document['imdbVotes'])
        document['imdbRating'] = float(document['imdbRating'])
        document['Year'] = int(document['Year'])

    except ValueError:
        print(f"Skipping row with invalid imdbVotes or imdbRating: {document}")
        continue
    
    # Convert MongoDB imdbID to string for insertion into MySQL
    imdbID = str(document['imdbID'])

    # Exclude the 'imdbID' field from columns
    columns = ['imdbid', 'Title', 'Year', 'Genre', 'Director', 'Writer', 'Actors', 'Plot', 'Language', 'Poster', 'imdbVotes', 'imdbRating']
    values = [imdbID] + [document.get(column, None) for column in columns[1:]]

    # Escape special characters in values using parameterized queries
    values = [str(value) for value in values]

    # Create the placeholders for the query string
    placeholders = ', '.join(['%s'] * len(columns[1:]))

    # Construct the query string
    query = f"INSERT INTO dashboard_content (imdbid, {', '.join(columns[1:])}) VALUES (%s, {placeholders})"

    # Execute the query
    mysql_cursor.execute(query, values)

# Commit and close connections
mysql_conn.commit()
mysql_conn.close()
mongo_client.close()
