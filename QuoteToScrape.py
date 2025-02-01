from bs4 import BeautifulSoup
import requests
import json

root = "https://quotes.toscrape.com"
url = "https://quotes.toscrape.com"

quotes_data = []

while True:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    quotes = soup.find_all("span", attrs={"class": "text"})
    authors = soup.find_all("small", attrs={"class": "author"})

    for quote, author in zip(quotes, authors):
        quote_text = quote.text.strip().encode("ascii", "ignore").decode('utf-8')
        author_name = author.text.strip().encode("ascii", "ignore").decode('utf-8')
        quotes_data.append({"quote": quote_text, "author": author_name})

    atag = soup.find("li", class_="next")
    if atag is None:
        print("No more 'Next' link found. Stopping the scraping process.")
        break

    href = atag.find("a").get("href")
    url = f"https://quotes.toscrape.com{href}"



with open("quotes_data.json", "w") as json_file:
    json.dump(quotes_data, json_file, indent=4)

print("Scraped data saved to quotes_data.json.")