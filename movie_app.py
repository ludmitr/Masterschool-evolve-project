import random
import statistics

from fuzzywuzzy import fuzz

from istorage import IStorage
import sys
from colorama import Fore
import os
import omdbapi_api_handler



class MovieApp:
    def __init__(self, storage: IStorage):
        self._storage = storage
        # assign clear command for command line depending on OS
        self._clear_command = "clear" if sys.platform in ["darwin",
                                                          "linux"] else "cls"

    def _exit_program(self) -> None:
        """prints a message and exits the program"""
        print("BYE!")
        sys.exit()

    def _list_movies_command(self) -> None:
        """
        Prints a list of movies with their ratings and release years.
        It first clears the screen, then prints the movies in a formatted string,
        and waits for the user to press Enter to continue.
        """
        movies: dict = self._storage.load_data()
        self._print_clear_screen_and_menu_title()
        total_movies = len(movies)

        # creating string for a print command
        print_movies_string = f"{total_movies} movies in total\n"
        movies_represent_list = [
            f'"{movie}": {movie_data["rating"]}, year: {movie_data["year"]}'
            for movie, movie_data in movies.items()]
        print_movies_string += "\n".join(movies_represent_list)
        print_movies_string += "\n"

        print(print_movies_string)
        self._user_input_press_enter_to_continue()

    def _add_movie_command(self) -> None:
        """
        Interactive command-line interface for adding a movie to the database.

        The method first prompts the user to input a movie name. It then searches
        for this movie using the omdbapi API. Depending on the search results, it
        either adds the movie to the database and notifies the user of the
        successful addition, or it displays an error message. Finally, it waits
        for the user to press enter to continue.
        """
        self._print_clear_screen_and_menu_title()

        input_movie_name = self._user_input_text("Enter a new movie name: ")

        # getting search result from omdbapi api
        search_result: dict = omdbapi_api_handler.search_by_title(
            input_movie_name)
        self._print_clear_screen_and_menu_title()

        # print message depends on result of search.if movie found- adding to db
        if search_result["Response"] == "True":
            self._storage.add_movie(search_result)
            print(f"Movie {search_result['Title']} successfully added/updated")
        else:
            print(self._error_text_red_color(f"{search_result['Error']}"))

        self._user_input_press_enter_to_continue()

    def _delete_movie_command(self):
        """
        deletes a movie from the movies dictionary based on user input for
        the movie name.If the movie exists in the dictionary, it will be
        deleted and a success message  will be displayed. If the movie
        does not exist in the dictionary, an error message will be displayed.
        """
        # getting movies from db and asking user to enter a movie to delete
        movies = self._storage.load_data()
        self._print_clear_screen_and_menu_title()
        input_movie_to_delete = self._user_input_text("Enter movie name to delete: ")
        self._print_clear_screen_and_menu_title()

        # Delete movie if it exists in db, else print error message
        if input_movie_to_delete in movies:
            self._storage.delete_movie(input_movie_to_delete)
            message_to_print = f"Movie {input_movie_to_delete} successfully deleted"
        else:
            message_to_print = self._error_text_red_color(
                f"Movie {input_movie_to_delete} doesn't exist!")

        self._print_clear_screen_and_menu_title()
        print(message_to_print)
        self._user_input_press_enter_to_continue()

    def _update_movie_command(self) -> None:
        """
        Command-line interface for updating notes for a specific movie in
        the database.

        The method prompts the user to input a movie name. If the movie is in
        the database, it allows the user to input notes for the movie and
        updates the movie in the database. It then prints a confirmation
        message. If the movie is not found, it displays an error message.
        """
        movies = self._storage.load_data()
        self._print_clear_screen_and_menu_title()
        input_movie_name = self._user_input_text("Enter movie name: ")

        # if movie exist -> update notes and creates output_string for commandL
        if input_movie_name in movies:
            input_movie_note = self._user_input_text("Enter movie notes: ")
            self._storage.update_movie(input_movie_name, input_movie_note)
            self._print_clear_screen_and_menu_title()
            output_string = f"Movie {input_movie_name} successfully updated"
        else:
            self._print_clear_screen_and_menu_title()
            output_string = self._error_text_red_color(
                f"Movie {input_movie_name} doesn't exist!")

        print(output_string)
        self._user_input_press_enter_to_continue()

    def print_stats_command(self) -> None:
        """
        Prints statistics about the movie's database,
        including the average and median ratings,
        and the best and worst rated movies.
        """
        movies = self._storage.load_data()

        # getting statistics data
        average_rating = round(
            sum(data["rating"] for data in movies.values()) / len(movies), 1)
        median_rating = round(
            statistics.median(data["rating"] for data in movies.values()), 1)
        best_movie_name = max(movies,
                              key=lambda movie: movies[movie]["rating"])
        best_movie_data = {"rating": movies[best_movie_name]["rating"],
                           "year": movies[best_movie_name]["year"]}
        worst_movie_name = min(movies,
                               key=lambda movie: movies[movie]["rating"])
        worst_movie_data = {"rating": movies[worst_movie_name]["rating"],
                            "year": movies[worst_movie_name]["year"]}

        # creating output string with statistics data
        stats_string = f"""Average rating: {average_rating}
    Median rating: {median_rating}
    Best movie: {best_movie_name} {best_movie_data}
    Worst movie: {worst_movie_name}, {worst_movie_data}"""

        self._print_clear_screen_and_menu_title()
        print(stats_string)
        self._user_input_press_enter_to_continue()

    def print_random_movie_command(self):
        """Prints a random movie from the database with its rating and year"""
        movies = self._storage.load_data()
        random_movie_name = random.choice(list(movies.keys()))
        self._print_clear_screen_and_menu_title()
        random_movie_data = {"rating": movies[random_movie_name]["rating"],
                             "year": movies[random_movie_name]["year"]}
        print(f"Your movie for tonight: {random_movie_name}  "
              f"{random_movie_data}")
        self._user_input_press_enter_to_continue()

    def search_movie_by_name_command(self):
        """
        Search for a movie by a partial or fuzzy match to its name and displays
        the results to the user. If there is an exact match, it will display the
        movie's rating and year. If there are no exact matches, it will suggest
        fuzzy matches and prompt the user to choose from the suggestions.
        """
        movies = self._storage.load_data()
        self._print_clear_screen_and_menu_title()

        input_movie_name = self._user_input_text("Enter part of movie name: ")
        found_movies_part_name = self._search_movie_by_part_name(movies,
                                                           input_movie_name)

        # creating print_result string, depending on the matching result
        if found_movies_part_name:
            print_result = self._create_str_for_found_movies(found_movies_part_name)
        else:
            found_movies_fuzzy_matching: list = self._search_movie_by_fuzzy_matching(
                movies, input_movie_name)
            print_result = self._create_str_for_fuzzy_matches(
                found_movies_fuzzy_matching, input_movie_name)

        self._print_clear_screen_and_menu_title()
        print(print_result)
        self._user_input_press_enter_to_continue()

    def _sorted_movies_by_rating_command(self) -> None:
        """Prints a sorted list of movies by rating on the screen"""
        movies = self._storage.load_data()
        ordered_movies_by_rating = self._sort_movies_by_rating(movies)

        print_result = ""
        for movie, data in ordered_movies_by_rating.items():
            print_result += f"{movie}: {data['rating']}\n"
        print_result = print_result.rstrip()  # remove last \n

        self._print_clear_screen_and_menu_title()
        print(print_result)
        self._user_input_press_enter_to_continue()

    def _sort_movies_by_rating(self, movies: dict) -> dict:
        """
            Return new dictionary of movies sorted by rating in descending order
        """
        sorted_dict = dict(sorted(movies.items(),
                                  key=lambda movie_data: movie_data[1][
                                      'rating'],
                                  reverse=True))
        return sorted_dict

    def _create_str_for_fuzzy_matches(self, found_movies_fuzzy_matching,
                                      input_movie_name) -> str:
        """Creates string that represent matching results for fuzzy search"""
        output_str = ""
        if len(found_movies_fuzzy_matching) > 0:
            output_str += " Did you mean?\n"
            for movie in found_movies_fuzzy_matching:
                output_str += f"-{movie}\n"
            output_str = output_str.rstrip()  # removing \n in the end
        else:
            output_str = self._error_text_red_color(
                f"The movie '{input_movie_name}' does not exist.")

        return output_str

    def _search_movie_by_fuzzy_matching(self, movies: dict,
                                        input_movie_name: str) -> list:
        """
        This function searches for movie names in a dictionary using fuzzy matching
        and returns a list of matching movie names.
        """
        approved_matching_score = 65

        # creating list of movies that their matching score is 65+.
        matched_movies = [
            name for name in movies
            if fuzz.partial_ratio(input_movie_name.lower(),
                                  name.lower()) > approved_matching_score
        ]

        return matched_movies

    def _create_str_for_found_movies(self, found_movies_part_name: dict) -> str:
        """create a string that represent found movies and returns it"""
        output_string = ""
        for movie, data in found_movies_part_name.items():
            movie_data = {"rating": data["rating"], "year": data["year"]}
            output_string += f"{movie}, {movie_data}\n"

        return output_string.rstrip()  # removing last \n

    def _search_movie_by_part_name(self, movies: dict,
                                   part_of_name: str) -> dict:
        """
        searches for movies whose names contain a given string as a substring.
        It takes two arguments: movies, which is a dictionary containing movies
        and their data, and part_of_name, which is the string to search for.
        It returns a dictionary containing the movies whose names
        contain part_of_name as a substring.
        """
        part_of_name = part_of_name.lower()

        # if part_of_name in key of movies, adding it element to found_movies_dict
        found_movies_dict = {key: value for key, value in movies.items() if
                             part_of_name in key.lower()}

        return found_movies_dict

    def run(self):
        pass
      # Print menu
      # Get use command
      # Execute command


    def _user_input_press_enter_to_continue(self) -> None:
        """user input to continue with color"""
        input(Fore.LIGHTBLUE_EX + "\nPress enter to continue" + Fore.RESET)

    def _user_input_text(self, text: str) -> str:
        """Asking user for an input in color, returns string"""
        return input(Fore.BLUE + text + Fore.RESET)

    def _error_text_red_color(self, text: str) -> str:
        """Returns colored string for an error message"""
        return Fore.RED + text + Fore.RESET

    def _print_clear_screen_and_menu_title(self) -> None:
        """clears the console screen and prints the title of the menu
         for the program"""
        # clear/reset screen
        os.system(self._clear_command)

        menu_title_string = (
                Fore.LIGHTBLUE_EX
                + f"{'|' * 15} My Movies Database {'|' * 15}\n"
                + Fore.RESET
        )
        print(menu_title_string)