import wikipediaapi
import datetime
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

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

date = input("Enter the date (MM/DD): ")

date_input = date
month, day = map(int, date_input.split('/'))
date_formatted = datetime.datetime(year=1, month=month, day=day).strftime('%B_%d')

url = 'https://en.wikipedia.org/wiki/' + date_formatted

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

events = {'Births': [], 'Deaths': [], 'Events': []}
unique_events = set()
for section in events.keys():
    section_content = soup.find('span', {'id': section}).parent.find_next_siblings(['ul', 'ol'])
    for ul in section_content:
        if ul.find_previous_sibling().name == 'h2':
            break
        for li in ul.find_all('li'):
            if 'Pakistan' in li.text and li.text not in unique_events:
                split_text = re.split(' – | : ', li.text.strip(), 1)
                year = split_text[0].strip()
                description = re.sub(r'\[\d+\]', '', split_text[1]).strip() if len(split_text) > 1 else ""
                formatted_date = f"{day} {datetime.datetime(year=int(year), month=month, day=1).strftime('%B')} {year}"
                if '(b.' in description:
                    events['Deaths'].append(f"{formatted_date}: Death of {description}")
                elif section == 'Births':
                    events[section].append(f"{formatted_date}: Birth of {description}")
                else:
                    events[section].append(f"{formatted_date}: {description}")
                unique_events.add(li.text)

print("\n")
for category, items in events.items():
    if items:
        print(category)
        for item in items:
            print(item)
        print("\n")

get_event_on_date(date)
