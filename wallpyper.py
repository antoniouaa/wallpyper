import requests
import ctypes
import os
from time import sleep
from random import choice

BASE_URL = "https://api.unsplash.com/search/photos"
TERMS = ["mountain", "sunset", "sunrise", "nature", "skyline", "monument", "graffiti", "aurora"]

def grab_credentials(cred_path):
    with open(cred_path) as f:
        credentials = {}
        for line in f:
            field, value = line.split("=")
            credentials[field] = value.strip()
        return credentials

def query(term, img_num=100, page_num=10, width=1920):
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {CREDENTIALS['ACCESS']}",
    }
    page_params = {
        "per_page": f"{img_num}",
        "orientation": "landscape",
        "page": f"{page_num}",
        "query": term
    }
    dimensions = f"?fit=crop&fm=png&w={width}"
    req = requests.get(BASE_URL, headers=headers, params=page_params)
    json = req.json()
    images = []
    for result in json["results"]:
        try:
            images.append(f'{result["urls"]["raw"]}{dimensions}')
        except KeyError:
            pass
    return images

def set_background(img_url, img_path="tmp\\wallpaper.png"):
    download = requests.get(img_url, stream=True)
    with open(img_path, "bw") as f:
        for x in download:
            f.write(x)
    absolute_img_path = os.path.abspath(img_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_img_path, 0)

if __name__ == "__main__":
    CREDENTIALS = grab_credentials("credentials.txt")
    change_every = 3*60*60
    while True:
        random_term = choice(TERMS)
        images = query(random_term)
        random_image = choice(images)
        set_background(random_image)
        sleep(change_every)
