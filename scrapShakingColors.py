import requests
from bs4 import BeautifulSoup
from translate import Translator
from datetime import datetime
import dateparser

# Make a GET request to the webpage
url = "https://www.shakingcolors.com/"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the article elements on the page
article_elements = soup.find_all(class_="card")

# Initialize variables to store the most recent article and its publication date
most_recent_article = None
most_recent_date = None

# Iterate over the article elements and find the most recent article
for article_element in article_elements:
    # Extract the publication date of the article (replace with your own logic)
    publication_date_element = article_element.find("div", class_="card__data")
    publication_date = dateparser.parse(publication_date_element.text.strip())

    # Compare the publication date with the current most recent date
    if most_recent_date is None or publication_date > most_recent_date:
        most_recent_article = article_element
        most_recent_date = publication_date

# Extract the link to the full article
article_link = most_recent_article.find("a")["href"]

# Make a GET request to the full article page
full_article_response = requests.get(article_link)

# Parse the HTML content of the full article page
full_article_soup = BeautifulSoup(full_article_response.content, "html.parser")

# Find the content of the full article (replace with your own logic)
full_article_content = full_article_soup.find("div", class_="single-post__body")

article_content = str(full_article_content)

# Translate the article to French using googletrans
translator = Translator(to_lang="fr")
translated_article = translator.translate(article_content)

# Write the translated article to a file
with open("translated_article.txt", "w") as file:
    file.write(translated_article)
