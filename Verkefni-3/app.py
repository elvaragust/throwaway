from flask import Flask, flash,redirect, render_template, request, json
import urllib.request
import os
from datetime import datetime
from jinja2 import ext

app= Flask(__name__)

app.jinja_env.add_extension(ext.do)

#bensin stöðvar 
with urllib.request.urlopen("https://apis.is/petrol/") as url:
    gogn = json.loads(url.read().decode())

def format_time(gogn):
    return datetime.strptime(gogn, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m. %Y. Kl. %H:%M')

app.jinja_env.filters['format_time'] = format_time 

''' Lægsta verðið '''
def minPetrol():
    minPetrolPrice = 1000
    company = None
    address = None
    lst = gogn['results']
    for i in lst:
        if i['bensin95'] is not None:
            if i['bensin95'] < minPetrolPrice:
                minPetrolPrice = i['bensin95']
                company = i['company']
                address = i['name']
    return [minPetrolPrice, company, address]
    
"""
# gengið
with urllib.request.urlopen("http://apis.is/currency") as url:
    data = json.loads(url.read().decode()) 
"""
@app.route('/')
def index():
    return render_template('index.html', gogn=gogn, minP=minPetrol())

@app.route('/company/<company>')
def comp(company):
    return render_template('company.html',gogn=gogn,com=company)

@app.route('/moreinfo/<key>')
def more(key):
    return render_template('moreinfo.html', gogn=gogn,k=key)



#Villu leit
@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html'),404

@app.errorhandler(500)
def servererror(error):
    return render_template('servererror.html'),500

if __name__ == '__main__':
    #app.run
    app.run(debug=True, use_reloader=True)