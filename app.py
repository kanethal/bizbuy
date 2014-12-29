from flask import Flask, make_response, session, request, jsonify
from scraper import url, pars, parse_main, parse_entry
import requests

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'not very secret'

@app.route('/')
def main():
    return(make_response(open('static/index.html').read()))

@app.route('/q', methods=['GET'])
def query():
    r = requests.get(url, params = pars)
    data = parse_main(r)
    return jsonify({'data': data})
    

if __name__ == '__main__': app.run()

