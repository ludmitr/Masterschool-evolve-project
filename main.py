import os
import random
import statistics
import sys
import numpy as np
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
from colorama import Fore
import movie_storage
import omdbapi_api_handler
import web_generator

MY_OS = sys.platform


def main():
    """
    Main entry point for the program. It prints a menu of options
    for the user to choose from, and executes the corresponding
    functionality based on the user's input.
    """
    # continuously displays the main menu, takes user input, and execute
    while True:
        print_menu()
        user_input = input(Fore.LIGHTBLUE_EX + "Enter choice (0-10): " + Fore.RESET)
        execute_user_input(user_input)


def execute_user_input(user_input: str) -> None:
    """
   This function executes the corresponding functionality based on the user's input.

   :param user_input: The user's input choice.
   :return: None
    """
    menu_functions_dict = {
        "0": exit_program,
        "1": print_movies_list,
        "2": add_movie_screen,
        "3": delete_movie_screen,
        "4": update_movie_screen,
        "5": print_stats_screen,
        "6": print_random_movie_screen,
        "7": search_movie_by_name_screen,
        "8": print_sorted_movies_by_rating_screen,
        "9": create_histogram_in_file_screen,
        "10": generate_website_screen
    }

    if user_input in menu_functions_dict:
        menu_functions_dict[user_input]()


def generate_website_screen():
    """Generate website"""
    print_clear_screen_and_menu_title()

    web_generator.generate_web()
    print("Website was generated successfully")

    user_input_press_enter_to_continue()


def exit_program():
    """prints a message and exits the program"""
    print("BYE!")
    sys.exit()


def user_input_text(text: str) -> str:
    """Asking user for an input in color, returns string"""
    return input(Fore.BLUE + text + Fore.RESET)


def error_text_red_color(text: str) -> str:
    """Returns colored string for an error message"""
    return Fore.RED + text + Fore.RESET


def print_clear_screen_and_menu_title() -> None:
    """clears the console screen and prints the title of the menu for the program"""
    # choosing right command - depend on client OS
    clear_command = "cls"
    if MY_OS in ["darwin", "linux"]:
        clear_command = "clear"

    # clear/reset screen
    os.system(clear_command)

    menu_title_string = (
            Fore.LIGHTBLUE_EX
            + f"{'|' * 15} My Movies Database {'|' * 15}\n"
            + Fore.RESET
    )
    print(menu_title_string)


def search_movie_by_part_name(movies: dict, part_of_name: str) -> dict:
    """
    searches for movies whose names contain a given string as a substring.
    It takes two arguments: movies, which is a dictionary containing movies
    and their data, and part_of_name, which is the string to search for.
    It returns a dictionary containing the movies whose names
    contain part_of_name as a substring.
    """
    part_of_name = part_of_name.lower()

    # if part_of_name in key of movies, adding it element to found_movies_dict
    found_movies_dict = {key: value for key, value in movies.items() if part_of_name in key.lower()}

    return found_movies_dict


def user_input_press_enter_to_continue() -> None:
    """user input to continue with color"""
    input(Fore.LIGHTBLUE_EX + "\nPress enter to continue" + Fore.RESET)


def print_movies_list():
    """
    Prints a list of movies with their ratings and release years.
    It first clears the screen, then prints the movies in a formatted string,
    and waits for the user to press Enter to continue.
    """
    movies = movie_storage.load_data()
    print_clear_screen_and_menu_title()
    total_movies = len(movies)

    # creating string for a print command
    print_movies_string = f"{total_movies} movies in total\n"
    movies_represent_list = [f'"{movie}": {movie_data["rating"]}, year: {movie_data["year"]}'
                             for movie, movie_data in movies.items()]
    print_movies_string += "\n".join(movies_represent_list)
    print_movies_string += "\n"

    print(print_movies_string)
    user_input_press_enter_to_continue()


