import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from datetime import datetime
import dateparser
import time
import dotenv
import os
from discord_webhook import DiscordWebhook


# Make a GET request to the webpage
url = "https://www.shakingcolors.com/"

# Charger les variables d'environnement à partir du fichier .env
dotenv.load_dotenv(".env")

# Accéder à la variable d'environnement WEBHOOK_URL
webhook_url = os.getenv("WEBHOOK_URL")

most_recent_date = datetime.min

while True :
    # Initialize variables to store the most recent article and its publication date
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the article elements on the page
    article_elements = soup.find_all(class_="card")

    most_recent_article = None
    new_article_found = False
        
    # Iterate over the article elements and find the most recent article
    for article_element in article_elements:
        # Extract the publication date of the article (replace with your own logic)
        publication_date_element = article_element.find("div", class_="card__data")
        publication_date = dateparser.parse(publication_date_element.text.strip())
        
        
        # Compare the publication date with the current most recent date
        if  publication_date > most_recent_date:
            most_recent_article = article_element
            most_recent_date = publication_date
            new_article_found = True

    if new_article_found:
        print("New article found published on ", most_recent_date)
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
        translator = Translator()
        print("translating article...")
        translated_article = translator.translate(article_content,dest="fr")

        # Write the translated article to a file
        with open("translated_article.txt", "w", encoding="utf-8") as file:
            file.write(translated_article.text)
        print("translated article written to file")
        
        # Read the content of the file
        #with open("translated_article.txt", "r", encoding="utf-8") as file:
            #file_content = file.read()

        # Send a Discord notification using the webhook and include the file content
        webhook = DiscordWebhook(url=webhook_url, content=f"New article found published on {most_recent_date}")
        #webhook.add_file(file=bytes(file_content, "utf-8"), filename="translated_article.txt")
        webhook.execute()

    else:
        print("No new article found today. The last article was published on ", most_recent_date)
        
