import os


def print_menu_title():
    os.system("cls")
    menu_title_string = "{} My Movies Database {}".format("*"*20, "*"*20)
    print(menu_title_string)


def print_movies_list(movies):
    print_menu_title()
    total_movies = len(movies)
    print_movies_string = f"\n{total_movies} movies in total\n"

    for movie, rating in movies.items():
        print_movies_string += f'"{movie}": {rating}\n'

    print(print_movies_string)

    input("Press enter to continue")




def add_movie(movies_dict: dict):
    pass


def delete_movie():
    pass


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
    menu_string = """ 
Menu:
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
        pass
    elif user_input == "3":
        pass
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

