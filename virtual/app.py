from xml.dom.expatbuilder import ParseEscape
from flask import Flask, render_template, render_template_string, request, redirect, url_for, jsonify, escape
from flask_socketio import SocketIO, emit
import json
import asyncio
import requests as requests
from random import randint
import httpx
import time
import jinja2


# following lines circumvent the proper way of including this file but idgaf
import sys
sys.path.append('../')
from Correlations import *

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    static = url_for('static', filename='/')
    return env.get_template('index.html').render(static=static)
    #return render_template('index.html')

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
        return env.get_template('results.html').render(test=c.results, time=end-start, numresults = num_results, correlations = c.correlations)
        #return render_template('results.html', test=c.results, time=end-start, numresults = num_results, correlations = c.correlations)


@app.route('/how')
def how():
    return render_template('how.html')
    

def include_file(name):
    return jinja2.Markup(loader.get_source(env, name)[0])

loader = jinja2.PackageLoader(__name__, 'templates')
env = jinja2.Environment(loader=loader)
env.globals['include_file'] = include_file

@app.route('/test', methods=['GET', 'POST'])
def test():
    return env.get_template('testSVG.html').render()
    #return render_template('testSVG.html')

