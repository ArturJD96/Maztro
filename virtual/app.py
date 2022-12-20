from xml.dom.expatbuilder import ParseEscape
from flask import Flask, render_template, request, redirect, url_for

# following lines circumvent the proper way of including this file but idgaf
import sys
sys.path.append('../')
from Correlations import Correlations_in_kern_repository

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

        #results = {'sonata01-1.krn': ['2', '8', '14', '17', '19', '27', '31-33', '55-56'], 'sonata01-2.krn': ['2', '4', '12-13', '44'], 'sonata01-3.krn': ['8', '29', '63', '65', '73', '94', '115', '130'], 'sonata02-1.krn': ['8', '11', '41', '43-45', '59', '75', '90', '93', '129', '131-133'], 'sonata02-2.krn': ['3-4', '4', '18', '31-32'], 'sonata02-3.krn': ['7', '27', '33', '46', '50', '53', '84', '93', '103', '114', '138', '157', '161', '164'], 'sonata03-2.krn': ['21', '30', '40', '65', '76', '79', '90'], 'sonata03-3.krn': ['3', '6', '13', '22', '25', '37', '46', '58', '74', '77', '84', '100', '105', '121', '126', '145', '148'], 'sonata04-1.krn': ['2', '10-11', '20', '23'], 'sonata04-2.krn': ['4-5', '5', '22-23', '39', '47', '57', '63'], 'sonata04-3.krn': ['22', '30', '43', '59'], 'sonata05-1.krn': ['2-4', '3-4', '43', '49', '63', '65', '67', '73', '77'], 'sonata05-2.krn': ['2', '7', '19', '26'], 'sonata05-3.krn': ['3', '16', '25', '27', '29', '43', '58', '62', '69', '83', '85', '91', '98', '123-126'], 'sonata06-1.krn': ['17', '19', '21', '88', '90'], 'sonata06-2.krn': ['20', '30'], 'sonata06-3a.krn': ['2'], 'sonata06-3e.krn': ['1', '1-3', '3', '5', '5-7'], 'sonata06-3l.krn': ['1', '1-3', '9', '9-11'], 'sonata06-3m.krn': ['5', '9-11', '14', '27', '31-32'], 'sonata07-1.krn': ['5', '12', '43-46', '92', '98', '104', '106', '124', '129', '132', '137-138'], 'sonata07-2.krn': ['5', '14', '27', '37', '37', '39', '57', '57', '63'], 'sonata07-3.krn': ['5', '13', '16', '25', '28', '32', '50', '97', '105', '122', '129', '139-140'], 'sonata08-1.krn': ['58', '58-59', '59-60', '62', '62-63', '67-68'], 'sonata08-2.krn': ['3', '9', '11', '13', '20', '22-23', '51', '51', '51-52'], 'sonata08-3.krn': ['3', '11', '14', '27', '30', '36', '41', '44', '62', '87', '89', '91', '109', '117', '120', '126', '131', '134', '147', '149', '151', '156', '167', '173', '178', '186', '189', '198'], 'sonata09-1.krn': ['10', '13', '17', '21', '53', '75', '79', '83', '94'], 'sonata09-2.krn': ['4', '9', '18', '42', '47', '55', '78', '83', '85', '85'], 'sonata09-3.krn': ['6', '17', '44', '68', '75', '75', '77', '77-78', '131-132'], 'sonata10-1.krn': ['8', '11', '20-21', '27-28', '65-67'], 'sonata10-2.krn': ['11', '21-24', '31-32'], 'sonata10-3.krn': ['5', '9', '11', '14', '28', '51', '66', '91', '100', '104', '106', '109', '123', '126', '141'], 'sonata11-1b.krn': ['23'], 'sonata11-1c.krn': ['40', '44', '49', '51', '51'], 'sonata11-1d.krn': ['10'], 'sonata11-1f.krn': ['3'], 'sonata11-2.krn': ['6', '11', '13', '15', '36', '38', '41', '43', '45'], 'sonata11-3.krn': ['1', '16', '25-27', '29-31', '90-91'], 'sonata12-1.krn': ['2', '36-37', '39', '41', '50', '73', '79', '83', '131', '134', '164', '171-173'], 'sonata12-2.krn': ['4', '12', '19', '24', '32'], 'sonata12-3.krn': ['23', '53', '97', '105', '116-117', '182', '188', '208', '221'], 'sonata13-1.krn': ['2', '9', '20-21', '44', '50', '54', '62', '65', '67', '69', '95', '102', '113', '116-117'], 'sonata13-2.krn': ['14', '16', '30', '43-47'], 'sonata13-3.krn': ['2', '8', '12', '14', '22', '31', '42', '48', '52', '54', '71', '79', '106', '113', '119', '123', '125', '139', '152', '188', '194', '201'], 'sonata14-1.krn': ['15', '19', '43', '45', '59', '62', '114', '119', '156', '159', '161', '177'], 'sonata14-2.krn': ['4', '9', '9', '11-12', '20', '41', '44', '52'], 'sonata14-3.krn': ['6', '19', '33', '55', '94', '109', '122', '136', '151', '163', '176', '226', '251', '265', '310', '312'], 'sonata15-1.krn': ['4', '17', '19', '25', '31', '45', '53'], 'sonata15-2.krn': ['21', '23'], 'sonata15-3.krn': ['9', '32', '42', '47-49'], 'sonata16-1.krn': ['19', '62', '78', '94', '151', '172', '192', '200'], 'sonata16-2.krn': ['11', '18', '21', '24', '31', '34', '39', '42-43'], 'sonata16-3.krn': ['9', '20', '23', '27-28', '37', '39', '48', '68', '71', '73', '75', '77', '79'], 'sonata17-1.krn': ['2', '5', '10', '17', '19', '26', '53', '55', '59', '68', '76', '76', '76', '96', '99', '103', '120', '120', '147', '153', '155'], 'sonata17-2.krn': ['4', '10', '25-26', '39-40'], 'sonata17-3.krn': ['12', '23', '27', '35', '37', '48', '56', '58-62']}
        #return render_template('results.html', results=results)
        # get data from Correlations.py
        c = Correlations_in_kern_repository()
        print(c.results)
        return render_template('results.html', results=c.results)
        #sonata = 'sonata03-1.krn'
        #myank = ['1', '2-3', '4', '6']
        #return render_template('results.html', sonata=sonata, filter=myank)
        