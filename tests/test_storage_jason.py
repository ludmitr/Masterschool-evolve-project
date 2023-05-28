from storage_json import StorageJson
import pytest
storage = StorageJson('../data.json')
movie_to_add = {"Title": "12 Angry Men",
                "imdbRating": 9.0,
                "Year": 1957,
                "Poster": "https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_SX300.jpg",
                "imdbID": "tt0050083",
                "Country": "United States"}


def test_init():
    with pytest.raises(FileNotFoundError,
                       match="No such file or directory: '../wrong_name.json'"):
        test_storage = StorageJson("../wrong_name.json")


def test_load_data():
    assert isinstance(storage.load_data(), dict), "load_data return dict"


def test_delete_movie():
    movie_title = "12 Angry Men"
    storage.delete_movie(movie_title)
    assert movie_title not in storage.load_data(), "check if movie not in db"


def test_add_movie():
    storage.add_movie(movie_to_add)
    assert movie_to_add["Title"] in storage.load_data()


def test_update_movie():
    movie_name = "12 Angry Men"
    note = "i liked it"
    storage.update_movie(movie_name, note)
    db = storage.load_data()
    assert db[movie_name]["note"] == "i liked it"




pytest.main()