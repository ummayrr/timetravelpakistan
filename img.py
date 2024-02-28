import os
import requests
import json
import glob
import mimetypes
from dotenv import load_dotenv

load_dotenv()

cse_id=os.getenv("cse_id_main")
api_key=os.getenv("api_key_main")

download_directory = "downloads"

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

for file in glob.glob(os.path.join(download_directory, '*')):
    if os.path.isfile(file):
        os.remove(file)
        print(f'Deleted: {file}')

num_files = len([name for name in os.listdir('.') if os.path.isfile(name) and name.startswith('text') and not name.endswith('original.txt')])

for i in range(1, num_files+1):
    with open(f'text{i}original.txt', 'r') as f:
        search_term = f.read().strip()

    start_index = 1
    while True:
        url = f"https://www.googleapis.com/customsearch/v1?q={search_term}&num=1&start={start_index}&searchType=image&key={api_key}&cx={cse_id}"

        response = requests.get(url)
        response.raise_for_status()

        search_results = response.json()
        image_url = search_results['items'][0]['link']

        response = requests.get(image_url)
        if response.status_code == 404:
            start_index += 1
            continue

        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)

        if not extension:
            extension = '.png'

        filename = f'image{i}{extension}'

        with open(os.path.join(download_directory, filename), 'wb') as out_file:
            out_file.write(response.content)

        file_size = os.path.getsize(os.path.join(download_directory, filename))
        if file_size < 30 * 1024:  # 20KB
            os.remove(os.path.join(download_directory, filename))
            print(f'Deleted: {os.path.join(download_directory, filename)} due to chhota size.')
            start_index += 1
            continue

        print('Image downloaded:', os.path.join(download_directory, filename))
        break
