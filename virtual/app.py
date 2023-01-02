from xml.dom.expatbuilder import ParseEscape
from flask import Flask, render_template, render_template_string, request, redirect, url_for, jsonify, escape
import json

# following lines circumvent the proper way of including this file but idgaf
import sys
sys.path.append('../')
from Correlations import Correlations_in_kern_repository

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    return render_template('google.html')

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
        data = request.form['data']
        print(data)

        # get data from Correlations.py
        c = Correlations_in_kern_repository()
        print(c.results)
        print("AAAAAAAAAA")
        return render_template('results.html', test=c.results)

@app.route('/resultsJSON', methods=['GET', 'POST'])
def resultsJSON():
    print('results')
    #if request.method == 'POST':
    c = Correlations_in_kern_repository()

    jsonResp = json.dumps(c.results) #{'jack': 4098, 'sape': 4139}
    print(jsonResp)
    print("BBBBBBBBBBBBBBB")
    #return jsonify(jsonResp)
    # following line returns the macro results() with parameter jsonResp
    
    return render_template_string('{{resultsJSON}}', resultsJSON=(jsonResp))
    #return render_template('results.html', resultsJSON = jsonify(jsonResp))
