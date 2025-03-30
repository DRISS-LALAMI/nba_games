from nba_api  import seasonal_games
import pandas as pd

# Initialize NBA teams list
nba_teams = [
    'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
    'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
    'Houston Rockets', 'Indiana Pacers', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
    'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
    'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
    'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'
]

def update_standings(standings, game):
    home_team = game['teams']['home']['name']
    away_team = game['teams']['visitors']['name']
    
    try: 
        home_score = 0 if (game['scores']['home']['points'] is None or 
                          isinstance(game['scores']['home']['points'], str)) else game['scores']['home']['points']
    except Exception as e:
        print(f"Error with home score: {e}")
        home_score = 0

    try: 
        away_score = 0 if (game['scores']['visitors']['points'] is None or 
                          isinstance(game['scores']['visitors']['points'], str)) else game['scores']['visitors']['points']
    except Exception as e:
        print(f"Error with away score: {e}")
        away_score = 0

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

def get_standings_df(standings, season):
    records = []
    for team, stats in standings.items():
        records.append({
            'SEASON': season,
            'Team': team,
            'W': stats['wins'],
            'L': stats['losses'],
            'PTS': stats['scored'],
            'OPP PTS': stats['allowed'],
            'DIFF': stats['scored'] - stats['allowed'],
            'PCT': stats['wins'] / (stats['wins'] + stats['losses']) if (stats['wins'] + stats['losses']) > 0 else 0,
            'HOME': f"{stats['home_wins']}-{stats['home_losses']}",
            'ROAD': f"{stats['away_wins']}-{stats['away_losses']}"
        })
    
    df = pd.DataFrame(records)
    df['PCT'] = df['PCT'].round(3)
    df['RK'] = df['PCT'].rank(ascending=False, method='min').astype(int)
    return df.sort_values(['PCT', 'DIFF'], ascending=[False, False])

# Initialize seasonal_standings dictionary
seasonal_standings = {}

# Process each season
for season, games_in_season in seasonal_games.items():
    # Reset standings for each season
    current_standings = {team: {
        'wins': 0, 'losses': 0, 
        'scored': 0, 'allowed': 0,
        'home_wins': 0, 'home_losses': 0,
        'away_wins': 0, 'away_losses': 0
    } for team in nba_teams}
    
    for game in games_in_season:
        if (game['teams']['home']['name'] in nba_teams and 
            game['teams']['visitors']['name'] in nba_teams):
            update_standings(current_standings, game)
    
    # Store standings for this season
    seasonal_standings[season] = get_standings_df(current_standings, season)

# Combine all seasons
all_standings = pd.concat(seasonal_standings.values())

# Print standings for each season
for season, standings_df in seasonal_standings.items():
    print(f"\n{season} Season Standings:")
    print(standings_df.head(10))