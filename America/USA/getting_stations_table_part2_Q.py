import locale
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

stations_df = pd.read_excel('/Users/jorge/Documents/USA_Stations_Q.xlsx')

agencies = stations_df['Agency'].tolist()
sites = stations_df['Site Number'].tolist()
names = stations_df['Site Name'].tolist()
states = stations_df['State'].tolist()
links = stations_df['Hyperlink'].tolist()

list_stations = []

for agency, site, name, state, link in zip(agencies, sites, names, states, links):

  print(agency, ' - ', site, ' - ', name, ' - ', state, ' - ', link)

  url = 'https://nwis.waterdata.usgs.gov/nwis/inventory/?{0}&agency_cd={1}'.format(link, agency)

  print(url)

  r = requests.get(url)
  html_doc = r.text
  soup1 = BeautifulSoup(html_doc, features='html.parser')
  information = soup1.find_all("div", {"id": "stationTable"})

  location = str(information[0])
  location = location.rsplit(', ')

  coordinates_lat = location[0]
  coordinates_lat = coordinates_lat.rsplit('Latitude')
  coordinates_lat = coordinates_lat[1]
  coordinates_lat = coordinates_lat.rsplit('  ')
  try:
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit('°')
    deg_lat = float(coordinates_lat[0])
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit("'")
    min_lat = float(coordinates_lat[0])
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit('"')
    sec_lat = float(coordinates_lat[0])
    if deg_lat < 0:
      deg_lat = abs(deg_lat)
      lat = -(deg_lat + (min_lat / 60) + (sec_lat / 3600))
    else:
      lat = deg_lat + (min_lat / 60) + (sec_lat / 3600)
    #print(lat)

    coordinates_lon = location[1]
    coordinates_lon = coordinates_lon.rsplit('Longitude')
    coordinates_lon = coordinates_lon[1]
    coordinates_lon = coordinates_lon.rsplit('  ')
    try:
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('°')
      deg_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit("'")
      min_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('"')
      sec_lon = float(coordinates_lon[0])
      lon = -(deg_lon + (min_lon / 60) + (sec_lon / 3600))
      #print(lon)

      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('   ')
      coordinates_lon = coordinates_lon[1]

      try:
        coordinates_lon = coordinates_lon.rsplit('<br/></dd>')
        datum = coordinates_lon[0]
        # print(datum)

        coordinates_lon = coordinates_lon[1]
        coordinates_lon = coordinates_lon.rsplit('<dd>')
        county = coordinates_lon[1]
        # print(county)
      except Exception as e:
        coordinates_lon = coordinates_lon[0]
        coordinates_lon = coordinates_lon.rsplit('<br/>')
        datum = coordinates_lon[0]
        # print(datum)

        county = coordinates_lon[1]
        county = county.rsplit('\n')
        county = county[1]
        # print(county)

        print(e)

      territory = location[2]
      # print(territory)

      try:
        hidrologic_unit = location[3]
        hidrologic_unit = hidrologic_unit.rsplit('Hydrologic Unit ')
        hidrologic_unit = hidrologic_unit[1]
        hidrologic_unit = hidrologic_unit.rsplit('</dd>')
        hidrologic_unit = hidrologic_unit[0]
        # print(hidrologic_unit)
      except Exception as e:
        print(e)
        hidrologic_unit = ''

      try:
        drainage_area = location[3]
        drainage_area = drainage_area.rsplit('Drainage area: ')
        drainage_area = drainage_area[1]
        drainage_area = drainage_area.rsplit(' square miles')
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        drainage_area = float(locale.atof(drainage_area[0])) * 2.58999
        #print(drainage_area)
      except Exception as e:
        print(e)
        drainage_area = np.nan

      try:
        elevation = location[3]
        elevation = elevation.rsplit('Datum of gage:  ')
        elevation = elevation[1]
        elevation = elevation.rsplit(' feet above   ')
        vertical_datum = elevation[1]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        elevation = float(locale.atof(elevation[0])) * 0.3048
        vertical_datum = vertical_datum.rsplit('.')
        vertical_datum = vertical_datum[0]
      except Exception as e:
        print(e)
        elevation = np.nan
        vertical_datum = ''

      try:
        land_surface_altitude = location[3]
        land_surface_altitude = land_surface_altitude.rsplit('Land surface altitude:  ')
        land_surface_altitude = land_surface_altitude[1]
        land_surface_altitude = land_surface_altitude.rsplit('\nfeet above')
        datum_land_surface_altitude = land_surface_altitude[1]
        datum_land_surface_altitude = datum_land_surface_altitude.rsplit('.')
        datum_land_surface_altitude = datum_land_surface_altitude[0]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        land_surface_altitude = float(locale.atof(land_surface_altitude[0])) * 0.3048
      except Exception as e:
        print(e)
        land_surface_altitude = np.nan
        datum_land_surface_altitude = ''

    except Exception as e:
      print(e)
      coordinates_lon = coordinates_lon[0]
      coordinates_lon = coordinates_lon.rsplit(' ')
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('°')
      deg_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit("'")
      min_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('"')
      sec_lon = float(coordinates_lon[0])
      lon = -(deg_lon + (min_lon / 60) + (sec_lon / 3600))
      #print(lon)

      datum = location[1]
      datum = datum.rsplit('"')
      datum = datum[1]
      datum = datum.rsplit('   ')
      datum = datum[1]
      datum = datum.rsplit('<br/>')
      datum = datum[0]
      #print(datum)

      county = location[1]
      county = county.rsplit('"')
      county = county[1]
      county = county.rsplit('   ')
      county = county[1]
      county = county.rsplit('<br/>')
      county = county[1]
      county = county.rsplit('<dd>')
      try:
        county = county[1]
      except Exception as e:
        print(e)
        county = county[0]
        county = county.rsplit('\n')
        county = county[1]
      #print(county)

      territory = location[2]
      # print(territory)

      try:
        hidrologic_unit = location[3]
        hidrologic_unit = hidrologic_unit.rsplit('Hydrologic Unit ')
        hidrologic_unit = hidrologic_unit[1]
        hidrologic_unit = hidrologic_unit.rsplit('</dd>')
        hidrologic_unit = hidrologic_unit[0]
        #print(hidrologic_unit)
      except Exception as e:
        print(e)
        hidrologic_unit = ''

      try:
        drainage_area = location[3]
        drainage_area = drainage_area.rsplit('Drainage area: ')
        drainage_area = drainage_area[1]
        drainage_area = drainage_area.rsplit(' square miles')
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        drainage_area = float(locale.atof(drainage_area[0]))*2.58999
        #print(drainage_area)
      except Exception as e:
        print(e)
        drainage_area = np.nan

      try:
        elevation = location[3]
        elevation = elevation.rsplit('Datum of gage:  ')
        elevation = elevation[1]
        elevation = elevation.rsplit(' feet above   ')
        vertical_datum = elevation[1]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        elevation = float(locale.atof(elevation[0])) * 0.3048
        vertical_datum = vertical_datum.rsplit('.')
        vertical_datum = vertical_datum[0]
      except Exception as e:
        print(e)
        elevation = np.nan
        vertical_datum = ''

      try:
        land_surface_altitude = location[3]
        land_surface_altitude = land_surface_altitude.rsplit('Land surface altitude:  ')
        land_surface_altitude = land_surface_altitude[1]
        land_surface_altitude = land_surface_altitude.rsplit('\nfeet above')
        datum_land_surface_altitude = land_surface_altitude[1]
        datum_land_surface_altitude = datum_land_surface_altitude.rsplit('.')
        datum_land_surface_altitude = datum_land_surface_altitude[0]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        land_surface_altitude = float(locale.atof(land_surface_altitude[0])) * 0.3048
      except Exception as e:
        print(e)
        land_surface_altitude = np.nan
        datum_land_surface_altitude = ''

  except Exception as e:
    coordinates_lat = coordinates_lat[0]
    coordinates_lat = coordinates_lat.rsplit(' ')
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit('°')
    deg_lat = float(coordinates_lat[0])
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit("'")
    min_lat = float(coordinates_lat[0])
    coordinates_lat = coordinates_lat[1]
    coordinates_lat = coordinates_lat.rsplit('"')
    sec_lat = float(coordinates_lat[0])
    if deg_lat < 0:
      deg_lat = abs(deg_lat)
      lat = -(deg_lat + (min_lat / 60) + (sec_lat / 3600))
    else:
      lat = deg_lat + (min_lat / 60) + (sec_lat / 3600)
    # print(lat)

    coordinates_lon = location[1]
    coordinates_lon = coordinates_lon.rsplit('Longitude')
    coordinates_lon = coordinates_lon[1]
    coordinates_lon = coordinates_lon.rsplit('  ')
    try:
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('°')
      deg_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit("'")
      min_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('"')
      sec_lon = float(coordinates_lon[0])
      lon = -(deg_lon + (min_lon / 60) + (sec_lon / 3600))
      # print(lon)

      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('   ')
      coordinates_lon = coordinates_lon[1]

      try:
        coordinates_lon = coordinates_lon.rsplit('<br/></dd>')
        datum = coordinates_lon[0]
        # print(datum)

        coordinates_lon = coordinates_lon[1]
        coordinates_lon = coordinates_lon.rsplit('<dd>')
        county = coordinates_lon[1]
        # print(county)
      except Exception as e:
        coordinates_lon = coordinates_lon[0]
        coordinates_lon = coordinates_lon.rsplit('<br/>')
        datum = coordinates_lon[0]
        # print(datum)

        county = coordinates_lon[1]
        county = county.rsplit('\n')
        county = county[1]
        # print(county)

        print(e)

      territory = location[2]
      # print(territory)

      try:
        hidrologic_unit = location[3]
        hidrologic_unit = hidrologic_unit.rsplit('Hydrologic Unit ')
        hidrologic_unit = hidrologic_unit[1]
        hidrologic_unit = hidrologic_unit.rsplit('</dd>')
        hidrologic_unit = hidrologic_unit[0]
        # print(hidrologic_unit)
      except Exception as e:
        print(e)
        hidrologic_unit = ''

      try:
        drainage_area = location[3]
        drainage_area = drainage_area.rsplit('Drainage area: ')
        drainage_area = drainage_area[1]
        drainage_area = drainage_area.rsplit(' square miles')
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        drainage_area = float(locale.atof(drainage_area[0])) * 2.58999
        # print(drainage_area)
      except Exception as e:
        print(e)
        drainage_area = np.nan

      try:
        elevation = location[3]
        elevation = elevation.rsplit('Datum of gage:  ')
        elevation = elevation[1]
        elevation = elevation.rsplit(' feet above   ')
        vertical_datum = elevation[1]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        elevation = float(locale.atof(elevation[0])) * 0.3048
        vertical_datum = vertical_datum.rsplit('.')
        vertical_datum = vertical_datum[0]
      except Exception as e:
        print(e)
        elevation = np.nan
        vertical_datum = ''

      try:
        land_surface_altitude = location[3]
        land_surface_altitude = land_surface_altitude.rsplit('Land surface altitude:  ')
        land_surface_altitude = land_surface_altitude[1]
        land_surface_altitude = land_surface_altitude.rsplit('\nfeet above')
        datum_land_surface_altitude = land_surface_altitude[1]
        datum_land_surface_altitude = datum_land_surface_altitude.rsplit('.')
        datum_land_surface_altitude = datum_land_surface_altitude[0]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        land_surface_altitude = float(locale.atof(land_surface_altitude[0])) * 0.3048
      except Exception as e:
        print(e)
        land_surface_altitude = np.nan
        datum_land_surface_altitude = ''

    except Exception as e:
      print(e)
      coordinates_lon = coordinates_lon[0]
      coordinates_lon = coordinates_lon.rsplit(' ')
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('°')
      deg_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit("'")
      min_lon = float(coordinates_lon[0])
      coordinates_lon = coordinates_lon[1]
      coordinates_lon = coordinates_lon.rsplit('"')
      sec_lon = float(coordinates_lon[0])
      lon = -(deg_lon + (min_lon / 60) + (sec_lon / 3600))
      # print(lon)

      datum = location[1]
      datum = datum.rsplit('"')
      datum = datum[1]
      datum = datum.rsplit('   ')
      datum = datum[1]
      datum = datum.rsplit('<br/>')
      datum = datum[0]
      # print(datum)

      county = location[1]
      county = county.rsplit('"')
      county = county[1]
      county = county.rsplit('   ')
      county = county[1]
      county = county.rsplit('<br/>')
      county = county[1]
      county = county.rsplit('<dd>')
      try:
        county = county[1]
      except Exception as e:
        print(e)
        county = county[0]
        county = county.rsplit('\n')
        county = county[1]
      # print(county)

      territory = location[2]
      # print(territory)

      try:
        hidrologic_unit = location[3]
        hidrologic_unit = hidrologic_unit.rsplit('Hydrologic Unit ')
        hidrologic_unit = hidrologic_unit[1]
        hidrologic_unit = hidrologic_unit.rsplit('</dd>')
        hidrologic_unit = hidrologic_unit[0]
        # print(hidrologic_unit)
      except Exception as e:
        print(e)
        hidrologic_unit = ''

      try:
        drainage_area = location[3]
        drainage_area = drainage_area.rsplit('Drainage area: ')
        drainage_area = drainage_area[1]
        drainage_area = drainage_area.rsplit(' square miles')
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        drainage_area = float(locale.atof(drainage_area[0])) * 2.58999
        # print(drainage_area)
      except Exception as e:
        print(e)
        drainage_area = np.nan

      try:
        elevation = location[3]
        elevation = elevation.rsplit('Datum of gage:  ')
        elevation = elevation[1]
        elevation = elevation.rsplit(' feet above   ')
        vertical_datum = elevation[1]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        elevation = float(locale.atof(elevation[0])) * 0.3048
        vertical_datum = vertical_datum.rsplit('.')
        vertical_datum = vertical_datum[0]
      except Exception as e:
        print(e)
        elevation = np.nan
        vertical_datum = ''

      try:
        land_surface_altitude = location[3]
        land_surface_altitude = land_surface_altitude.rsplit('Land surface altitude:  ')
        land_surface_altitude = land_surface_altitude[1]
        land_surface_altitude = land_surface_altitude.rsplit('\nfeet above ')
        datum_land_surface_altitude = land_surface_altitude[1]
        datum_land_surface_altitude = datum_land_surface_altitude.rsplit('.')
        datum_land_surface_altitude = datum_land_surface_altitude[0]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        land_surface_altitude = float(locale.atof(land_surface_altitude[0])) * 0.3048
      except Exception as e:
        print(e)
        land_surface_altitude = np.nan
        datum_land_surface_altitude = ''

  list_stations.append([agency, site, name, state, link, lat, lon, datum, elevation, vertical_datum,
                        land_surface_altitude, datum_land_surface_altitude, drainage_area,
                        hidrologic_unit, territory])

list_wells_df = pd.DataFrame(list_stations, columns=['Agency', 'Site Number', 'Site Name',
                                                  'State', 'Hyperlink', 'Latitude', 'Longitude',
                                                  'Datum', 'Elevation (m.a.s.l.)', 'Vertical Datum',
                                                  'Land surface altitude (m.a.s.l.)', 'Land surface Datum',
                                                  'Drainage Area (km2)', 'Hydrologic Unit Code',
                                                  'Territory'])

list_wells_df.set_index('Agency', inplace=True)

print(list_wells_df)

list_wells_df.to_csv("/Users/jorge/Documents/Hydrological_Data/America/USA/USA_Stations_Q.csv")