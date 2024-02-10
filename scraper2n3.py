import wikipediaapi
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_event_on_date(date):
    found = False

    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='TimeTravelPakistan')
    page = wiki_wiki.page('Timeline_of_Pakistani_history')

    if page.exists():
        lines = page.text.split('\n')
        current_year = None
        for line in lines:
            if re.match(r'^\d{4}$', line.strip()):
                current_year = line.strip()
            elif line.startswith(date):
                if re.search(r'\d{4}', line) is None and current_year is not None:
                    event = line.replace(date + ': ', '')
                    print(f"{date} {current_year}: {event}")
                else:
                    print(line)
                found = True

    url = "https://en.wikipedia.org/wiki/Timeline_of_Pakistani_history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = pd.read_html(url)

    for table in tables:
        if 'Date' in table.columns:
            for index, row in table.iterrows():
                if row['Date'] == date:
                    event = re.sub(r'\[\d+\]', '', row['Event']) 
                    print(f"{row['Date']} {row['Year']}: {event}")
                    found = True

    if not found:
        print("No event found for this date.")

date = input("Enter a date (e.g., 18 August): ")
get_event_on_date(date)
