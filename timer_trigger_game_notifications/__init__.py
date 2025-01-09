import logging
import os
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from azure.eventgrid import EventGridPublisherClient
from azure.core.credentials import AzureKeyCredential

def main(mytimer) -> None:
    data = []
    # No return statement needed if no output binding is used
    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    logging.info('Python timer trigger function executed.')

    # Environment variables
    api_key = os.getenv("SPORTS_API_KEY")
    event_grid_topic = os.getenv("EVENT_GRID_TOPIC_ENDPOINT")
    event_grid_key = os.getenv("EVENT_GRID_TOPIC_KEY")

    # Adjust for Central Time (UTC-6)
    utc_now = datetime.now(timezone.utc)
    central_time = utc_now - timedelta(hours=6)  # Central Time is UTC-6
    today_date = central_time.strftime("%Y-%m-%d")
    
    logging.info(f"Fetching games for date: {today_date}")
    
    # Fetch data from the API
    api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"
    # logging.info(api_url)
     
    try:
        with urllib.request.urlopen(api_url) as response:
            data = json.loads(response.read().decode())
            # logging.info(json.dumps(data, indent=4))  # Debugging: log the raw data
    except Exception as e:
        logging.info(f"Error fetching data from API: {e}")

    # Process games data
    messages = [format_game_data(game) for game in data]
    final_message = "<br>---<br>".join(messages) if messages else "No games available for today."

    # Publish to Event Grid
    try:
        client = EventGridPublisherClient(event_grid_topic, AzureKeyCredential(event_grid_key))
        event = {
            "id": "1",
            "subject": "NBA Game Notification",
            "data": final_message,
            "eventType": "GameResult",
            "dataVersion": "1.0"
        }
        client.send(event)
        
        logging.info("Notifications successfully published to Event Grid.")
    
    except Exception as e:
        logging.info(f"Error publishing to event grid: {e}")
        


def format_game_data(game):
    status = game.get("Status", "Unknown")
    away_team = game.get("AwayTeam", "Unknown")
    home_team = game.get("HomeTeam", "Unknown")
    final_score = f"{game.get('AwayTeamScore', 'N/A')}-{game.get('HomeTeamScore', 'N/A')}"
    start_time = game.get("DateTime", "Unknown")
    channel = game.get("Channel", "Unknown")
    
    # Format quarters
    quarters = game.get("Quarters", [])
    quarter_scores = ', '.join([f"Q{q['Number']}: {q.get('AwayScore', 'N/A')}-{q.get('HomeScore', 'N/A')}" for q in quarters])
    
    if status == "Final":
        return (
            f"Game Status: {status}<br>"
            f"{away_team} vs {home_team}<br>"
            f"Final Score: {final_score}<br>"
            f"Start Time: {start_time}<br>"
            f"Channel: {channel}<br>"
            f"Quarter Scores: {quarter_scores}<br>"
        )
    elif status == "InProgress":
        last_play = game.get("LastPlay", "N/A")
        return (
            f"Game Status: {status}<br>"
            f"{away_team} vs {home_team}<br>"
            f"Current Score: {final_score}<br>"
            f"Last Play: {last_play}<br>"
            f"Channel: {channel}<br>"
        )
    elif status == "Scheduled":
        return (
            f"Game Status: {status}<br>"
            f"{away_team} vs {home_team}<br>"
            f"Start Time: {start_time}<br>"
            f"Channel: {channel}<br>"
        )
    else:
        return (
            f"Game Status: {status}<br>"
            f"{away_team} vs {home_team}<br>"
            f"Details are unavailable at the moment.<br>"
        )