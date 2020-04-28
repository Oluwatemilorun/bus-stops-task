# Task: Bus Stops in Lagos, Nigeria

> Design code that retrieves a list of all the bus stops in Lagos, Nigeria including the name, latitude and longitude for the bus stop, as well as the local area name. Examples of local area names are “Mushin”, “Yaba”, “Surulere”.

## Approach

### First Thought
The first approach I took to this task was to go throught Google Maps API documentation to see if there was an API available to retrieve it directly. After much Googling, I stumbled on a StackOverflow question with the exact same problem and a [response](https://stackoverflow.com/a/7139196/7124240) to that question was there wasn't a direct API to achieve said task on Google Maps.

Although, a simple Google search of `bus stops in lagos` returned the results needed, with the list or search results spanning across 10 pages. So, I decided to crawl it scrape it out. But, an issue surfaced has to how to get the coordinates (Lng/Lat) of said bus stops without having to click over 100 locations to get it. I later discovered that, the Lng/Lat of each location was embed in the url of each location on Google Maps...which was dynamically upated using JavaScript, bummer.

### Further Digging
Going through Google Maps, I discovered it offered a way to search for places directly. Knowing this I went directly to the Google Maps Place API documentation where I finally found [Text Search Requests](https://developers.google.com/places/web-service/search#TextSearchRequests) which allows you make the same search query done directly on the Google Maps platform with an API endpoint.

### Final Resolve
I wrote a simple python script to make a request that makes a search query on Google Maps and retrieves the list of bus stops in lagos, Nigeria. This script also, produces a JSON and CSV file containing the results.

### Challenges
- My Google Place API (free) key doesn't allow me make a lot of query, so I am limited to little results

## Using the Script
### Requirements
- Google Places API Key
- Google Custom Search Engine (cse) Key
- Python 3

### Usage
Open `./places.py` and replace the value of `api_key` with the API key retrieved or collected from Google API Console.

```bash
# Install  dependecies
$ pip install -r requirements.txt

# Run python script
$ python places.py
```
