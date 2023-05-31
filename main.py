from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import sys
import os


def main():
    """ The main() function is the primary entry point for running the
    application. Its role is to check if any command-line arguments are
    provided to specify the file name and storage type (either CSV or JSON).
    If no arguments are specified, the function defaults to JSON storage using
    a file named 'data'
    """
    # Default values
    file_name = "data"
    file_ext = "json"

    # checking for command line args
    if len(sys.argv) > 1:
        temp_name, file_ext = os.path.splitext(sys.argv[1])
        file_name = temp_name if file_ext in [".csv", ".json"] else file_name

    storage = (StorageCsv if file_ext == "csv" else StorageJson)(file_name)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == '__main__':
    main()
