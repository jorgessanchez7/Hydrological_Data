import locale
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def extract_coordinate_info(coordinate_str):
    """Extracts and computes the coordinate from a string."""
    parts = coordinate_str.split()
    coordinates = parts[0]
    coordinates = coordinates.rsplit('°')
    deg = float(coordinates[0])
    coordinates = coordinates[1]
    coordinates = coordinates.rsplit("'")
    minute = float(coordinates[0])
    coordinates = coordinates[1]
    coordinates = coordinates.rsplit('"')
    sec = float(coordinates[0])
    if deg < 0:
      deg_lat = abs(deg)
      coordinate = -(deg + minute/60 + sec/3600)
    else:
      coordinate = deg + minute/60 + sec/3600
    return coordinate

def extract_info_from_location(location):
    """Extracts detailed information from a location string."""
    try:
        parts = location.split(', ')
        lat_str = parts[0].split('Latitude')[1].strip()
        lon_str = parts[1].split('Longitude')[1].strip()
        latitude = extract_coordinate_info(lat_str)
        longitude = -(extract_coordinate_info(lon_str))

        # Extract other information
        datum = parts[3].split('Datum of gage:')[1].split()[0]
        county = parts[2].split(':')[1].strip()
        hydrologic_unit = parts[4].split('Hydrologic Unit')[1].split()[0]

        # Convert square miles to square kilometers if necessary
        drainage_area = parts[5].split('Drainage area:')[1].split()[0]
        drainage_area = float(locale.atof(drainage_area.replace(' square miles', ''))) * 2.58999

        return latitude, longitude, datum, county, hydrologic_unit, drainage_area
    except Exception as e:
        print(f"Error extracting info: {e}")
        return np.nan, np.nan, '', '', '', np.nan

def process_station(agency, site, name, state, link):
    """Processes a single station and extracts required information."""
    print(agency, ' - ', site, ' - ', name, ' - ', state, ' - ', link)
    url = f'https://nwis.waterdata.usgs.gov/nwis/inventory/?{link}&agency_cd={agency}'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    information = soup.find("div", {"id": "stationTable"})

    if information:
        return extract_info_from_location(str(information))
    else:
        return np.nan, np.nan, '', '', '', np.nan

# Read the DataFrame
stations_df = pd.read_excel('/path/to/your/file.xlsx')

# Process each station and collect results
results = []
for row in stations_df.itertuples():
    lat, lon, datum, county, hydrologic_unit, drainage_area = process_station(row.Agency, row._2, row.Site_Name, row.State, row.Hyperlink)
    results.append([row.Agency, row._2, row.Site_Name, row.State, row.Hyperlink, lat, lon, datum, county, hydrologic_unit, drainage_area])

# Create a new DataFrame from the results
columns = ['Agency', 'Site Number', 'Site Name', 'State', 'Hyperlink', 'Latitude', 'Longitude', 'Datum', 'County', 'Hydrologic Unit', 'Drainage Area (km2)']
processed_stations_df = pd.DataFrame(results, columns=columns)

# Save the processed data to a CSV file
processed_stations_df.to_csv('/path/to/your/output.csv', index=False)