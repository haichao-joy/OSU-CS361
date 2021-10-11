from flask import Flask, render_template, request, jsonify, session
import transformer
import validators
from imgscraper import img
import requests
import random
import csv
from datetime import timedelta
import urllib

upper = 23793
lower = 1

app = Flask(__name__)
app.secret_key = "SCOTT&STOTT's_SECRIT_PLAYS"
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=2)



@app.route("/", methods=["POST", "GET"])
def home():
    if 'history' not in session:
        session['history'] = []
        session['index'] = 0

    if request.method == 'GET':
        url, loc, pop, text = get_page()
    elif request.method == 'POST':
        url, loc, pop, text = post_page(request.form['submit'])
    else:
        return "<p>Invalid Request</p>"

    PARAMS = {"inputLink":url}
    img_arr = requests.get("http://flip2.engr.oregonstate.edu:6248/api", PARAMS)
    print(img_arr)
    print(img_arr.json())
    img_arr = img_arr.json()['links']
    img_arr = img_filter(img_arr)

    print(len(session['history']), session['index'], session['history'])
    header = requests.get("http://flip3.engr.oregonstate.edu:8183/"+url).json()

    content = {"images":img_arr, "len":len(img_arr), "location":loc, "population": pop, "text":text[0],
               "keywords":text[1], "header":header["data"], "index":session["index"]}

    return render_template('mainpage.html', **content)

"""
@app.route("/summary", methods=["POST", "GET"])
def summary():
    url_input = request.form.get("url_input")
    text_input = request.form.get("text_input")
    length = request.form.get("length")
    if validators.url(url_input) is True:
        summary = transformer.url_summarize(url_input, length)
        return render_template('transformed.html', tldr=summary[0], keywords=summary[1], len=len(summary[1]), flag=True)
    else:
        summary = transformer.text_summarize(text_input, length)
        return render_template('transformed.html', tldr=summary, flag=False)
"""
@app.route('/api/', methods=['GET'])
def url_api():
    type = request.args.get('type')
    input = request.args.get('input')
    length = request.args.get('length')
    res_json = None
    if type == "url":
        res_json = transformer.url_summarize(input, length)
    elif type == "text":
        res_json = transformer.text_summarize(input, length)

    res_json = {"summary": res_json[0], "keywords": res_json[1]}
    return jsonify(res_json)



@app.route('/api/text/', methods=['GET'])
def text_api():
    text = request.args.get('text')
    length = request.args.get('length')
    res_json = transformer.text_summarize(text, length)
    res_json = {'summary': res_json[0], "keywords": res_json[1]}
    return jsonify(res_json)


def img_filter(img_arr):
    ret_arr = []
    for i in range(len(img_arr)):
        c = img_arr[i].find('px')
        if c > 0:
            d = ''.join(filter(str.isdigit, img_arr[i][c - 4:c]))
            if int(d) > 99:
                ret_arr.append(img_arr[i])
    return ret_arr

def get_rand_location():
    rand = random.randint(lower, upper)
    with open('locationfile.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)

    url = reader[rand][12]
    pop = reader[rand][9]
    loc = utf_decoder(reader[rand][0] + ", " + reader[rand][4])
    url = utf_decoder(url)

    return (url, pop, loc)

def utf_decoder(str):
    return urllib.parse.unquote(urllib.parse.unquote(str))


def post_page(form):
    #text = (None, None)
    url, pop, loc = get_rand_location()

    index = session['index']-1
    if form == 'next' and index+1 == len(session['history']):
            text = transformer.url_summarize(url)
            session['index'] = session['index'] + 1
            session['history'].append( (url, pop, loc, text) )
            session.modified = True
    else:
        if form == 'next':
            session['index'] = session['index'] + 1
            index = index+1
        elif form == 'back':
            session['index'] = session['index']-1
            index = index-1
        url = session['history'][index][0]
        pop = session['history'][index][1]
        loc = session['history'][index][2]
        text = session['history'][index][3]

    url = utf_decoder(url)
    return url, loc, pop, text

def get_page():
    url, pop, loc = get_rand_location()
    text = transformer.url_summarize(url)
    #text = (None, None)
    session['history'].append((url, loc, pop, text))
    session['index'] = len(session['history'])
    return url, loc, pop, text

if __name__ == "__main__":
    app.run()