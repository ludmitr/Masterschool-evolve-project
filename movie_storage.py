import json

FILE_PATH = "data.json"


def load_data():
    """
    Returns a dictionary that contains
    the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open(FILE_PATH, "r") as file:
        return json.loads(file.read())


def add_movie(data) -> None:
    """
    Adds a movie to the movie's database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    title, imdb_id = data["Title"], data["imdbID"]
    year, image_url = int(data["Year"]), data["Poster"]
    rating = float(data["imdbRating"])

    movies = load_data()
    movies[title] = {"rating": rating, "year": year, "image": image_url,
                     "imdb_id": imdb_id, "country": [data["country"]]}

    save_data(movies)


def delete_movie(title: str) -> None:
    """
    Deletes a movie from the movie's database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    if title in movies:
        del movies[title]

    save_data(movies)


def update_movie(title: str, note: str) -> None:
    """
    Updates a movie from the movie's database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    movies[title]["note"] = note

    save_data(movies)


def save_data(movies: dict) -> None:
    """Serialize the movies data in data.json"""
    with open(FILE_PATH, "w") as file:
        file.write(json.dumps(movies))
