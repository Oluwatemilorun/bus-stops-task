import os
import json
from googleapiclient.discovery import build

api_key = "YOUR_API_KEY"
cse_id = "YOUR_CSI_KEY"

def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

results = google_search('bus stops in lagos')

output = open(os.path.join('output.json'), 'w+')

output.write(json.dumps(results))
output.close()