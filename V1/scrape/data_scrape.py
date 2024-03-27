import requests
from bs4 import BeautifulSoup
import re
import custom_functions as cf

urls = ["https://myanimelist.net/topanime.php", "https://myanimelist.net/topanime.php?limit=50"]

name = []
episodes = []
airing = []
members = []
ratings = []
timespans = []

def scrape_data(url):
    response = requests.get(url)

    # Parse the HTML content of the repository webpage
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract anime details
    details = soup.find_all('div', attrs={'class': 'detail'})

    # Extract raw ratings
    raw_ratings_9 = soup.find_all('span', attrs={'class': "text on score-label score-9"})
    raw_ratings_8 = soup.find_all('span', attrs={'class': "text on score-label score-8"})
    raw_ratings = raw_ratings_9 + raw_ratings_8

    # Regex pattern to remove characters for episodes & members
    remove_characters = r'\d+|\?'

    for detail in details:
        # Extract anime name
        anime_name = detail.find('a', attrs={'hoverinfo_trigger'})
        if anime_name:
            name.append(anime_name.text.strip())

        # Extract anime information
        info = detail.find('div', class_='information di-ib mt4')
        if info:
            info_lines = info.get_text('\n').strip().split('\n')
            # Extract and clean episodes
            clean_episodes = ''.join(re.findall(remove_characters, info_lines[0]))
            episodes.append(clean_episodes)
            # Extract airing
            airing.append(info_lines[2])
            # Extract and clean members
            clean_members = ''.join(re.findall(remove_characters, info_lines[4]))
            members.append(clean_members)

    # Extract ratings
    for span in raw_ratings:
        # Extract the text content, cast it to float, and append it to the ratings list
        rating = float(span.text.strip())  # Remove leading and trailing whitespace, and cast to float
        ratings.append(rating)

for url in urls:
    scrape_data(url)


for date in airing:
    # Calculate the timespan for each airing date
    timespan = cf.calculate_timespan(date)
    
    # Append the timespan to the list
    timespans.append(timespan)

