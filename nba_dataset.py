from nba_project.nba_api import games

import pandas as pd

# Initialize team standings dictionary for all 30 NBA teams
nba_teams = [
    'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
    'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
    'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
    'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
    'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
    'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'
]

standings = {team: {
    'wins': 0,
    'losses': 0,
    'scored': 0,
    'allowed': 0,
    'home_wins': 0,
    'home_losses': 0,
    'away_wins': 0,
    'away_losses': 0
} for team in nba_teams}

def update_standings(game):
    home_team = game['teams']['home']['name']
    away_team = game['teams']['visitors']['name']
    try: 
        if game['scores']['home']['points'] is None or isinstance(game['scores']['home']['points'], str): 
            home_score = 0
        else :        
            home_score = game['scores']['home']['points']
    except : 
        print("something went wrong for {}" .format(game['scores']['home']['points']) )

    try: 
        if game['scores']['visitors']['points'] is None or isinstance(game['scores']['visitors']['points'], str):     
            away_score = 0
        else :        
            away_score = game['scores']['visitors']['points']
    except :
         print("something went wrong for {}" .format(game['scores']['visitors']['points']) )

    # Update points totals
    standings[home_team]['scored'] += home_score
    standings[home_team]['allowed'] += away_score
    standings[away_team]['scored'] += away_score
    standings[away_team]['allowed'] += home_score
    
    # Update records
    if home_score > away_score:
        standings[home_team]['wins'] += 1
        standings[home_team]['home_wins'] += 1
        standings[away_team]['losses'] += 1
        standings[away_team]['away_losses'] += 1
    else:
        standings[away_team]['wins'] += 1
        standings[away_team]['away_wins'] += 1
        standings[home_team]['losses'] += 1
        standings[home_team]['home_losses'] += 1

def get_standings_df():
    records = []
    for team in standings:
        stats = standings[team]
        records.append({
            'Team': team,
            'W': stats['wins'],
            'L': stats['losses'],
            'PTS': stats['scored'],
            'OPP PTS': stats['allowed'],
            'DIFF': stats['scored'] - stats['allowed'],
            'PCT': stats['wins'] / (stats['wins'] + stats['losses']) if (stats['wins'] + stats['losses']) > 0 else 0,
            'HOME': f"{stats['home_wins']}-{stats['home_losses']}",
            'ROAD': f"{stats['away_wins']}-{stats['away_losses']}",
            'SEASON' : game["season"]
        })
    
    df = pd.DataFrame(records)
    df['PCT'] = df['PCT'].round(3)
    df['RK'] = df['PCT'].rank(ascending=False, method='min').astype(int)
    df = df.sort_values(['PCT', 'DIFF'], ascending=[False, False] )
    
    return df[['RK', 'Team', 'W', 'L', 'PCT', 'PTS', 'OPP PTS', 'DIFF', 'HOME', 'ROAD', 'SEASON']]

# Process all games
for game in games:  # Your games list from data["response"]
    if game['teams']['home']['name'] not in nba_teams or game['teams']['visitors']['name'] not in nba_teams :
        continue
    else :
        update_standings(game)

# Get final standings
standings_df = get_standings_df()
print(standings_df.head(10))  # Show top 10 teams