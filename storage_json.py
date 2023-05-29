"""
storage_json.py
This module provides a StorageJson class implementing the IStorage interface.
It manages a movie database stored in a JSON file.

This module is designed for flexible movie data handling, providing a
user-friendly :D interface for managing a movie database.
It supports adding, deleting, updating, and loading movie data from a JSON file.
"""
from istorage import IStorage
import json
import os

class StorageJson(IStorage):
    """
    StorageJson class provides implementation for the IStorage interface.
    It manages and interacts with a movie database stored in a JSON file.
    This class supports operations such as adding, deleting, updating,
    and loading movie data. It validates the JSON file path during
    initialization and raises a FileNotFoundError if the file does not exist.
    """
    def __init__(self, file_path):
        self.file_path = file_path


    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, path):
        if os.path.exists(path):
            self._file_path = path
        else:
            raise FileNotFoundError(f"No such file or directory: '{path}'")


    def _save_data(self, movies: dict) -> None:
        """Serialize the movies data in data.json"""
        with open(self._file_path, "w") as file:
            file.write(json.dumps(movies))

    def load_data(self) -> dict:
        """
        Returns a dictionary that contains
        the movies information from the database.

        The function loads the information from the JSON
        file and returns the data.

        :return dict
            For example, the function will return:
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
        with open(self._file_path, "r") as file:
            return json.loads(file.read())

    def add_movie(self, data: dict) -> None:
        """Adds a movie to the movie's database."""
        title, imdb_id = data["Title"], data["imdbID"]
        year, image_url = int(data["Year"]), data["Poster"]
        rating, country = float(data["imdbRating"]), data["Country"]

        # loading data
        movies: dict = self.load_data()

        # updating data
        movies[title] = {"rating": rating, "year": year, "image": image_url,
                         "imdb_id": imdb_id, "country": country}

        self._save_data(movies)

    def delete_movie(self, title: str) -> None:
        """
        Deletes a movie from the movie's database.
        Loads the information from the JSON file, deletes the movie,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.load_data()
        if title in movies:
            del movies[title]

        self._save_data(movies)

    def update_movie(self, title: str, note: str) -> None:
        """
        Updates a movie from the movie's database.
        Loads a dict from the JSON file, updates the movie in dict,
        and saves it. The function doesn't need to validate the input.
        """
        movies = self.load_data()
        movies[title]["note"] = note

        self._save_data(movies)
