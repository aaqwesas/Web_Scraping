import requests
from bs4 import BeautifulSoup
import pandas as pd


data = []

page = 1

while True:
    url = f"https://books.toscrape.com/catalogue/page-{str(page)}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.title.text == "404 Not Found":
        print("All pages have been scraped.")
        break
    else:
        print(f"Scraping page {page}")
        books = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for book in books:
            info = {}

            info["Title"] = book.find("img").attrs["alt"]
            info["Link"] = "https://books.toscrape.com/catalogue/" +  book.find('a').attrs["href"]
            info["Price"] = "$" + book.find("p", class_="price_color").text.strip()[2:]
            info["Stock"] = book.find("p", class_="instock availability").text.strip()
            info["Rating"] = book.find("p", class_="star-rating").attrs["class"][1]
            data.append(info)
        page += 1



df = pd.DataFrame(data)
df.to_csv("books.csv", index=False)
df.to_excel("book.xlsx", index=False)