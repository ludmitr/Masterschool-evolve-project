"""
This module defines an abstract base class (ABC) that serves as an interface
for various storage types in a movie management system. The main purpose of this
module is to ensure all storage types have a consistent interface.
"""
from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    abstract base class that defines a generic interface for movie storage.
    """

    @abstractmethod
    def load_data(self) -> dict:
        """
        Abstract method that load all the movies in the storage.

        This method should be overridden by concrete implementations.

        :return
            dict
            For example, the function may return:
            {
              "Titanic": {
                "rating": 9,
                "year": 1999
              },
              "...": {
                ...
              },
            }"""
        pass

    @abstractmethod
    def add_movie(self, data: dict) -> None:
        """
        Abstract method that adds a movie to the storage.
        This method should be overridden by concrete implementations

        :param
            data: dict
            example:
            {
                "Title": "The Godfather",
                "rating": 9.2,
                "year": 1972,
                "image": "https://m.media-amazon.com/images/M/MV....
                "imdb_id": "tt0068646",
                "country": "United States"
            }
        """
        pass

    @abstractmethod
    def delete_movie(self, title: str) -> None:
        """
        Abstract method that removes a movie from the storage.
        This method should be overridden by concrete implementations.
        :param
            title (str): The title of the movie to be deleted.
        """
        pass

    @abstractmethod
    def update_movie(self, title: str, note: str) -> None:
        """
        Abstract method that updates the notes of a specific movie in the storage.
        This method should be overridden by concrete implementations.
        :param
            title (str): The title of the movie to be updated.
            notes (str): The new notes for the movie.
        """
        pass
