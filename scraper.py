import asyncio
import random
from bs4 import BeautifulSoup
import requests
import re
import calendar
import wikipediaapi
import pandas as pd
from datetime import datetime
import os
from sydney import SydneyClient
from dotenv import load_dotenv
import pytz

load_dotenv()

#har mahine update karna hai bhai
bing_cookies_main = os.getenv("BING_COOKIES_MAIN")
os.environ["BING_COOKIES"] = bing_cookies_main

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
                #oye tu ne tables pe kiun ni search kia
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
#searching for tables again separately
    for table in tables:
        if 'Date' in table.columns:
            for index, row in table.iterrows():
                if row['Date'] == date:
                    event = re.sub(r'\[\d+\]', '', row['Event']) 
                    events.append(f"{row['Date']} {row['Year']}: {event}")

    return events

def convert_date_format(date):
# at first look it might seem avoidable, but had to it becz the way i had started it all
    date_object = datetime.strptime(date, "%m/%d")
    return date_object.strftime("%-d %B")

async def main():
    while True:
        try:
            pkt = pytz.timezone('Asia/Karachi')
            date = datetime.now(pkt).strftime('%m/%d')
            date_converted = convert_date_format(date)

            # Scraper 1
            month, day = date.split('/')
            month = calendar.month_name[int(month)].lower()
            #shukria espn wale bhai
            url = f"https://www.espncricinfo.com/on-this-day/cricket-events/{month}/{day}"
            date2 = f"{day} {month.capitalize()}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            divs = soup.find_all('div')
            unique_div_texts = set()
            events_1 = []

            for i, div in enumerate(divs):
                text = div.text.strip()
                # well this one's hacked through, not the most solid thing to do but works 
                if len(text) >  1350:
                    continue
                if re.match(r'^\d{4}', text):
                    lower_text = text.lower()
                    if 'pakistan' in lower_text:
                        count_pakistan = lower_text.count('pakistan')
                        #is pe koi baat nahi hogi:
                        if not (count_pakistan == 1 and ('against pakistan' in lower_text or 'over pakistan' in lower_text or 'and a tour to pakistan' in lower_text or 'against a rather modest' in lower_text or 'caught short by pakistan' in lower_text or 'played three three tests for england in pakistan' in lower_text or 'england a squad to tour pakistan' in lower_text or 'with pakistan bowlers dropping' in lower_text or 'after nazar mohammad of pakistan' in lower_text or 'return to the side in 2015' in lower_text or 'famous test win over pakistan in harare' in lower_text or 'ending pakistan' in lower_text or 'conquered pakistan' in lower_text or re.search(r'against .* and pakistan', lower_text) or re.search(r'against .*, pakistan', lower_text) or re.search(r'against .*, and pakistan', lower_text) or re.search(r'against .*, .*, and pakistan', lower_text) or re.search(r'against .*, .*, .*, and pakistan', lower_text))):
                            if text not in unique_div_texts:
                                text = text.replace('\n', ' ')
                                year = re.search(r'\b\d{4}\b', text).group()
                                formatted_text = text.replace(year, '',  1).strip()
                                events_1.append(f"{date2} {year}: {formatted_text}")
                                unique_div_texts.add(text)

            # scraper 2
            events_2 = get_event_on_date(date_converted)

               # scraper 3
            date_input = date
            month, day = map(int, date_input.split('/'))
            date_formatted = datetime(year=1, month=month, day=day).strftime('%B_%d')
            url = 'https://en.wikipedia.org/wiki/' + date_formatted

            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            events_3 = {'Births': [], 'Deaths': [], 'Events': [], 'Holidays': []}
            unique_events = set()

            def is_holiday(text):
                return 'Day' in text or 'Holiday' in text or 'Observance' in text

            def process_section(header, section_name):
                next_tag = header.find_next(['ul', 'ol'])

                if next_tag:
                    while next_tag and next_tag.name in ['ul', 'ol']:
                        for li in next_tag.find_all('li'):
                            if 'Pakistan' in li.text and li.text not in unique_events:
                                split_text = re.split(r' â€“ | : ', li.text.strip(), 1)

                                if len(split_text) > 1:
                                    year = split_text[0].strip()
                                    description = split_text[1].strip()
                                else:
                                    year = ''
                                    description = split_text[0].strip()

                                formatted_date = f"{day} {datetime(year=1, month=month, day=day).strftime('%B')} {year}"

                                if is_holiday(description):
                                    events_3['Holidays'].append(f"{formatted_date}: {description}")
                                elif '(b.' in description:
                                    events_3['Deaths'].append(f"{formatted_date}: Death of {description}")
                                elif section_name == 'Births':
                                    events_3['Births'].append(f"{formatted_date}: Birth of {description}")
                                else:
                                    events_3['Events'].append(f"{formatted_date}: {description}")

                                unique_events.add(li.text)
                        next_tag = next_tag.find_next(['ul', 'ol'])

            def process_remaining_as_events():
                all_list_items = soup.find_all('li')
                for li in all_list_items:
                    if 'Pakistan' in li.text and li.text not in unique_events:
                        split_text = re.split(r' â€“ | : ', li.text.strip(), 1)

                        if len(split_text) > 1:
                            year = split_text[0].strip()
                            description = split_text[1].strip()
                        else:
                            year = ''
                            description = split_text[0].strip()

                        formatted_date = f"{day} {datetime(year=1, month=month, day=day).strftime('%B')} {year}"
                        events_3['Events'].append(f"{formatted_date}: {description}")
                        unique_events.add(li.text)

            headers = soup.find_all(['h2', 'h3'])

            for header in headers:
                section_name = header.get_text(strip=True).lower()

                if 'births' in section_name:
                    process_section(header, 'Births')
                elif 'deaths' in section_name:
                    process_section(header, 'Deaths')
                elif 'holidays' in section_name or 'observances' in section_name:
                    process_section(header, 'Holidays')

            process_remaining_as_events()


            # combining all events bhai
    #       all_events = events_1 + events_2 + [item for sublist in events_3.values() for item in sublist]
            all_events = events_2 + [item for sublist in events_3.values() for item in sublist] ######removed espn######
            events_dict = {}

            for event in all_events:
                date_year, description = event.split(": ", 1)
                if date_year in events_dict:
                    if len(description.split()) < len(events_dict[date_year].split()):
                        events_dict[date_year] = description
                else:
                    events_dict[date_year] = description

            events = [f"{date_year}: {description}" for date_year, description in events_dict.items()]

            async def main() -> None:
                # saare saboot mita do bhai
                for i in range(1, 21):
                    if os.path.exists(f'text{i}.txt'):
                        os.remove(f'text{i}.txt')
                    if os.path.exists(f'text{i}original.txt'):
                        os.remove(f'text{i}original.txt')

                async with SydneyClient(style="precise") as sydney:
                    await sydney.reset_conversation(style="precise") #bhai
                  #hehe
                    question = "Optimize the text for an instagram post, add a little background after the heading with interesting information in simple words. Heading should only include the date, followed by a colon. Censor any strong words like suicide to su__ic__ide, bombing to b__o__mbing, etc. Do not add any emotions, only facts. Text: "  
                    question2 = "Optimize the text for an instagram post, make the text a little simpler, add any useful info and you can cut useless info. There should be heading before. Heading should only include the date, followed by a colon. Do not add any emotions, only facts. Text: "
                    image_prompt_base_text = "Optimize this text into a prompt to get relevant images from a search engine. If 'birth of' or 'death of' is mentioned in text, do not include that, instead include only and only person's name for 'birth of' and 'death of' events. Remove any useless information. Try to be precise and short. Do not write anything other than the prompt in your response. Text: "

                    for i, event in enumerate(events, start=1):
                        if event in events_1:
                            question_to_ask = question2 + event
                        else:
                            question_to_ask = question + event
                        image_prompt = image_prompt_base_text + event
                  #ocd; but also they work better with reset convos
                        await sydney.reset_conversation(style="precise")
                        image_prompt_response = await sydney.ask(image_prompt, citations=False)
                        image_prompt_response = image_prompt_response.replace('"', '')
                      #search prompt for google
                        with open(f'text{i}original.txt', 'w') as f:
                            f.write(image_prompt_response)
                        await sydney.reset_conversation(style="precise")
                     #lil cleaning 🧹
                        response = await sydney.ask(question_to_ask, citations=False) #nahi chahiye bhai
                        response = re.sub(r'\[\^.\^\]', '', response)
                        response = response.replace('**', '')
                        response = '📅 ' + response + ' 🇵🇰' 
                        response = response + '\n\n'
                    #i dont think algorithm will pick these up.   
                        response = response + '#Pakistan #History #OnThisDay #PakistanPolitics #PakistanHistory #Politics #Cricket #PakistanCricketTeam #Sports #ThisDayInHistory #pakistan_pics #historyfacts #historylovers #cricketupdates #pakistandiaries #historypodcast #PakistanCricketBoard #pakistanart #historyclass'
                        with open(f'text{i}.txt', 'w') as f:
                            f.write(response)
                        print(response, end="", flush=True)
                        print("\n")
                    await sydney.close_conversation()

            if __name__ == "__main__":
                await main()
            break  # agar kaam khtm hua toh bhai
        except Exception as e:
            print(f"fukkkkkkkkkkkkk whatever is this: {e}") #doesnt happen now fortunately
            wait_time = random.uniform(3600, 5400)  # retrying after error. 1 hr - 1.5 hr
            print(f"dobara try after {wait_time/3600} hours...")
            await asyncio.sleep(wait_time) 

if __name__ == "__main__":
    asyncio.run(main())

