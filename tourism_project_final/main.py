from fastapi import FastAPI, Body, Query, Request
from typing import Literal
from fastapi.responses import HTMLResponse, Response  # Import HTMLResponse
import numpy as np
import uvicorn
import requests
from collections import Counter
import json
import pandas as pd
import plotly.express as px
import warnings
from plotly.offline import plot
import plotly.graph_objects as go
warnings.filterwarnings("ignore", "is_categorical_dtype")
warnings.filterwarnings("ignore", "use_inf_as_na")

app = FastAPI()


@app.get("/weather")
def get_weather(place: str = None):
    """Fetches weather information based on place entered, along with findings and recommendations for
    the weekly forecast, and a long range forecast based with Farmer's Almanac data with recommendations
    of when to visit San Francisco.

    Args:
        place (optional): identifier for weather information of the location

    Returns:
        HTML content about the short term and long range forecast to display on a webpage,
        If no place parameter is queried, a general HTML page displays with links for the
        various place parameters
    """

    # Display if a parameter query is entered into the URL
    if place:
        # Assign URL to variable: url of the json weather forecast of SF locations
        if place == 'DowntownSF':
            url = 'https://api.weather.gov/gridpoints/MTR/84,105/forecast'
        elif place == 'SFO':
            url = 'https://api.weather.gov/gridpoints/MTR/85,98/forecast'
        elif place == 'SJC':
            url = 'https://api.weather.gov/gridpoints/MTR/98,83/forecast'
        else:
            url = 'https://api.weather.gov/gridpoints/MTR/91,101/forecast'
        r = requests.get(url)

        # parse in as a JSON
        json_data = r.json()

        weather = {
            'DowntownSF': json_data['properties']['periods'],
            'SFO': json_data['properties']['periods'],
            'SJC': json_data['properties']['periods'],
            'OAK': json_data['properties']['periods']
        }

        # Get the icon images for the forecast
        forecast1 = weather[place][0]['icon']
        forecast2 = weather[place][1]['icon']
        forecast3 = weather[place][2]['icon']
        forecast4 = weather[place][3]['icon']
        forecast5 = weather[place][4]['icon']
        forecast6 = weather[place][5]['icon']

        """-------------------------------------------------------------------------------------------------------------
        This section is for setting up the css and html information            
        -------------------------------------------------------------------------------------------------------------"""

        # Cascading style sheet
        my_css ="""
        <style>
           /* Add some CSS styles for a fancy look */
           body {
           font-family: Arial, sans-serif;
           background-color: #FFD4C5;
           text-align: left;
           padding: 50px;
           }
           h0 {
           color: #000000;
           font-size: 45px;
           margin-bottom: 20px;
           text-align: left;
           }
           h1 {
           color: #007bff;
           font-size: 36px;
           margin-bottom: 20px;
           text-align: left;
           }
           p {
           color: #333;
           font-size: 18px;
           }
        </style>
        """

        # HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
           <h0>
              <meta charset="UTF-8">
              <title>Weather in {}</title>
              <style></style>
           </h0>
           <body>
              <p><a href="/weather">Go to Main Weather Page</a></p>
              <h1>Short Term Weather in {}</h1>
              <p><img src="{}" alt="Icon"> <b>{}</b> : {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              
              <h1>Short Term Weather Analysis </h1>
              <p> {} </p>
              <p> {} </p>
              <p> {} </p>
              <p> <b>Recommendations:</b> {} </p>
           </body>
        </html>
        """

        def weather_recommendation(json_data):
            """
            This function prints out recommended packing items and to plan on indoor/outdoor activities
             based on the short term weather

            Parameters:
            json_data of the Place parameter, either DowntownSF, SFO, SJC, or OAK

            Returns:
            str: Findings and recommended packing items due to the weather forecast
            """

            # Load the file and print out the keys
            print('\n-----HOMEWORK 3 OUTPUT-----')

            # Get the weather forecast portion of the data
            weather_forecast = json_data['properties']['periods']

            temperatures = []
            rain_probs = []
            wind_speed = []

            # Loop through the days and append the data to the lists
            for fc in weather_forecast:
                # Append the average
                temperatures.append(fc['temperature'])

                # Get the rain probability for each day and append to rain_probs
                if fc['probabilityOfPrecipitation']['value'] is None:
                    rain_probs.append(0)
                else:
                    rain_probs.append(fc['probabilityOfPrecipitation']['value'])

                # Get the wind speed for the forecast
                wind_speed.append(int(fc['windSpeed'][:2].strip()))

            # Determine average temperature, rain occurences, and max windspeed
            mean_temperature = np.mean(temperatures)
            count_rain_probs = len(np.where(np.array(rain_probs) > 0)[0])
            max_windspeed = np.max(wind_speed)

            # Print out the findings to the consoles
            print("\nFINDINGS")
            temp_findings = "The forecasted mean temperature for the next 7 days is " + str(round(mean_temperature, 1)) + "F.\n"
            rain_findings = str(count_rain_probs) + " out of " + str(len(rain_probs)) + " forecasts in the next 7 days have a chance of rain.\n"
            wind_findings = "The maximum windspeed in the next 7 days is " + str(max_windspeed) + " mph.\n"
            print(temp_findings)
            print(rain_findings)
            print(wind_findings)
            findings = {}
            findings['temp'] = temp_findings
            findings['rain'] = rain_findings
            findings['wind'] = wind_findings

            # Give recommendations based on temperature, rain probabilities, and windspeed
            def recommender(mean_temperature, count_rain_probs, max_windspeed):
                recommendation = ''
                indoorFlag = 1
                if mean_temperature < 50:
                    recommendation += 'Bring a heavy jacket due to the lower temperature. '
                    indoorFlag = 1
                elif mean_temperature >= 50 and mean_temperature <= 70:
                    recommendation += 'Bring a light jacket or sweater due to the mild temperature. '
                else:
                    recommendation += 'Warm temperatures.'
                    indoorFlag = 0

                if count_rain_probs > 0:
                    indoorFlag += 1
                    recommendation += 'Bring an umbrella or rain jacket just in case. '
                else:
                    indoorFlag += 0
                    recommendation += 'No rain jacket needed. '

                if max_windspeed < 8:
                    indoorFlag += 0
                    recommendation += 'Light to no wind expected. '
                elif max_windspeed >= 8 and max_windspeed < 16:
                    indoorFlag += 0
                    recommendation += 'Consider bringing a jacket for the wind. '
                else:
                    indoorFlag += 1
                    recommendation += 'Strong sustained winds or gusts. '

                if indoorFlag > 0:
                    recommendation += 'Have some indoor activities planned.'
                else:
                    recommendation += 'Outdoor activities should be fine.'
                return recommendation

            return findings,recommender(mean_temperature, count_rain_probs, max_windspeed)

        findings_str, recommendation_str = weather_recommendation(json_data)
        print('\nWEATHER RECOMMENDATIONS\n')
        print(recommendation_str)



        """----------------------------------------------------------------------------------------------------------"""

        # format the html content with the corresponding {} arguments
        my_page = html_content.format(place, place,
                   forecast1, weather[place][0]['name'],weather[place][0]['detailedForecast'],
                   forecast2, weather[place][1]['name'],weather[place][1]['detailedForecast'],
                   forecast3, weather[place][2]['name'],weather[place][2]['detailedForecast'],
                   forecast4, weather[place][3]['name'], weather[place][3]['detailedForecast'],
                   forecast5, weather[place][4]['name'], weather[place][4]['detailedForecast'],
                   forecast6, weather[place][5]['name'], weather[place][5]['detailedForecast'],
                   findings_str['temp'], findings_str['rain'], findings_str['wind'],recommendation_str
                   )

        # Replace the style strings with the CSS
        my_final_page = my_page.replace('<style></style>', my_css)
        return HTMLResponse(content=my_final_page, media_type="text/html")
    else:
        """------------------------------------------------------------------------------"""
        """       This section is for setting displaying just the /weather page          """
        """------------------------------------------------------------------------------"""
        """----------------------------------------------------------------------------------------------------------"""

        def weather_plots():
            """
            This function creates a dataframe to display on a map plot on the main weather page

            Parameters:
            None

            Returns:
            str: This function returns html content for plotting SF locations on a map and displaying the current
            weather at that location.
            """
            ll = [[37.7937, -122.3965], [37.6193, -122.3816], [37.3387, -121.8853], [37.7191, -122.2195]]
            SF_url = 'https://api.weather.gov/gridpoints/MTR/84,105/forecast'
            SFO_url = 'https://api.weather.gov/gridpoints/MTR/85,98/forecast'
            SJC_url = 'https://api.weather.gov/gridpoints/MTR/98,83/forecast'
            OAK_url = 'https://api.weather.gov/gridpoints/MTR/91,101/forecast'
            r_sf = requests.get(SF_url)
            r_sfo = requests.get(SFO_url)
            r_sjc = requests.get(SJC_url)
            r_oak = requests.get(OAK_url)

            # parse in as a JSON
            json_sf = r_sf.json()
            json_sfo = r_sfo.json()
            json_sjc = r_sjc.json()
            json_oak = r_oak.json()

            place_name = ['DowntownSF', 'SFO', 'SJC', 'OAK']
            coord_df = pd.DataFrame(columns=['place', 'lat', 'long', 'current_weather'])
            coord_df['place'] = place_name
            try:
                if 'properties' in json_sf and 'periods' in json_sf['properties']:
                    coord_df['current_weather'][0] = json_sf['properties']['periods'][0]['detailedForecast']
                else:
                    coord_df['current_weather'][
                        0] = "Weather.gov Forecast Grid Expired, current service alert occurring"
            except (KeyError, IndexError):
                coord_df['current_weather'][0] = "Error retrieving forecast data (check API response format)"
            try:
                if 'properties' in json_sfo:
                    coord_df['current_weather'][1] = json_sfo['properties']['periods'][0]['detailedForecast']
                else:
                    coord_df['current_weather'][
                        1] = "Weather.gov Forecast Grid Expired, current service alert occurring"
            except (KeyError, IndexError):
                coord_df['current_weather'][1] = "Error retrieving forecast data (check API response format)"

            try:
                if 'properties' in json_sjc:
                    coord_df['current_weather'][2] = json_sjc['properties']['periods'][0]['detailedForecast']
                else:
                    coord_df['current_weather'][
                        2] = "Weather.gov Forecast Grid Expired, current service alert occurring"
            except (KeyError, IndexError):
                coord_df['current_weather'][2] = "Error retrieving forecast data (check API response format)"

            try:
                if 'properties' in json_oak:
                    coord_df['current_weather'][3] = json_oak['properties']['periods'][0]['detailedForecast']
                else:
                    coord_df['current_weather'][
                        3] = "Weather.gov Forecast Grid Expired, current service alert occurring"
            except (KeyError, IndexError):
                coord_df['current_weather'][3] = "Error retrieving forecast data (check API response format)"

            # Fill the dataframe with lat/long
            for i in range(len(place_name)):
                coord_df['lat'][i] = ll[i][0]
                coord_df['long'][i] = ll[i][1]

            # Create the map plot
            fig = px.scatter_mapbox(coord_df, title='Downtown San Francisco and Airports',
                                    lat="lat", lon="long", hover_name = 'place', text = 'current_weather', zoom=8, height=500, width=850)
            fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker_size=18)
            html_div = plot(fig, output_type='div', include_plotlyjs=False)

            return html_div

        # Call the weather plot function and put it into variable
        fig_html = weather_plots()

        my_css = """
        <style>
           /* Add some CSS styles for a fancy look */
           body {
           font-family: Arial, sans-serif;
           background-color: #FFD4C5;
           text-align: center;
           padding: 50px;
           }
           h0 {
           color: #000000;
           font-size: 45px;
           margin-bottom: 20px;
           text-align: center;
           }
           h1 {
           color: #007bff;
           font-size: 36px;
           margin-bottom: 20px;
           text-align: center;
           }
           p {
           color: #333;
           font-size: 18px;
           }
           .my-div {
            width: fit-content;  /* Set the desired width */
            margin: 0 auto;  /* Center horizontally */
            border-style: solid;
            border-width: 2px;
            border-color: black;
        }
        </style>
        """
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
           <head>
              <meta charset="UTF-8">
              <title>Weather in San Francisco</title>
              <style></style>
              <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFWeatherLogo.jpg?raw=true" alt="Icon"> </p>
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Issues In Downtown San Francisco</title>
                    <!-- Include Plotly.js -->
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
           </head>
           <body>
              <h1>Places</h1>
              <p>Check future weather at <a href="/weather?place=DowntownSF">Downtown SF</a>, <a href="/weather?place=SFO">SFO</a>, <a href="/weather?place=SJC">SJC</a>, or <a href="/weather?place=OAK">OAK</a></p>
              <p><a href="/">or Go to Main Page</a></p>
                
                  <h1>Current Weather in San Francisco and Airports</h1>
                  <p> View current weather imported from weather.gov</p>

                <!-- Display the Plotly figure -->
                <div class="my-div">
                {}
                </div>
              <h1>General San Francisco Climate Information</h1>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/weather_plots/barplot.png" alt="Icon" style="border: 2px solid black;"> </p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/weather_plots/lineplot.png" alt="Icon" style="border: 2px solid black;"> </p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/weather_plots/wordcloud.png" alt="Icon" style="border: 2px solid black;"> </p>
              
           </body>
        </html>
        """
        my_page = html_content.format(fig_html)
        my_final_page = my_page.replace('<style></style>', my_css)
        return HTMLResponse(content=my_final_page, media_type="text/html")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """<!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Welcome to Our Website!</title>
          <style>
             /* Add some CSS styles for a fancy look */
             body {
             font-family: Arial, sans-serif;
             background-color: #FFD4C5;
             text-align: center;
             padding: 50px;
             }
             h1 {
             color: #007bff;
             font-size: 36px;
             margin-bottom: 20px;
             }
             p {
             color: #333;
             font-size: 18px;
             }
          </style>
          <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFTourismLogo.jpg?raw=true" alt="Icon"> </p>
       </head>
       <body>
          <h1>Welcome to ABC to the E page for San Francisco tourism !</h1>
          <p>Explore our content to discover San Francisco food spots and landmarks. Check the latest transportation, weather, and safety information!</p>
          <p><a href="/attractions">Attractions</a></p>
          <p><a href="/restaurants">Restaurants</a></p>
          <p><a href="/weather">Weather</a></p>
          <p><a href="/transportation">Transportation</a></p>
          <p><a href="/safety">Safety</a></p>
       </body>
    </html>"""
    return HTMLResponse(content=html_content)


@app.get("/transportation")
def get_transportation():
    """Fetches 511 traffic event data to show html content of areas to avoid in the Bay Area.

    Args:
        None

    Returns:
        HTML content about current traffic alerts and roads to avoid.
    """

    """------------------------------------------------------------------------------"""
    """This section is used for reading in 511 JSON data and providing recommendations """
    """------------------------------------------------------------------------------"""
    def transportation_recommendation():
        """
        This function prints out recommendations due to 511 traffic alerts

        Parameters:
        None

        Returns:
        str, findings and recommendations are printed out on the console and return in a string to display in html format
        """
        # Open the JSON file with the appropriate encoding

        url = 'https://api.511.org/Traffic/Events?api_key=25d61f5c-8297-44b5-815b-c6912d440fba&format=json'
        r = requests.get(url)

        # parse in as a JSON
        traffic_json = json.loads(r.content.decode('utf-8-sig'))
        traffic_events = traffic_json['events']

        event_type, areas, roads = [], [], []
        # Loop through the days and append the data to the lists
        for te in traffic_events:
            event_type.append(te['event_type'])
            areas.append(te['areas'][0]['name'])
            roads.append(te['roads'][0]['name'])

        # Create traffic dataframe from mapping
        traffic_df = pd.DataFrame(columns=['event', 'type', 'lat', 'long', 'headline'])
        for i in range(len(traffic_events)):
            traffic_df.loc[i, 'event'] = traffic_events[i]['id']
            traffic_df.loc[i, 'type'] = traffic_events[i]['event_type']
            traffic_df.loc[i, 'lat'] = traffic_events[i]['geography']['coordinates'][1]
            traffic_df.loc[i, 'long'] = traffic_events[i]['geography']['coordinates'][0]
            traffic_df.loc[i, 'headline'] = traffic_events[i]['headline']

        # Create the map plot
        fig = px.scatter_mapbox(traffic_df, title='Bay Area Traffic Events',
                                lat="lat", lon="long", hover_name='type', text=traffic_df.headline.str.wrap(30).apply(lambda x: x.replace('\n', '<br>')), zoom=8, height=500,
                                width=850)
        fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_traces(marker_size=18)
        html_div = plot(fig, output_type='div', include_plotlyjs=False)


        # Count up the different events, areas, and roads mentioned
        event_count = Counter(event_type)
        area_count = Counter(areas)
        road_count = Counter(roads)

        print('FINDINGS\n')
        transpo_findings_str = 'Currently there are ' + str(len(event_type)) + ' traffic events in the San Francisco Bay Area:'
        print(transpo_findings_str)
        transpo_findings_str += '<br>'
        for item, count in event_count.items():
            print(f'{item}: {count}')
            transpo_findings_str += f'{item}: {count}\n<br>'

        # Calculate the total count for areas
        area_total_count = sum(area_count.values())
        # Normalize counts to percentages
        normalized_area_counts = {item: count / area_total_count * 100 for item, count in area_count.items()}
        # Print normalized percentages
        print('\nBreakdown of where the traffic events are occuring:')
        transpo_findings_str += '<br>Breakdown of where the traffic events are occuring:<br>'
        high_areas = ''
        for area, percentage in normalized_area_counts.items():
            print(f'{area}: {percentage:.1f}%')
            transpo_findings_str += f'{area}: {percentage:.1f}%<br>'
            if percentage >= 20:
                high_areas += f'({area})'

        print('\nRoads with more than one type of traffic event are occuring:')
        transpo_findings_str +='<br>Roads with more than one type of traffic event are occuring:<br>'
        avoid_roads = ''
        for item, count in road_count.items():
            if count > 1:
                print(f'{item}: {count}')
                transpo_findings_str += f'{item}: {count}<br>'
                avoid_roads += f'{item} '

        print('\nRECOMMENDATIONS')
        transpo_rec_str= 'Based on the traffic alerts, most traffic events are occuring in: ' + str(high_areas) +\
              '. Expect delays in these areas and consider avoiding: ' + str(avoid_roads)
        print(transpo_rec_str)

        return transpo_findings_str,transpo_rec_str, html_div
    transpo_f, transpo_rec, html_div = transportation_recommendation()

    """------------------------------------------------------------------------------"""
    """This section is for setting up the css and html information for transportation"""
    """------------------------------------------------------------------------------"""

    # Cascading style sheet
    my_css = """
            <style>
               /* Add some CSS styles for a fancy look */
               body {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: center;
               padding: 50px;
               }
               h0 {
               color: #000000;
               font-size: 45px;
               margin-bottom: 20px;
               text-align: center;
               }
               h1 {
               color: #007bff;
               font-size: 36px;
               margin-bottom: 20px;
               text-align: center;
               }
               p {
               color: #333;
               font-size: 18px;
               }
                .my-div {
                width: fit-content;  /* Set the desired width */
                margin: 0 auto;  /* Center horizontally */
                border-style: solid;
                border-width: 2px;
                border-color: black;
            </style>
            """
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Transportation in San Francisco</title>
          <style></style>
          <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFTransportationLogo.jpg?raw=true" alt="Icon"> </p>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Traffic Alerts in San Francisco</title>
            <!-- Include Plotly.js -->
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Traffic Alerts:</h1>
            <!-- Display the Plotly figure -->
                <div class="my-div">
                    {}
                </div>
          <p>{}</p>
          <p><b>Recommendations: </b>{}</p>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format(html_div, transpo_f, transpo_rec)

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")

@app.get("/attractions", response_class=HTMLResponse)
def get_attractions():
    # Cascading style sheet
    my_css = """
            <style>
               /* Add some CSS styles for a fancy look */
               body {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: center;
               padding: 50px;
               }
               h0 {
               color: #000000;
               font-size: 45px;
               margin-bottom: 20px;
               text-align: center;
               }
               h1 {
               color: #007bff;
               font-size: 36px;
               margin-bottom: 20px;
               text-align: center;
               }
               p {
               color: #333;
               font-size: 18px;
               }
                .my-div {
                width: fit-content;  /* Set the desired width */
                margin: 0 auto;  /* Center horizontally */
                border-style: solid;
                border-width: 2px;
                border-color: black;
            </style>
            """
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Attractions in San Francisco</title>
          <style></style>
          <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/SFAttractionLogo.jpg" alt="Icon"> </p>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Attraction Stuff:</h1>

          <p><b>Recommendations: </b></p>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format()

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")

@app.get("/safety", response_class=HTMLResponse)
def get_safety():
    # Cascading style sheet
    my_css = """
            <style>
               /* Add some CSS styles for a fancy look */
               body {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: center;
               padding: 50px;
               }
               h0 {
               color: #000000;
               font-size: 45px;
               margin-bottom: 20px;
               text-align: center;
               }
               h1 {
               color: #007bff;
               font-size: 36px;
               margin-bottom: 20px;
               text-align: center;
               }
               p {
               color: #333;
               font-size: 18px;
               }
                .my-div {
                width: fit-content;  /* Set the desired width */
                margin: 0 auto;  /* Center horizontally */
                border-style: solid;
                border-width: 2px;
                border-color: black;
            </style>
            """
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Safety in San Francisco</title>
          <style></style>
          <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/SFSafetyLogo.jpg" alt="Icon"> </p>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Safety Stuff:</h1>

          <p><b>Recommendations: </b></p>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format()

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")

@app.get("/restaurants", response_class=HTMLResponse)
def get_restaurants():
    # Cascading style sheet
    my_css = """
            <style>
               /* Add some CSS styles for a fancy look */
               body {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: center;
               padding: 50px;
               }
               h0 {
               color: #000000;
               font-size: 45px;
               margin-bottom: 20px;
               text-align: center;
               }
               h1 {
               color: #007bff;
               font-size: 36px;
               margin-bottom: 20px;
               text-align: center;
               }
               p {
               color: #333;
               font-size: 18px;
               }
                .my-div {
                width: fit-content;  /* Set the desired width */
                margin: 0 auto;  /* Center horizontally */
                border-style: solid;
                border-width: 2px;
                border-color: black;
            </style>
            """
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Safety in San Francisco</title>
          <style></style>
          <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/SFRestaurantLogo.jpg" alt="Icon"> </p>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Restaurant Stuff:</h1>

          <p><b>Recommendations: </b></p>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format()

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")




# Main function
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
