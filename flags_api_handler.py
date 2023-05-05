import pycountry


def get_flag_html_link(country_name: str) -> str:
    """returns country flag picture link"""
    country_name = country_name.split(",")[0]
    country_code = get_country_code(country_name)
    if not country_code and country_name == "Russia":
        country_code = "RU"
    url = f"https://www.countryflagicons.com/FLAT/24/{country_code}.png"
    if country_code:
        return url


def get_country_code(country_name):
    """Returns the ISO 3166-1 alpha-2 country code for the given country name."""
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_2
    except AttributeError:
        return None
