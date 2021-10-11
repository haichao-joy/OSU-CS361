#Reference: https://pythonbasics.org/flask-template-data/

from flask import Flask, render_template, request, url_for
import json
import requests
import os

app = Flask(__name__)

#render the main web page of the application, which lets the user to input a link
@app.route('/', methods=["POST", "GET"])
def index():
    return render_template("index.html")

#render the web page with summarized contents in json format
@app.route('/summary', methods = ['POST', 'GET'])
def summary():
    if request.method == 'POST':
        inputLink = request.form.get('inputLink')

        #use a teammate's transformer microservice by using http request method
        PARAMS = {"type": "url", "input": inputLink, "length":7}
        resp = requests.get(url = "http://flip1.engr.oregonstate.edu:4444/api", params = PARAMS).json()

        return render_template("summary.html", summaryData = resp)




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5324))
    app.run(port=port, debug=True)