import os
import sys
import csv
import json
import requests
from time import sleep

api_key = "" # replace here

output_data = []

shell_input = sys.argv[1:]

def get_places(cordinate=shell_input[0], keyword=shell_input[1]):

	next_page_token = None

	while True:

		try:
			response = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={cordinate}&rankby=distance&type={keyword}&key=' + api_key).json()
			break

		except Exception as e:
			print('An Error Occured!')


	try:
		next_page_token = response['next_page_token']

	except Exception as e:
		next_page_token = None
	
	places = response['results']
	format_repsonse(places)
	
	while next_page_token:

		sleep(10.0)

		print('Waiting....')

		while True:

			try:

				response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=%s&key=%s' % (next_page_token, api_key)).json()
				break

			except Exception as e:
				print('An Error Occured')

		try:
			next_page_token = response['next_page_token']

		except Exception as e:
			next_page_token = None

		places = response['results']
		format_repsonse(places)
	
	print('Done.')


def repeat_process(cycles=int(shell_input[2]), keyword=shell_input[1]):

	for i in range(cycles):

		data = output_data[-1]

		long = data['location']['lng']
		lat = data['location']['lat']


		while True:

			try:
				response = requests.get(f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&rankby=distance&type={keyword}&key=' + api_key).json()
				break

			except Exception as e:
				print('An Error Occured!')

		try:
			next_page_token = response['next_page_token']

		except Exception as e:
			next_page_token = None
	
		places = response['results']
		format_repsonse(places)
	
		while next_page_token:

			sleep(10.0)

			print('Waiting....')

			while True:

				try:
					response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken=%s&key=%s' % (next_page_token, api_key)).json()
					break

				except Exception as e:
					print('An Error Occured!')

			try:
				next_page_token = response['next_page_token']

			except Exception as e:
				next_page_token = None

			places = response['results']
			format_repsonse(places)

	print('Successful!')

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

		def filter_place(data):

			if data['location']['lat'] == place['geometry']['location']['lat'] and data['location']['lng'] == place['geometry']['location']['lng']:
				return True
			elif round(data['location']['lat'], 3) == round(place['geometry']['location']['lat'], 3) and round(data['location']['lng'], 3) == round(place['geometry']['location']['lng'], 3):
				return True
			else:
				return False
		
		filted = list(filter(filter_place, output_data))
		if len(list(filted)) == 0:

			output_data.append({
				'name': place['name'],
				'area_name': place['vicinity'],
				'location': place['geometry']['location'],
				'color': get_icon_color(place['types']),
			})

def create_output_json(data):

	print('Creating output json file...')
	output = open(os.path.join('output.json'), 'w+', encoding='utf-8')
	output.write(json.dumps(data))
	output.close()
	print('output.json file created')

def create_output_csv(data):

	print('Creating output csv file...')
	with open('output.csv', 'w+', newline='', encoding='utf-8') as csvfile:
		outputwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_ALL)
		outputwriter.writerow(['name', 'Area name', 'Location (lat/lng)', 'Icon color'])
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
	repeat_process()

	create_output_json(output_data)
	create_output_csv(output_data)
