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
      deg = abs(deg)
      coordinate = -(deg + minute/60 + sec/3600)
    else:
      coordinate = deg + minute/60 + sec/3600
    return coordinate

def extract_info_from_location(location):
    """Extracts detailed information from a location string."""
    parts = location.split(', ')
    lat_str = parts[0].split('Latitude')[1].strip()
    lon_str = parts[1].split('Longitude')[1].strip()
    latitude = extract_coordinate_info(lat_str)
    longitude = -(extract_coordinate_info(lon_str))
    datum = parts[1].split('"')[1].split()[0]
    datum = datum.rsplit('<br/></dd>')
    datum = datum[0]
    try:
        elevation = parts[3].split('Datum of gage:')[1].split()[0]
        # Convert feet to square meters
        elevation = float(locale.atof(elevation)) * 0.3048
        vertical_datum = parts[3].split('feet above')[1].split()[0]
        vertical_datum = vertical_datum.rsplit('.')
        vertical_datum = vertical_datum[0]
    except Exception as e:
        print(f"No Elevation Data: {e}")
        elevation = np.nan
        vertical_datum = ''

    try:
        land_surface_altitude = parts[3].split('Land surface altitude:')[1].split()[0]
        # Convert feet to square meters
        land_surface_altitude = float(locale.atof(land_surface_altitude)) * 0.3048
        datum_land_surface_altitude = parts[3].split('feet above')[1].split()[0]
        datum_land_surface_altitude = datum_land_surface_altitude.rsplit('.')
        datum_land_surface_altitude = datum_land_surface_altitude[0]
    except Exception as e:
        print(f"No Land Surface Altitude Data: {e}")
        land_surface_altitude = np.nan
        datum_land_surface_altitude = ''

    try:
        drainage_area = parts[3].split('Drainage area:')[1].split()[0]
        # Convert square miles to square kilometers
        drainage_area = float(locale.atof(drainage_area)) * 2.58999
    except Exception as e:
        print(f"No Drainage Area Data: {e}")
        drainage_area = np.nan

    # Extract other information
    try:
        county = parts[1].split('<dd>')[1].strip()
    except Exception as e:
        county = parts[1]
        county = county.rsplit('\n')
        county = county[1]
    territory = parts[2]
    try:
        hydrologic_unit = parts[3].split('Hydrologic Unit')[1].split()[0]
        hydrologic_unit = hydrologic_unit.rsplit('</dd>')
        hydrologic_unit = hydrologic_unit[0]
    except Exception as e:
        print(f"No Hydrologic Unit Data: {e}")
        hydrologic_unit = ''

    return latitude, longitude, datum, elevation, vertical_datum, land_surface_altitude, \
           datum_land_surface_altitude, drainage_area, hydrologic_unit, territory, county

def process_station(agency, site, name, state, link):
    """Processes a single station and extracts required information."""
    print(agency, ' - ', site, ' - ', name, ' - ', state, ' - ', link)
    url = f'https://nwis.waterdata.usgs.gov/nwis/inventory/?{link}&agency_cd={agency}'
    print(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    information = soup.find("div", {"id": "stationTable"})

    return extract_info_from_location(str(information))

# Read the DataFrame
stations_df = pd.read_excel('/Users/jorge/Documents/USA_Stations_Q_test.xlsx')

# Process each station and collect results
results = []
for row in stations_df.itertuples():
    lat, lon, datum, elevation, vertical_datum, lsal, lsal_datum, drainage_area, hydrologic_unit,\
    territory, county  = process_station(row.Agency, row._2, row._3, row.State, row.Hyperlink)
    results.append([row.Agency, row._2, row._3, row.State, row.Hyperlink, lat, lon, datum,
                    elevation, vertical_datum, lsal, lsal_datum, drainage_area, hydrologic_unit, territory, county])

# Create a new DataFrame from the results
columns = ['Agency', 'Site Number', 'Site Name', 'State', 'Hyperlink', 'Latitude', 'Longitude', 'Datum',
           'Elevation (m.a.s.l.)', 'Vertical Datum', 'Land surface altitude (m.a.s.l.)', 'Land surface Datum',
           'Hydrologic Unit', 'Drainage Area (km2)', 'Territory', 'County']
processed_stations_df = pd.DataFrame(results, columns=columns)

# Save the processed data to a CSV file
processed_stations_df.to_csv('/Users/jorge/Documents/Hydrological_Data/America/USA/USA_Stations_Q_v1.csv', index=False)