import os
from storage_csv import StorageCsv
import csv
import pytest
from movie_app import MovieApp




movie_to_add = {"Title": "12 Angry Men",
                "imdbRating": 9.0,
                "Year": 1957,
                "Poster": "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg",
                "imdbID": "tt0050083",
                "Country": "United States"}

def test_creating_empty_csv():
    storage = StorageCsv("../test")
    with open("../test.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        first_line = next(reader)
    assert first_line[0] == "Movie Name"
    assert first_line[1] == "Data"
    os.remove("../test.csv")

def test_adding_movie():
    storage = StorageCsv("../test2")
    storage.add_movie(movie_to_add)
    assert storage.load_data()["12 Angry Men"]["rating"] == 9
    os.remove("../test2.csv")

def test_file_path_parameter():
    storage = StorageCsv("../test")
    storage.file_path = "../test2"
    assert os.path.exists("../test.csv")
    assert os.path.exists("../test2.csv")
    os.remove("../test.csv")
    os.remove("../test2.csv")

def test_load_data():
    storage = StorageCsv("../test")
    assert isinstance(storage.load_data(), dict)
    os.remove("../test.csv")

def test_delete_movie():
    storage = StorageCsv("../test")
    storage.add_movie(movie_to_add)
    assert "12 Angry Men" in storage.load_data()
    storage.delete_movie("12 Angry Men")
    assert "12 Angry Men" not in storage.load_data()
    os.remove("../test.csv")

def test_update_movie():
    note = "test"
    storage = StorageCsv("../test")
    storage.add_movie(movie_to_add)
    storage.update_movie("12 Angry Men", note)
    assert storage.load_data()["12 Angry Men"]["note"] == note
    os.remove("../test.csv")



pytest.main()
