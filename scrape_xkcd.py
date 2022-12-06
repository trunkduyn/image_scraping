import io
import os
import re

from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

import requests
from PIL import Image

headless = True
cur_dir = os.path.dirname(os.path.abspath(__file__))
target_folder = os.path.join(cur_dir, "xkcd_comics")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

chrome_options = Options()
if headless:
    chrome_options.add_argument("--headless")

url_pattern = "https://xkcd.com/{}/"

with webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options) as wd:
    for i in range(1665, 2707):
        url = url_pattern.format(i)
        content = requests.get(url)
        url_match = re.search("https://imgs.xkcd.com/comics/[^\"]+", content.text)
        if url_match:
            print(url_match.group())
            try:
                image_content = requests.get(url_match.group()).content
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')
            except:
                print("no matching url found in page")
                continue
        else:
            print("No image found")
        file_path = os.path.join(target_folder, 'xkcd_{}.jpg'.format(i))
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
