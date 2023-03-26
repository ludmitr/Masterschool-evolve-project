import os
import random
import statistics
import sys
import numpy as np
from matplotlib import pyplot as plt
from fuzzywuzzy import fuzz
from colorama import Fore
my_os = sys.platform


def main():
    movies = {
        "The Shawshank Redemption": 9.5,
        "Pulp Fiction": 8.8,
        "The Room": 3.6,
        "The Godfather": 9.2,
        "The Godfather: Part II": 9.0,
        "The Dark Knight": 9.0,
        "12 Angry Men": 8.9,
        "Everything Everywhere All At Once": 8.9,
        "Forrest Gump": 8.8,
        "Star Wars: Episode V": 8.7
    }
    while True:
        print_menu()
        user_input = input(Fore.LIGHTBLUE_EX + "Enter choice (1-8): " + Fore.RESET)
        execute_user_input(user_input, movies)


def execute_user_input(user_input, movies):
    menu_functions_dict = {
        "1": print_movies_list,
        "2": add_movie_screen,
        "3": delete_movie_screen,
        "4": update_movie_screen,
        "5": print_stats_screen,
        "6": print_random_movie_screen,
        "7": search_movie_by_name_screen,
        "8": print_sorted_movies_by_rating_screen,
        "9": create_histogram_in_file_screen
    }

    if user_input in menu_functions_dict:
        menu_functions_dict[user_input](movies)


def user_input_text(text: str) -> str:
    return input(Fore.BLUE + text + Fore.RESET)


def error_text_red_color(text: str) -> str:
    return Fore.RED + text + Fore.RESET


def print_clear_screen_and_menu_title():
    clear_command = "cls"
    if my_os in ["darwin", "linux"]:
        clear_command = "clear"
    os.system(clear_command)
    menu_title_string = Fore.LIGHTBLUE_EX + "{} My Movies Database {}\n".format("|"*15, "|"*15) + Fore.RESET
    print(menu_title_string)


def search_movie_by_part_name(movies: dict, part_of_name: str) -> dict:
    part_of_name = part_of_name.lower()
    # if part_of_name in key of movies, adding it element to found_movies_dict
    found_movies_dict = {key: value for key, value in movies.items() if part_of_name in key.lower()}
    return found_movies_dict


def add_movie_to_dict(movies: dict, movie_name: str, movie_rating: str):
    movie_rating_float = float(movie_rating)
    movies[movie_name] = round(movie_rating_float, 1)


def is_movie_rating_valid(rank: str) -> bool:
    try:
        rank_float = float(rank)
        if 0 <= rank_float <= 10:
            return True
        else:
            return False
    except ValueError:
        return False


def user_input_press_enter_to_continue():
    input(Fore.LIGHTBLUE_EX + "\nPress enter to continue" + Fore.RESET)


def print_movies_list(movies):
    print_clear_screen_and_menu_title()
    total_movies = len(movies)
    print_movies_string = f"{total_movies} movies in total\n"
    print_movies_string += "\n".join([f'"{movie}": {rating}' for movie, rating in movies.items()])
    print_movies_string += "\n"
    print(print_movies_string)

    user_input_press_enter_to_continue()


def add_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_name = user_input_text("Enter a new movie name: ")
    input_movie_rating = user_input_text("Enter new movie rating: ")

    print_clear_screen_and_menu_title()
    if is_movie_rating_valid(input_movie_rating):
        add_movie_to_dict(movies, input_movie_name, input_movie_rating)
        print(f"Movie {input_movie_name} successfully added")
    else:
        print(error_text_red_color(f"Rating {input_movie_rating} is invalid"))

    user_input_press_enter_to_continue()


def delete_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_to_delete = user_input_text("Enter movie name to delete: ")
    print_clear_screen_and_menu_title()
    if input_movie_to_delete in movies:
        del movies[input_movie_to_delete]
        message_to_print = f"Movie {input_movie_to_delete} successfully deleted"
    else:
        message_to_print = error_text_red_color(f"Movie {input_movie_to_delete} doesn't exist!")

    print_clear_screen_and_menu_title()
    print(message_to_print)
    user_input_press_enter_to_continue()