def add_movie_screen(movie_name: str = None):
    """
    Add a new movie to the movies dictionary with a given name, rating, and year.
    If the input data is invalid, an error message will be displayed
    """
    print_clear_screen_and_menu_title()

    if movie_name:
        input_movie_name = movie_name
    else:
        input_movie_name = user_input_text("Enter a new movie name: ")

    search_result: dict = omdbapi_api_handler.search_by_title(input_movie_name)
    print_clear_screen_and_menu_title()

    # print message depends on result of search
    if search_result["Response"] == "True":
        movie_storage.add_movie(search_result)
        print(f"Movie {search_result['Title']} successfully added/updated")
    else:
        print(error_text_red_color(f"{search_result['Error']}"))

    user_input_press_enter_to_continue()


def delete_movie_screen():
    """
    deletes a movie from the movies dictionary based on user input for
    the movie name.If the movie exists in the dictionary, it will be
    deleted and a success message  will be displayed. If the movie
    does not exist in the dictionary, an error message will be displayed.
    """
    movies = movie_storage.load_data()
    print_clear_screen_and_menu_title()
    input_movie_to_delete = user_input_text("Enter movie name to delete: ")
    print_clear_screen_and_menu_title()

    if input_movie_to_delete in movies:
        movie_storage.delete_movie(input_movie_to_delete)
        message_to_print = f"Movie {input_movie_to_delete} successfully deleted"
    else:
        message_to_print = error_text_red_color(f"Movie {input_movie_to_delete} doesn't exist!")

    print_clear_screen_and_menu_title()
    print(message_to_print)
    user_input_press_enter_to_continue()


def update_movie_screen() -> None:
    """
    Updates the rating of an existing movie in the movie's dictionary.
    If the movie doesn't exist, an error message is displayed
    """
    movies = movie_storage.load_data()
    print_clear_screen_and_menu_title()
    input_movie_name = user_input_text("Enter movie name: ")

    # if movie exist -> update  notes and creates output_string for a menu
    if input_movie_name in movies:
        input_movie_note = user_input_text("Enter movie notes: ")
        movie_storage.update_movie(input_movie_name, input_movie_note)
        print_clear_screen_and_menu_title()
        output_string = f"Movie {input_movie_name} successfully updated"
    else:
        print_clear_screen_and_menu_title()
        output_string = error_text_red_color(f"Movie {input_movie_name} doesn't exist!")

    print(output_string)
    user_input_press_enter_to_continue()


def print_stats_screen() -> None:
    """
    Prints statistics about the movie's database,
    including the average and median ratings,
    and the best and worst rated movies.
    """
    movies = movie_storage.load_data()
    average_rating = round(sum(data["rating"] for data in movies.values()) / len(movies), 1)
    median_rating = round(statistics.median(data["rating"] for data in movies.values()), 1)
    best_movie_name = max(movies, key=lambda movie: movies[movie]["rating"])
    best_movie_data = {"rating": movies[best_movie_name]["rating"],
                       "year": movies[best_movie_name]["year"]}
    worst_movie_name = min(movies, key=lambda movie: movies[movie]["rating"])
    worst_movie_data = {"rating": movies[worst_movie_name]["rating"],
                        "year": movies[worst_movie_name]["year"]}

    stats_string = f"""Average rating: {average_rating}
Median rating: {median_rating}
Best movie: {best_movie_name} {best_movie_data}
Worst movie: {worst_movie_name}, {worst_movie_data}"""

    print_clear_screen_and_menu_title()
    print(stats_string)
    user_input_press_enter_to_continue()


def print_random_movie_screen():
    """Prints a random movie from the database with its rating and year"""
    movies = movie_storage.load_data()
    random_movie_name = random.choice(list(movies.keys()))
    print_clear_screen_and_menu_title()
    random_movie_data = {"rating": movies[random_movie_name]["rating"],
                         "year": movies[random_movie_name]["year"]}
    print(f"Your movie for tonight: {random_movie_name}  {random_movie_data}")
    user_input_press_enter_to_continue()


def search_movie_by_fuzzy_matching(movies: dict, input_movie_name: str) -> list:
    """
    This function searches for movie names in a dictionary using fuzzy matching
    and returns a list of matching movie names.
    """
    approved_matching_score = 65

    # creating list of movies that their matching score is 65+. iterating on a dictionary movies
    matched_movies = [
        name for name in movies
        if fuzz.partial_ratio(input_movie_name.lower(), name.lower()) > approved_matching_score
    ]

    return matched_movies


