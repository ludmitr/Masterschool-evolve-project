import csv
from istorage import IStorage
import os


class StorageCsv(IStorage):
    """
    This class provides implementation for the IStorage interface.
    It manages and interacts with a movie database stored in a CSV file.
    This class supports operations such as adding, deleting, updating,
    and loading movie data. It validates the CSV file path during
    initialization - if file with that name does not exist
    will create a new one.
    """
    _HEADERS = ["Movie Name", "Data"]

    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        """Sets the file path for the object, checking if the path exists.
        Create file_path."""
        file_path += ".csv"
        if os.path.exists(file_path):
            self._file_path = file_path
        else:
            with open(file_path, "w") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(StorageCsv._HEADERS)
        self._file_path = file_path

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
        movies_from_db = {}

        with open(self._file_path, "r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # skipping headers

            for row in reader:
                if row:
                    movie_name = row[0]
                    movie_data = eval(row[1])
                    movies_from_db[movie_name] = movie_data

        return movies_from_db

    def _save_data(self, movies: dict) -> None:
        """Serialize the movies dict in json file"""
        with open(self._file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(StorageCsv._HEADERS)

            for movie, movie_data in movies.items():
                row = [movie, movie_data]
                writer.writerow(row)

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
        Loads the information from the csv file, deletes the movie,
        and saves it. """
        movies = self.load_data()
        if title in movies:
            del movies[title]

        self._save_data(movies)

    def update_movie(self, title: str, note: str) -> None:
        """
        Updates a movie from the movie's database.
        Loads a dict from the CSV file, updates the movie in dict,
        and saves it.
        """
        movies = self.load_data()
        movies[title]["note"] = note

        self._save_data(movies)
