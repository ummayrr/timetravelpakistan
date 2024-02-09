import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

def get_event_on_date(date):
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

date = input("Enter a date (e.g., 18 August): ")
get_event_on_date(date)
