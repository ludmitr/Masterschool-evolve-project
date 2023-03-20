import os


def print_menu_title():
    os.system("cls")
    menu_title_string = "{} My Movies Database {}\n".format("*"*15, "*"*15)
    print(menu_title_string)


def print_movies_list(movies):
    print_menu_title()
    total_movies = len(movies)
    print_movies_string = f"{total_movies} movies in total\n"
    print_movies_string += "\n".join([f'"{movie}": {rating}' for movie, rating in movies.items()])
    print_movies_string += "\n"
    print(print_movies_string)

    input("Press enter to continue")


def add_movie_screen(movies: dict):
    print_menu_title()

    movie_name = input("Enter a new movie name: ")
    movie_rating = input("Enter new movie rating: ")

    grades = "".join([str(num) for num in list(range(0, 11))])

    print_menu_title()
    if movie_rating in grades:
        movies[movie_name] = movie_rating
        print(f"Movie {movie_name} successfully added")
    else:
        print(f"Rating {movie_rating} is invalid")

    input("\nPress enter to continue")


def delete_movie_screen(movies: dict):
    print_menu_title()
    input_movie_to_delete = input("Enter movie name to delete: ")
    print_menu_title()
    message_to_print = ""
    if input_movie_to_delete in movies:
        del movies[input_movie_to_delete]
        message_to_print = "Movie ff successfully deleted"
    else:
        message_to_print = "Movie dd doesn't exist!"

    print_menu_title()
    print(message_to_print)
    input("\nPress enter to continue")


def update_movie():
    pass


def print_stats(movies: dict):
    pass


def print_random_movie(movies: dict):
    pass


def search(movies: dict):
    pass


def print_sorted_movies_by_rating(movies: dict):
    pass


def print_menu():
    print_menu_title()
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
        pass
    elif user_input == "5":
        pass
    elif user_input == "6":
        pass
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

