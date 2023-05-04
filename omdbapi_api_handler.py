import requests

API_KEY = "f994fda"

<<<<<<< HEAD

=======
>>>>>>> 05efbd8 (connected my app with omdbapi. implemented new features)
def search_by_title(title: str) -> dict:
    """Search request for movie title. Returns dict with data of found movie"""
    url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={title}"

    try:
        with requests.get(url) as res:
            response = res
        return response.json()
    except requests.exceptions.ConnectionError:
        pass

    return{"Response": "False", "Error": "Problems with connection"}

