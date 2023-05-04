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


def add_movie(title: str, year: int, rating: float, image_url):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies: dict = load_data()
    movies[title] = {"rating": rating, "year": year, "image": image_url}

    save_data(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    if title in movies:
        del movies[title]

    save_data(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = load_data()
    movies[title]["rating"] = rating

    save_data(movies)


def save_data(movies: dict):
    """Serialize the movies data in data.json"""
    with open(FILE_PATH, "w") as file:
        file.write(json.dumps(movies))
