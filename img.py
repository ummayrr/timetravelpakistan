import requests
import json
import os
import glob
import mimetypes

cse_id = ""
api_key = ""

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

        filename = f'image{i}{extension}'

        with open(os.path.join(download_directory, filename), 'wb') as out_file:
            out_file.write(response.content)

        print('Image downloaded:', os.path.join(download_directory, filename))
        break
