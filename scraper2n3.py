import wikipediaapi
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_event_on_date(date):
    events = []

  
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
                    events.append(f"{date} {current_year}: {event}")
                else:
                    year_match = re.search(r'\d{4}', line)
                    if year_match:
                        year = year_match.group(0)
                        event = line.replace(date + ': ', '').strip()
                        event = re.sub(r'^' + date + ' ', '', event)
                        event = re.sub(r'^:', '', event).strip() 
                        event = re.sub(r'^' + date.split()[1] + ' ', '', event)  
                        event = re.sub(r'^\s+', '', event) 
                        if event.startswith(year): 
                            event = event.replace(year, '', 1).strip() 
                        event = re.sub(r'^:', '', event).strip()  
                        events.append(f"{date} {year}: {event}")

    url = "https://en.wikipedia.org/wiki/Timeline_of_Pakistani_history"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = pd.read_html(url)

    for table in tables:
        if 'Date' in table.columns:
            for index, row in table.iterrows():
                if row['Date'] == date:
                    event = re.sub(r'\[\d+\]', '', row['Event']) 
                    events.append(f"{row['Date']} {row['Year']}: {event}")

    if events:
        for event in events:
            print(event)
    else:
        print("No event found for this date.")

date = input("Enter a date (e.g., 18 August): ")
get_event_on_date(date)
