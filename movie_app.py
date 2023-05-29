import statistics

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

    def _command_list_movies(self) -> None:
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

    def _add_movie_screen(self) -> None:
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

    def _delete_movie_screen(self):
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

    def _update_movie_screen(self) -> None:
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

    def print_stats_screen(self) -> None:
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

    def run(self):
        pass
      # Print menu
      # Get use command
      # Execute command

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

    def _user_input_press_enter_to_continue(self) -> None:
        """user input to continue with color"""
        input(Fore.LIGHTBLUE_EX + "\nPress enter to continue" + Fore.RESET)

    def _user_input_text(self, text: str) -> str:
        """Asking user for an input in color, returns string"""
        return input(Fore.BLUE + text + Fore.RESET)

    def _error_text_red_color(self, text: str) -> str:
        """Returns colored string for an error message"""
        return Fore.RED + text + Fore.RESET
