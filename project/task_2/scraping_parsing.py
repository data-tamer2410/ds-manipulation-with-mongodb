"""Task 2: Scraping and parsing data from site."""

import json
import requests
from bs4 import BeautifulSoup
from project.task_1.main import parse_error


@parse_error
def parse_data() -> tuple[list[dict], list[dict]]:
    """Parse data from site."""
    url = "http://quotes.toscrape.com"
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "lxml")

    qoutes = []
    authors = []
    for el in soup.find_all("div", class_="quote"):
        tags = [tag.text for tag in el.find_all("a", class_="tag")]
        author = el.find("small", class_="author").text
        quote = el.find("span", class_="text").text
        qoutes.append({"tags": tags, "author": author, "quote": quote})

        about_author_url = f'{url}{el.select("span a[href]")[0]["href"]}'
        about_author_html = requests.get(about_author_url, timeout=10)
        about_author_soup = BeautifulSoup(about_author_html.text, "lxml")
        about_author = about_author_soup.find("div", class_="author-details")
        born_date = about_author.find("p").find("span", class_="author-born-date").text
        born_location = (
            about_author.find("p").find("span", class_="author-born-location").text
        )
        description = about_author.find("div", class_="author-description").text.strip()
        authors.append(
            {
                "fullname": author,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }
        )
    return qoutes, authors


@parse_error
def data_to_json(qoutes: list[dict], authors: list[dict]) -> None:
    """Write data to json."""
    if qoutes and authors:
        with open("./qoutes.json", "w", encoding="utf-8") as file:
            json.dump(qoutes, file, indent=2, ensure_ascii=False)

        with open("./authors.json", "w", encoding="utf-8") as file:
            json.dump(authors, file, indent=2, ensure_ascii=False)
        print("Data saved to json.")
    else:
        print("Data not saved.")


if __name__ == "__main__":
    parsed_qoutes, parsed_authors = parse_data()
    data_to_json(parsed_qoutes, parsed_authors)