def update_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_name = user_input_text("Enter movie name: ")

    if input_movie_name in movies:
        input_movie_rating = user_input_text("Enter new movie rating (0-10): ")
        if is_movie_rating_valid(input_movie_rating):
            add_movie_to_dict(movies, input_movie_name, input_movie_rating)
            print_clear_screen_and_menu_title()
            print(f"Movie {input_movie_name} successfully updated")
        else:
            print_clear_screen_and_menu_title()
            print(error_text_red_color(f"Rating {input_movie_rating} is invalid"))
    else:
        print_clear_screen_and_menu_title()
        print(error_text_red_color(f"Movie {input_movie_name} doesn't exist!"))

    user_input_press_enter_to_continue()


def print_stats_screen(movies: dict):
    average_rating = round(sum(movies.values()) / len(movies), 1)
    median_rating = round(statistics.median(movies.values()), 1)
    best_movie_name = max(movies, key=movies.get)
    worst_movie_name = min(movies, key=movies.get)

    stats_string = """Average rating: {}
Median rating: {}
Best movie: {}, {}
Worst movie: {}, {}""".format(
        average_rating,
        median_rating,
        best_movie_name,
        movies[best_movie_name],
        worst_movie_name,
        movies[worst_movie_name])

    print_clear_screen_and_menu_title()
    print(stats_string)
    user_input_press_enter_to_continue()


def print_random_movie_screen(movies: dict):
    random_movie_name = random.choice(list(movies.keys()))
    print_clear_screen_and_menu_title()
    print(f"Your movie for tonight: {random_movie_name}, it's rated {movies[random_movie_name]}")
    user_input_press_enter_to_continue()


def search_movie_by_fuzzy_matching(movies: dict, input_movie_name: str) -> list:
    approved_matching_score = 65
    # creating list of movies that their matching score is 65+. iterating on a dictionary movies
    matched_movies = [name for name in movies if
                      fuzz.partial_ratio(input_movie_name.lower(), name.lower()) > approved_matching_score]
    return matched_movies


def search_movie_by_name_screen(movies: dict):
    print_clear_screen_and_menu_title()

    input_movie_name = user_input_text("Enter part of movie name: ")
    found_movies_part_name = search_movie_by_part_name(movies, input_movie_name)
    print_result = ""
    if len(found_movies_part_name) > 0:
        for movie, rating in found_movies_part_name.items():
            print_result += f"{movie}, {rating}\n"
        print_result = print_result.rstrip()  # removing last \n
    else:
        found_movies_fuzzy_matching = search_movie_by_fuzzy_matching(movies, input_movie_name)
        print_result = error_text_red_color(f"The movie '{input_movie_name}' does not exist.")
        if len(found_movies_fuzzy_matching) > 0:
            print_result += " Did you mean?\n"
            for movie in found_movies_fuzzy_matching:
                print_result += f"-{movie}\n"
            print_result = print_result.rstrip()    # removing \n in the end
    print_clear_screen_and_menu_title()
    print(print_result)
    user_input_press_enter_to_continue()


def sort_movies_by_rating(movies) -> dict:
    sorted_dict = dict(sorted(movies.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


def print_sorted_movies_by_rating_screen(movies: dict):
    ordered_movies_by_rating = sort_movies_by_rating(movies)
    print_result = ""
    for movie, rating in ordered_movies_by_rating.items():
        print_result += f"{movie}: {rating}\n"
    print_result = print_result.rstrip()  # remove last \n

    print_clear_screen_and_menu_title()
    print(print_result)
    user_input_press_enter_to_continue()


def print_menu():
    print_clear_screen_and_menu_title()
    menu = Fore.RED + "\033[4m" + "menu:" + "\033[0m" + Fore.RESET
    menu_string = f"""{menu}
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Create Rating Histogram
"""
    print(menu_string)


def create_and_save_histogram(movies, input_file_name):
    movies_np = np.array(list(movies.values()))
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.hist(movies_np, bins=[0, 1, 2, 3, 4, 5, 6.5, 7.5, 8, 8.5, 9, 10])

    plt.savefig(input_file_name + ".png")


def create_histogram_in_file_screen(movies):
    print_clear_screen_and_menu_title()

    input_file_name = user_input_text("Name the file to save histogram: ")
    create_and_save_histogram(movies, input_file_name)

    print_clear_screen_and_menu_title()
    print(f"Histogram saved in file named {input_file_name}")
    user_input_press_enter_to_continue()


if __name__ == '__main__':
    main()
