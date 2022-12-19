from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template('test.html', names=['a', 'b', 'c'])
    


