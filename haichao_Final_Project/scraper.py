#References: https://gist.github.com/suriyadeepan/b940caf6cba552527613c1f93e26cc80
#https://www.edureka.co/blog/web-scraping-with-python/

from flask import Flask, render_template, request
import json
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
@app.route('/', methods = ['POST', 'GET'])
def web_scraper():
	return render_template('web_scraper.html')
@app.route("/result", methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		inputLink = request.form.get('inputLink')
		imgContent = requests.get(url=inputLink).content
		soup = BeautifulSoup(imgContent, 'html.parser')
		imgs = soup.find_all('img')
		links = []
		for img in imgs:
			img_link = img.get('src')
			print(img.get('src'))
			links.append(img_link)
		return render_template("result.html", scrapedData = links)

@app.route('/api', methods = ['POST', 'GET'])
def api():
	if request.method == 'GET':
		inputLink = request.args.get('inputLink')
#scrape all the images' links in a wikipedia page
		imgContent = requests.get(url=inputLink).content

		soup = BeautifulSoup(imgContent, 'html.parser')

		imgs = soup.find_all('img')

		links = []

		for img in imgs:
			img_link = img.get('src')
			print(img.get('src'))
			links.append(img_link)

		
		json = {"links": links}
		return json
		

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 6548))
   app.run(port=port, debug=True)

