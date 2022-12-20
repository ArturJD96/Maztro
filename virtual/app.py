from xml.dom.expatbuilder import ParseEscape
from flask import Flask, render_template, request, redirect, url_for
# following line imports ../Correlations.py one folder up
#from ..Correlations import Correlations


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    return render_template('test.html')

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
        sonata = 'sonata03-1.krn'
        myank = ['1', '3', '4', '6']
        return render_template('results.html', sonata=sonata, filter=myank)
        