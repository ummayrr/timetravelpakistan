import wikipediaapi
import re

def get_event_on_date(date):
    wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='TimeTravelPakistan')
    page = wiki_wiki.page('Timeline_of_Pakistani_history')

    if not page.exists():
        print("Page not found")
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
                    print(f"{date} {year}: {event}")
                else:
                    print(line)
            found = True

    if not found:
        print("No event found for this date.")

date = input("Enter a date, e.g., '18 August' ")
get_event_on_date(date)
