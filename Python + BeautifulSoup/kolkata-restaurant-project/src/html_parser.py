
from bs4 import BeautifulSoup

def parse_restaurant_html(html):

    soup = BeautifulSoup(html, "lxml")

    restaurant = {}

    # Adapt these selectors to the authorized
    # provider's documented HTML structure.

    name = soup.select_one(
        "[data-field='restaurant-name']"
    )

    cuisine = soup.select_one(
        "[data-field='cuisine']"
    )

    rating = soup.select_one(
        "[data-field='rating']"
    )

    cost = soup.select_one(
        "[data-field='cost-for-two']"
    )

    address = soup.select_one(
        "[data-field='address']"
    )

    restaurant["restaurant_name"] = (
        name.get_text(" ", strip=True)
        if name else None
    )

    restaurant["cuisine"] = (
        cuisine.get_text(" ", strip=True)
        if cuisine else None
    )

    restaurant["ratings"] = (
        rating.get_text(" ", strip=True)
        if rating else None
    )

    restaurant["cost_for_two"] = (
        cost.get_text(" ", strip=True)
        if cost else None
    )

    restaurant["address"] = (
        address.get_text(" ", strip=True)
        if address else None
    )

    return restaurant
