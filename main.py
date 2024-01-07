import requests
import pandas as pd
from datetime import datetime

csv_file_path = "input.csv"
current_date_time = datetime.now().strftime("%Y%m%d-%H%M")

SoundchartsAppId = "your_soundcharts_appid" # Replace by your Soundcharts AppID
SoundchartsApiKey = "your_soundcharts_api-key" # Replace by your Soundcharts API Key

def getSpotifyListeners(soundcharts_id): # Gets the monthly listeners for a given artists' Soundcharts ID
    api_url = f"https://customer.api.soundcharts.com/api/v2/artist/{soundcharts_id}/streaming/spotify/listeners" # Use the appropriate API call
    headers = {"x-app-id": SoundchartsAppId, "x-api-key": SoundchartsApiKey}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        value = data.get("items", [{}])[0].get("value") # Retrieve the value from the "value" key pair (Spotify monthly listeners)

        if value is not None:
            return value
        else:
            print(f"No valid data found in the response for Soundcharts ID {soundcharts_id}")
        return None
        
    else:
        print(f"Error fetching data for Soundcharts ID {soundcharts_id}. Status code: {response.status_code}")
        return None
        

def generateTable(csv_file): # Generates the expected .csv output file
    print('Fetching artists data...') # Placeholder to inform user that the program is running
    df = pd.read_csv(csv_file)
    rows_list = []  # List to store rows as dictionaries

    for index, row in df.iterrows():
        soundcharts_id = row["soundcharts_id"]
        listeners_value = getSpotifyListeners(soundcharts_id) # Loops through the getSpotifyListeners function going through all the Soundcharts IDs provided in the .csv input file

        if listeners_value is not None:
            row_dict = {
                "backend_id": row.get("backend_id", None),
                "artist_slug": row.get("artist_slug", None),
                "spotify_listeners": listeners_value,
                "date": datetime.today().strftime('%Y-%m-%d')  # Add today's date
            }
            rows_list.append(row_dict)
        else:
            print(f"No valid data found for Soundcharts ID {soundcharts_id}")

    # Check if rows_list is not empty before creating DataFrame
    if rows_list:
        # Convert the list of dictionaries to DataFrame
        result_table = pd.DataFrame(rows_list)

        # Reorder columns with "date" as the second-to-last column
        result_table = result_table[
            ["backend_id", "artist_slug", "date", "spotify_listeners"]
        ]

        # Save the DataFrame to a new CSV file
        output_file_name = "output-" + current_date_time + ".csv"
        result_table.to_csv(output_file_name, index=False)
    else:
        print("No valid data found.")
    print(f'Done! File saved to {output_file_name}.')

generateTable(csv_file_path)
