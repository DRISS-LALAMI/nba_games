import http.client
import ssl
import requests
import json
import pandas as pd
# Create unverified context
context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection(
    "api-nba-v1.p.rapidapi.com",
    context=context
    )

headers = {
    'x-rapidapi-key': "3f02c12bd2msh27e7b13e0d4d910p11f36ajsn530d686a9dea",
    'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
}

seasons = [2020, 2021, 2022, 2023, 2024]
games = []
for season in seasons:
    conn.request("GET", f"/games?season={season}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    # Decode UTF-8 bytes to Unicode, and convert single quotes 
    # to double quotes to make it valid JSON
    my_json = data.decode('utf8')   #.replace("'", '"')
    #print(my_json)
    #print('- ' * 20)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    #print(s)

    #print(data["response"][0] )  # keys = ['get', 'parameters', 'errors', 'results', 'response']
    games += data["response"]
    
#print(games[0])
 
