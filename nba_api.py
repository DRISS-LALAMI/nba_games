# import list
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
seasonal_games = {}

for season in seasons :
    conn.request("GET", f"/games?season={season}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode('utf8'))
    seasonal_games[season] = data["response"]  # Stores games by season
#  create games list that contains all the games

 
     
     
     
