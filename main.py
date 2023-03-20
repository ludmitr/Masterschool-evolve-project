import os
import random
import statistics
import sys
my_os = sys.platform


def print_clear_screen_and_menu_title():
    clear_command = "cls"
    if my_os in ["darwin", "linux"]:
        clear_command = "clear"
    os.system(clear_command)
    menu_title_string = "{} My Movies Database {}\n".format("*"*15, "*"*15)
    print(menu_title_string)


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


def print_movies_list(movies):
    print_clear_screen_and_menu_title()
    total_movies = len(movies)
    print_movies_string = f"{total_movies} movies in total\n"
    print_movies_string += "\n".join([f'"{movie}": {rating}' for movie, rating in movies.items()])
    print_movies_string += "\n"
    print(print_movies_string)

    input("Press enter to continue")


def add_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_name = input("Enter a new movie name: ")
    input_movie_rating = input("Enter new movie rating: ")

    print_clear_screen_and_menu_title()
    if is_movie_rating_valid(input_movie_rating):
        add_movie_to_dict(movies, input_movie_name, input_movie_rating)
        print(f"Movie {input_movie_name} successfully added")
    else:
        print(f"Rating {input_movie_rating} is invalid")

    input("\nPress enter to continue")


def delete_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_to_delete = input("Enter movie name to delete: ")
    print_clear_screen_and_menu_title()
    message_to_print = ""
    if input_movie_to_delete in movies:
        del movies[input_movie_to_delete]
        message_to_print = f"Movie {input_movie_to_delete} successfully deleted"
    else:
        message_to_print = f"Movie {input_movie_to_delete} doesn't exist!"

    print_clear_screen_and_menu_title()
    print(message_to_print)
    input("\nPress enter to continue")


def update_movie_screen(movies: dict):
    print_clear_screen_and_menu_title()
    input_movie_name = input("Enter movie name: ")

    if input_movie_name in movies:
        input_movie_rating = float(input("Enter new movie rating (0-10): "))
        if is_movie_rating_valid(input_movie_rating):
            add_movie_to_dict(movies, input_movie_name, input_movie_rating)
            print_clear_screen_and_menu_title()
            print(f"Movie {input_movie_name} successfully updated")
        else:
            print_clear_screen_and_menu_title()
            print(f"Rating {input_movie_rating} is invalid")
    else:
        print_clear_screen_and_menu_title()
        print(f"Movie {input_movie_name} doesn't exist!")

    input("\nPress enter to continue")



def print_stats_screen(movies: dict):
    average_rating = round(sum(movies.values()) / len(movies), 1)
    median_rating = round(statistics.median(movies.values()), 1)
    best_movie_name = max(movies, key=movies.get)
    worst_movie_name = min(movies, key=movies.get)

    stats_string ="""Average rating: {}
Median rating: {}
Best movie: {}, {}
Worst movie: {}, {}""".format(average_rating,
           median_rating,
           best_movie_name, movies[best_movie_name],
           worst_movie_name, movies[worst_movie_name])

    print_clear_screen_and_menu_title()
    print(stats_string)
    input("\nPress enter to continue")

def print_random_movie(movies: dict):
    random_movie_name = random.choice(list(movies.keys()))
    print_clear_screen_and_menu_title()
    print(f"Your movie for tonight: {random_movie_name}, it's rated {movies[random_movie_name]}")
    input("\nPress enter to continue")

def search(movies: dict):
    pass


def print_sorted_movies_by_rating(movies: dict):
    pass


def print_menu():
    print_clear_screen_and_menu_title()
    menu_string = """Menu:
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
"""
    print(menu_string)


def execute_user_input(user_input, movies):
    if user_input == "1":
        print_movies_list(movies)
    elif user_input == "2":
        add_movie_screen(movies)
    elif user_input == "3":
        delete_movie_screen(movies)
    elif user_input == "4":
        update_movie_screen(movies)
    elif user_input == "5":
        print_stats_screen(movies)
    elif user_input == "6":
        print_random_movie(movies)
    elif user_input == "7":
        pass
    elif user_input == "8":
        pass



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
        user_input = input("Enter choice (1-8): ")
        execute_user_input(user_input, movies)


if __name__ == '__main__':
    main()

