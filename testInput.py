# coding=utf8

from Correlations import Correlations_in_kern_repository
import requests

#main:
def __main__:
# some dummy input variable:
    input = "**kern\
    cc\
    cc#\
    dd\
    ee–"

    # a post request to localhost:
    r = requests.post('http://localhost:5000/results', data = {'data': input})