import movie_storage
import os

NEW_WEB_PATH = os.path.join("_static", "index.html")
TEMPLATE_PATH = os.path.join("_static", "index_template.html")
TITLE_NAME = "Dima's Project Movie App"
IMDB_PATH = "https://www.imdb.com/title/"


def load_template() -> str:
    """return html template"""
    with open(TEMPLATE_PATH, "r") as file:
        return file.read()


def save_website(web_page: str) -> None:
    """saves generated web"""
    with open(NEW_WEB_PATH, "w") as file:
        file.write(web_page)


def generate_web() -> None:
    """Generate webpage index.html that representing movies data"""
    movies: dict = movie_storage.load_data()
    generated_web = load_template().replace("__TEMPLATE_TITLE__", TITLE_NAME)

    # generate html representation of movies
    generated_movies_html = ""
    for movie, data in movies.items():
        # year, image_url, = data["year"], data["image"]
        # note, rating = data.get("note", ""), data["rating"]
        # imdb_path = IMDB_PATH + data["imdbID"]
        generated_movies_html += generate_movie(movie, data)

    generated_web = generated_web.replace("__TEMPLATE_MOVIE_GRID__", generated_movies_html)
    save_website(generated_web)


def generate_movie(movie_title, data) -> str:
    """generate html for movie"""
    movie_html = "<li>\n"
    movie_html += "<div class ='movie'>\n"
    movie_html += f"<a href={IMDB_PATH + data['imdb_id']} target='_blank'>"
    movie_html += f"<img class='movie-poster' src='{data['image']}' title='{data.get('note','')}'/>\n"
    movie_html += f"</a>"
    movie_html += f"<div class='imdb'><em>IMDb:</em> {data['rating']}</div>\n"
    movie_html += f"<div class='movie-title'>{movie_title}</div>\n"
    movie_html += f"<div class='movie-year'>{data['year']}</div>\n"
    movie_html += "</div>\n"
    movie_html += "</li>\n"

    return movie_html
