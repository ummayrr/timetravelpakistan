import wikipediaapi
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_event_on_date_from_text(date):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='TimeTravelPakistan')
    page = wiki_wiki.page('Timeline_of_Pakistani_history')

    if not page.exists():
        print("Page not found")
        return None

    lines = page.text.split('\n')
    current_year = None
    for line in lines:
        if re.match(r'^\d{4}$', line.strip()):
            current_year = line.strip()
        elif line.startswith(date):
            if re.search(r'\d{4}', line) is None and current_year is not None:
                event = line.replace(date + ': ', '')
                return f"{date} {current_year}: {event}"
            else:
                return line

    return None

def get_event_on_date_from_table(date):
    url = "https://en.wikipedia.org/wiki/Timeline_of_Pakistani_history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = pd.read_html(url)

    for table in tables:
        if 'Date' in table.columns:
            for index, row in table.iterrows():
                if row['Date'] == date:
                    event = re.sub(r'\[\d+\]', '', row['Event']) 
                    return f"{row['Date']} {row['Year']}: {event}"

    return None

def get_event_on_date(date):
    event_from_text = get_event_on_date_from_text(date)
    event_from_table = get_event_on_date_from_table(date)

    if event_from_text is not None:
        print(event_from_text)
    if event_from_table is not None:
        print(event_from_table)

    if event_from_text is None and event_from_table is None:
        print("No event found for this date.")

date = input("Enter a date (e.g., 18 August): ")
get_event_on_date(date)
