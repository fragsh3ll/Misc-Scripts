#!/usr/bin/env python3

# Bing IP Search - performs a reverse IP search on Bing for a list of IP addresses. Good for discovering vhosts, etc.
# Result numbers can sometimes be off
# Usage: python3 bingsearch.py <file containing IP addresses>

import argparse
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('file',help='file containing a list of IP addresses')
args = parser.parse_args()

search_url = 'https://www.bing.com/search?q=ip:'

with open(args.file) as file:
    content = [line.strip() for line in file]

for ip in content:
    r = requests.get(search_url + ip)
    soup = BeautifulSoup(r.text, 'html.parser')
    result_num = soup.find('span',{'class':'sb_count'})
#   result_title = soup.find_all('li', 'b_algo')

    if result_num != None:
        print('Searching Bing for %s...' % ip)
        print('\t[+] %s for %s - link: %s' % (result_num.string,ip,search_url+ip))
    else:
        print('Searching Bing for %s... nothing' % ip)
