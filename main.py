import argparse
from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
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

    # Define the argparse parser
    parser = argparse.ArgumentParser(
        description='This script runs a MovieApp with a specified'
                    ' storage type and file name.')
    parser.add_argument('--file_name', metavar='F', type=str,
                        help='The file name with extension '
                             'example filename.json or filename.csv')

    # Parse the command line arguments
    args = parser.parse_args()

    # If file argument is provided, use it to set file name and extension
    if args.file_name:
        temp_name, file_ext = os.path.splitext(args.file_name)
        file_name = temp_name if file_ext in [".csv", ".json"] else file_name

    # Creating storage and run the app
    storage = (StorageCsv if file_ext == ".csv" else StorageJson)(file_name)
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == '__main__':
    main()
