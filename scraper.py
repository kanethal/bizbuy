import requests
import json
from bs4 import BeautifulSoup as bs
import re

# Functions -------------------------------------------------------------------
def parse_main(r):
    soup = bs(r.content, 'html.parser')
    reg = re.compile(r'List_.*')
    listings = soup.findAll('a', {'id': reg})

    data = []
    for entry in listings:
        row = {}
        row['id'] = entry.attrs.get('id', 'DIDNOTPARSE')
        cflow = entry.find('span', 'cflow')
        row['title'] = entry.find('b', 'title').text
        row['cash_flow'] = int(cflow.find('b').text.strip('$').replace(',', '')) if cflow else None
        row['price'] = int(entry.find('span', 'price').text.strip('$').replace(',', ''))
        row['href'] = 'http://www.bizbuysell.com' + entry.attrs['href']
        data.append(row)
    return data

def parse_entry(r):
    #r = requests.get(data[0]['href'])
    soup2 = bs(r.content)
    table = sum([entry.findAll('p') for entry in soup2.findAll('div', 'specs')], [])
    # entries have lots of whitespace, and are divided by a colon
    rows = dict(["".join(row.text.split()).split(':') for row in table])
    return rows

# Test ------------------------------------------------------------------------
url = 'http://www.bizbuysell.com/listings/handlers/searchresultsredirector.ashx' 
pars = json.load(open('examples/default_pars.json'))

if __name__ == '__main__':
    r = requests.get(url, params=pars)
    data = parse_main(r)
    entry = parse_entry(requests.get(data[0]['href']))
