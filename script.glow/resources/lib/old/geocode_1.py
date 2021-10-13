#!/bin/python

import requests

postcode = raw_input('Enter Postcode: ')

url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': postcode}
r = requests.get(url, params=params)
results = r.json()['results']

print results

location = results[0]['geometry']['location']
latitude = location['lat']
longitude = location['lng']

address_components = results[0]['address_components']

for item in range(1, len(address_components)):
  print address_components[item]['long_name']

print postcode.upper()
print "%f, %f" % (latitude, longitude)

print results[0]['formatted_address']