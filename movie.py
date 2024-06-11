from typing import List
from typing import Any
from dataclasses import dataclass
import json
@dataclass
class Rating:
    Source: str
    Value: str

    @staticmethod
    def from_dict(obj: Any) -> 'Rating':
        _Source = str(obj.get("Source"))
        _Value = str(obj.get("Value"))
        return Rating(_Source, _Value)

@dataclass
class Movie:
    Title: str
    Year: str
    Rated: str
    Released: str
    Runtime: str
    Genre: str
    Director: str
    Writer: str
    Actors: str
    Plot: str
    Language: str
    Country: str
    Awards: str
    Poster: str
    Ratings: List[Rating]
    Metascore: str
    imdbRating: str
    imdbVotes: str
    imdbID: str
    Type: str
    DVD: str
    BoxOffice: str
    Production: str
    Website: str
    Response: str

    @staticmethod
    def from_dict(obj: Any) -> 'Movie':
        _Title = str(obj.get("Title"))
        _Year = str(obj.get("Year"))
        _Rated = str(obj.get("Rated"))
        _Released = str(obj.get("Released"))
        _Runtime = str(obj.get("Runtime"))
        _Genre = str(obj.get("Genre"))
        _Director = str(obj.get("Director"))
        _Writer = str(obj.get("Writer"))
        _Actors = str(obj.get("Actors"))
        _Plot = str(obj.get("Plot"))
        _Language = str(obj.get("Language"))
        _Country = str(obj.get("Country"))
        _Awards = str(obj.get("Awards"))
        _Poster = str(obj.get("Poster"))
        _Ratings = [Rating.from_dict(y) for y in obj.get("Ratings")]
        _Metascore = str(obj.get("Metascore"))
        _imdbRating = str(obj.get("imdbRating"))
        _imdbVotes = str(obj.get("imdbVotes"))
        _imdbID = str(obj.get("imdbID"))
        _Type = str(obj.get("Type"))
        _DVD = str(obj.get("DVD"))
        _BoxOffice = str(obj.get("BoxOffice"))
        _Production = str(obj.get("Production"))
        _Website = str(obj.get("Website"))
        _Response = str(obj.get("Response"))
        return Movie(_Title, _Year, _Rated, _Released, _Runtime, _Genre, _Director, _Writer, _Actors, _Plot, _Language, _Country, _Awards, _Poster, _Ratings, _Metascore, _imdbRating, _imdbVotes, _imdbID, _Type, _DVD, _BoxOffice, _Production, _Website, _Response)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# Movie = Movie.from_dict(jsonstring)
