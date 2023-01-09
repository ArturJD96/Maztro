from xml.dom.expatbuilder import ParseEscape
from flask import Flask, render_template, render_template_string, request, redirect, url_for, jsonify, escape
import json
import asyncio
import requests as requests
from random import randint
import httpx
import time


# following lines circumvent the proper way of including this file but idgaf
import sys
sys.path.append('../')          # ! ! ! this might be usefull for folder restructuring
from Correlations import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    print('search')

    test_data= {
        'kern': '        **kern        *M4/4        =1-        4g        8fL        8eJ        4d        4c        =        *-',
        'test': {'foo': 7, 'bar': 'a string'}
    }
    
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        return render_template('test.html', query=test_data)

@app.route('/google', methods=['GET', 'POST'])
def google():
    print('google')
    return render_template('google.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    print('results')
    if request.method == 'POST':
        start = time.perf_counter()
        # THIS IS WHERE THE MIDI INPUT SHOULD GO
        #data = request.form['data']
        #print(data)

        # get data from Correlations.py
        c = Correlations_in_kern_repository()
        end = time.perf_counter()
        print(c.results)
        print(c.correlations)
        num_results = sum([len(c.results[x]) for x in c.results if isinstance(c.results[x], list)])
        return render_template('results.html', test=c.results, time=end-start, numresults = num_results, correlations = c.correlations)
    
############## FOR TESTING ##########################3
# function converted to coroutine
async def get_xkcd_image(session):
    random = randint(0, 300)
    result = await session.get(f'http://xkcd.com/{random}/info.0.json') # dont wait for the response of API
    return result.json()['img']

# function converted to coroutine
async def get_multiple_images(number):
    async with httpx.AsyncClient() as session: # async client used for async functions
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks) # gather used to collect all coroutines and run them using loop and get the ordered response
    return result


@app.route('/comic')
async def hello():
    start = time.perf_counter()
    urls = await get_multiple_images(5)
    end = time.perf_counter()
    markup = f"Time taken: {end-start}<br><br>"
    for url in urls:
        markup += f'<img src="{url}"></img><br><br>'

    return markup

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testSVG.html')
    #return render_template('results.html', test={'checking database': []})

@app.route('/how')
def how():
    return render_template('how.html')
    
#@app.route('/resultsJSON', methods=['GET', 'POST'])
#def resultsJSON():
#    print('results')
#    #if request.method == 'POST':
#    c = Correlations_in_kern_repository()

#    jsonResp = json.dumps(c.results) #{'jack': 4098, 'sape': 4139}
#    print(jsonResp)
#    print("BBBBBBBBBBBBBBB")
#    #return jsonify(jsonResp)
#    # following line returns the macro results() with parameter jsonResp
    
#    return render_template_string('{{resultsJSON}}', resultsJSON=(jsonResp))
#    #return render_template('results.html', resultsJSON = jsonify(jsonResp))
