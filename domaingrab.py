#!/usr/bin/env python3

# Simple script to grab the AD domain from an NTLM auth page.
# Just point it at a page that's prompting you for creds.
# For OWA, you can point it at autodiscover or EWS e.g.: python3 domaingrab.py https://owa.client.com/EWS/Exchange.asmx

import requests
import sys
import base64
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    if len(sys.argv) < 2:
        print("Usage: {} <url>".format(sys.argv[0]))
        exit(1)

    url = 'https://'+sys.argv[1] if 'http' not in sys.argv[1] else sys.argv[1]

    try:
        get_domain(url)
    except requests.exceptions.SSLError:
        print('[-] Using HTTPS failed. Trying plain HTTP...')
        url = url.replace('https', 'http')
        get_domain(url)

def get_domain(url):
    try:
        request = requests.post(url, headers={
            'Authorization': 'NTLM TlRMTVNTUAABAAAAB4IIogAAAAAAAAAAAAAAAAAAAAAKAO5CAAAADw=='},
                                verify=False)
        challenge = request.headers['WWW-Authenticate'].split(', ')[0].split(' ')[1]
        if challenge.startswith('TlRMTVNTUAAC'):
            st = str(base64.b64decode(challenge)).replace('\\x00','')
            domain = re.search('x0f(.*)\\\\x02',st)
            print('[+] Domain: {}'.format(domain.group(1)))
        else:
            print('[-] Domain not found')
    except KeyError:
        print('[-] WWW-Authenticate header not found. Are you sure you have the correct page?')

if __name__ == '__main__':
    main()