def create_str_for_found_movies(found_movies_part_name: dict) -> str:
    """create a string that represent found movies and returns it"""
    output_string = ""
    for movie, data in found_movies_part_name.items():
        movie_data = {"rating": data["rating"], "year": data["year"]}
        output_string += f"{movie}, {movie_data}\n"

    return output_string.rstrip()  # removing last \n


def create_str_for_fuzzy_matches(found_movies_fuzzy_matching, input_movie_name) -> str:
    """Creates string that represent matching results for fuzzy search"""
    output_str = ""
    if len(found_movies_fuzzy_matching) > 0:
        output_str += " Did you mean?\n"
        for movie in found_movies_fuzzy_matching:
            output_str += f"-{movie}\n"
        output_str = output_str.rstrip()  # removing \n in the end
    else:
        output_str = error_text_red_color(f"The movie '{input_movie_name}' does not exist.")

    return output_str


def search_movie_by_name_screen():
    """
    Search for a movie by a partial or fuzzy match to its name and displays
    the results to the user. If there is an exact match, it will display the
    movie's rating and year. If there are no exact matches, it will suggest
    fuzzy matches and prompt the user to choose from the suggestions.
    """
    movies = movie_storage.load_data()
    print_clear_screen_and_menu_title()

    input_movie_name = user_input_text("Enter part of movie name: ")
    found_movies_part_name = search_movie_by_part_name(movies, input_movie_name)

    # creating print_result string, depending on the matching result
    if len(found_movies_part_name) > 0:
        print_result = create_str_for_found_movies(found_movies_part_name)
    else:
        found_movies_fuzzy_matching: list = search_movie_by_fuzzy_matching(movies, input_movie_name)
        print_result = create_str_for_fuzzy_matches(found_movies_fuzzy_matching, input_movie_name)

    print_clear_screen_and_menu_title()
    print(print_result)
    user_input_press_enter_to_continue()


def sort_movies_by_rating(movies) -> dict:
    """
        Return new dictionary of movies sorted by rating in descending order
    """
    sorted_dict = dict(sorted(movies.items(),
                              key=lambda movie_data: movie_data[1]['rating'],
                              reverse=True))
    return sorted_dict


def print_sorted_movies_by_rating_screen() -> None:
    """Prints a sorted list of movies by rating on the screen"""
    movies = movie_storage.load_data()
    ordered_movies_by_rating = sort_movies_by_rating(movies)

    print_result = ""
    for movie, data in ordered_movies_by_rating.items():
        print_result += f"{movie}: {data['rating']}\n"
    print_result = print_result.rstrip()  # remove last \n

    print_clear_screen_and_menu_title()
    print(print_result)
    user_input_press_enter_to_continue()


def print_menu():
    """Prints a menu of options for the user to choose from"""
    print_clear_screen_and_menu_title()
    menu = Fore.RED + "\033[4m" + "menu:" + "\033[0m" + Fore.RESET
    menu_string = f"""{menu}
0. Exit    
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram
10.Generate website
"""
    print(menu_string)


def create_and_save_histogram(movies: dict, input_file_name: str) -> None:
    """Creates a histogram of movie ratings and saves it to a file with the input_file_name."""
    movies_np = np.array([movies[movie]["rating"] for movie in movies])
    _, plot_axes = plt.subplots(figsize=(10, 7))
    plot_axes.hist(movies_np, bins=[0, 1, 2, 3, 4, 5, 6.5, 7.5, 8, 8.5, 9, 10])

    plt.savefig(input_file_name + ".png")


def create_histogram_in_file_screen():
    """
    Displays a menu screen with instructions to enter a file name to save the histogram.
    Saves the histogram in a PNG file with the given name in the
    current directory. Displays a message with the name of the file where the histogram
    was saved, and waits for the user to press Enter to continue.
    """
    movies = movie_storage.load_data()
    print_clear_screen_and_menu_title()

    input_file_name = user_input_text("Name the file to save histogram: ")
    create_and_save_histogram(movies, input_file_name)

    print_clear_screen_and_menu_title()
    print(f"Histogram saved in file named {input_file_name}")
    user_input_press_enter_to_continue()


if __name__ == '__main__':
    main()
