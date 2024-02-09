import wikipediaapi
import re

def get_event_on_date(date):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='TimeTravelPakistan')
    page = wiki_wiki.page('Timeline_of_Pakistani_history')

    if not page.exists():
        print("Page nottt found")
        return

    lines = page.text.split('\n')
    found = False
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

    if not found:
        print("Nno event found for thisss date.")

date = input("Enter a date, 18 August ")
get_event_on_date(date)
