import sys
import json

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://lumtest.com/myip.json"

proxies = {'http': 'http://brd-customer-hl_20768c74-zone-zone1:3n7z29me5mr6@brd.superproxy.io:22225',
            'https': 'http://brd-customer-hl_20768c74-zone-zone1:3n7z29me5mr6@brd.superproxy.io:22225'}

cert_path = "/home/joe/Téléchargements/ca.crt"


response = requests.get(url, proxies=proxies, verify=False)

json_response = json.loads(response.text)
geo = json_response["geo"]
country = json_response["country"]
city = geo["city"]

print(response.json())
