#Reference: https://gist.github.com/suriyadeepan/b940caf6cba552527613c1f93e26cc80

import requests
from bs4 import BeautifulSoup

def img(url):
    imgContent = requests.get(url=url).content

    soup = BeautifulSoup(imgContent, 'html.parser')

    imgs = soup.find_all('img')

    ret = []

    for img in imgs:
        ret.append(img.get('src'))

    return ret



"""
textContent = requests.get(url = 'https://en.wikipedia.org/wiki/City').content

soup = BeautifulSoup(textContent, 'html.parser')

texts = soup.find_all('a')
for text in texts:
	print(text.get('href'))
"""