import os
import csv
import json
import requests

api_key = "YOUR_API_KEY" # replace here
output_data = []

def get_places():
	next_page_token = None

	response = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?query=bus+stops+lagos&radius=10000000&key=' + api_key).json()
	try:
		next_page_token = response['next_page_token']

	except Exception as e:
		next_page_token = None
	
	places = response['results']
	format_repsonse(places)
	
	while next_page_token:
		response = requests.get('https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken%s&key=%s' % (next_page_token, api_key)).json()
		try:
			next_page_token = response['next_page_token']

		except Exception as e:
			next_page_token = None

		places = response['results']
		format_repsonse(places)
	
	print('Done.')

def get_icon_color(types):
	"""
	There are 2 main feature types that is used in determining the color
	- `transit_station` - returns `Blue`
	- `bus_station` - returns `Yellow`
	
	`Unknown` is returned if the type doesn't have either of these types

	@param	`type`: List

	"""

	if 'bus_station' in types:
		return 'Yellow'
	elif 'transit_station' in types:
		return 'Blue'
	else:
		return 'Unknown'


def format_repsonse(places):
	print('Reading %d places' % len(places))
	for place in places:
		output_data.append({
			'name': place['name'],
			'area_name': place['formatted_address'],
			'location': place['geometry']['location'],
			'color': get_icon_color(place['types'])
		})

def create_output_json(data):
	print('Creating output json file...')
	output = open(os.path.join('output.json'), 'w+')
	output.write(json.dumps(data))
	output.close()
	print('output.json file created')

def create_output_csv(data):
	print('Creating output csv file...')
	with open('output.csv', 'w+', newline='') as csvfile:
		outputwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_ALL)
		outputwriter.writerow(['Bus stop name', 'Area name', 'Location (lat/lng)', 'Icon color'])
		for row in output_data:
			outputwriter.writerow([
				row['name'],
				row['area_name'],
				'%s/%s' % (row['location']['lat'], row['location']['lng']),
				row['color']
			])

	
	print('output.csv file created')
		

if __name__== "__main__":
	get_places()

	create_output_json(output_data)
	create_output_csv(output_data)