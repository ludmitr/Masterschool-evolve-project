import movie_storage


NEW_WEB_PATH = "_staitc/index.html"
TEMPLATE_PATH = "_staitc/index_template.html"
TITLE_NAME = "Dima's Project Movie App"

def load_template() -> str:
    """return html template"""
    with open(TEMPLATE_PATH, "r") as file:
        return file.read()


def save_website(web_page: str):
    """saves generated web"""
    with open(NEW_WEB_PATH, "w") as file:
        file.write(web_page)


def generate_web():
    """Generate webpage index.html that representing movies data"""
    movies: dict = movie_storage.load_data()
    generated_web = load_template().replace("__TEMPLATE_TITLE__",TITLE_NAME)

    # generate html representation of movies
    generated_movies = ""
    for movie, data in movies.items():
        rating, year, image_url = data["rating"], data["year"], data["image"]
        generated_movies += generate_movie(movie, rating, year, image_url)

    generated_web = generated_web.replace("__TEMPLATE_MOVIE_GRID__", generated_movies)
    save_website(generated_web)


def generate_movie(movie_title: str, rating, year, image_url) -> str:
    """generate html for movie"""
    movie_html = "<li>\n"
    movie_html += "<div class ='movie'>\n"
    movie_html += f"<img class='movie-poster' src='{image_url}' title=''/>\n"
    movie_html += f"<div class='movie-title'>{movie_title}</div>\n"
    movie_html += f"<div class='movie-year'>{year}</div>\n"
    movie_html += "</div>\n"
    movie_html += "</li>\n"

    return movie_html
