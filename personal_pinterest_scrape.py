from collections import defaultdict

import requests
from py3pin.Pinterest import Pinterest
import os


def get_all_pins(pinterest, board_id):
    batch = pinterest.board_feed(board_id=board_id)
    while batch:
        for pin in batch:
            yield pin
        batch = pinterest.board_feed(board_id=board_id)

def get_all_boards(pinterest, max=500):
    batch = pinterest.boards()
    count = 0
    while batch and count<max:
        count += len(batch)
        for board in batch:
            yield board
        batch = pinterest.boards()


cur_dir = os.path.dirname(os.path.abspath(__file__))

email = 'lyltje@gmail.com'
password = 'WakaWaka^66KippiePinturas'
username = 'ly111x'
# I had to change some stuff local, the import doesnt have updates yet that are needed to run (uses elements_by_id instead of By.ID)
pinterest = Pinterest(email=email, password=password, username=username)
pinterest.login()

image_urls = defaultdict(list)

count = 0
fail_count = 0
for i, b in enumerate(get_all_boards(pinterest)):
    board_name = b['name']
    if "drawings" == board_name:
        x = 2
    for j, pin in enumerate(get_all_pins(pinterest, b['id'])):  # enumerate(batch):
        x = 2
        if not 'images' in pin or not pin['images']:
            fail_count += 1
        else:
            image_url = pin['images']['orig']['url']
            image_urls[board_name].append(image_url)
    print(board_name, b['id'], len(image_urls[board_name]))

data_folder = "images"

download_fails = 0
for b_name, urls in image_urls.items():
    directory = os.path.join(cur_dir, data_folder, b_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for url in urls:
        name = url.split('/')[-1]
        output_path = os.path.join(directory, name)
        if os.path.exists(output_path):
            print(b_name, url, 'allready exists')
            continue
        print(b_name, url, 'download')
        # download the image
        response = requests.get(url)
        if response.status_code:
            with open(output_path, 'wb') as fp:
                fp.write(response.content)
        else:
            download_fails += 1

total_count = sum(len(url) for url in image_urls.values())
print(f"Total: {total_count}")
print(f"failcount: {fail_count}")
print(f"download failcount: {download_fails}")
