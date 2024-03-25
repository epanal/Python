from flask import Flask, request
import numpy as np
import requests
import datetime
from collections import Counter
import json
import pandas as pd
import plotly.express as px
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
from bs4 import BeautifulSoup

app = Flask(__name__)

my_css = """
            <style>
               /* Add some CSS styles for a fancy look */
               html {
                    display: flex;
                    justify-content: center;
                }
               body {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: center;
               padding: 0px;
               }           
               body2 {
               font-family: Arial, sans-serif;
               background-color: #FFD4C5;
               text-align: left;
               padding: 0px;
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
               h3 {
               color: #000000;
               font-size: 45px;
               margin-bottom: 20px;
               text-align: left;
               }
               h4 {
               color: #007bff;
               font-size: 36px;
               margin-bottom: 20px;
               text-align: left;
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
                div.content { width: 1000px}


            </style>
            """

@app.route('/')
def root():
    html_content = """<!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Welcome to Our Website!</title>
          <style>
             /* Add some CSS styles for a fancy look */
             html {
                    display: flex;
                    justify-content: center;
                }
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
             div.content { width: 1000px}
          </style>
          <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFTourismLogo.jpg?raw=true" alt="Icon"> </p>
       </head>
       <body>
          <div class"content">
          <h1>Welcome to ABC to the E page for San Francisco tourism !</h1>
          <p>Explore our content to discover San Francisco food spots and landmarks. Check the latest transportation, weather, and safety information!</p>
          <p><a href="/attractions">Attractions</a></p>
          <p><a href="/restaurants">Restaurants</a></p>
          <p><a href="/safety">Safety</a></p>
          <p><a href="/weather">Weather</a></p>
          <p><a href="/transportation">Transportation</a></p>
          </div>
       </body>
    </html>"""
    return html_content


@app.route("/weather")
def get_weather():
    place = request.args.get('place')
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

        # HTML content
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
           <h3>
              <meta charset="UTF-8">
              <title>Weather in {}</title>
              <style></style>
           </h3>
           <body2>
              <p><a href="/weather">Go to Main Weather Page</a></p>
              <h4>Short Term Weather in {}</h4>
              <p><img src="{}" alt="Icon"> <b>{}</b> : {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
              <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>

              <h4>Short Term Weather Analysis </h4>
              <p> {} </p>
              <p> {} </p>
              <p> {} </p>
              <p> <b>Recommendations:</b> {} </p>
           </body2>
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
        return my_final_page
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

            coord_df.current_weather = coord_df.current_weather.str.wrap(40)
            coord_df.current_weather = coord_df.current_weather.apply(lambda x: x.replace('\n', '<br>'))

            # Create the map plot
            fig = px.scatter_mapbox(coord_df, title='Downtown San Francisco and Airports',
                        lat="lat", lon="long", hover_name='place', text='current_weather', zoom=8, height=500,
                        width=850)
            fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_traces(marker_size=18)
            html_div = plot(fig, output_type='div', include_plotlyjs=False)

            return html_div

        # Call the weather plot function and put it into variable
        fig_html = weather_plots()

        html_content = """
        <!DOCTYPE html>
        <html lang="en">
           <head>
              <meta charset="UTF-8">
              <title>Weather in San Francisco</title>
              <style></style>
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Issues In Downtown San Francisco</title>
                    <!-- Include Plotly.js -->
                    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
           </head>
           <body>
              <div class="content">
              <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFWeatherLogo.jpg?raw=true" alt="Icon"> </p>
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
            </div>
           </body>
        </html>
        """
        my_page = html_content.format(fig_html)
        my_final_page = my_page.replace('<style></style>', my_css)
        return my_final_page
@app.route("/transportation")
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

        #print('FINDINGS\n')
        transpo_findings_str = 'Currently there are ' + str(len(event_type)) + ' traffic events in the San Francisco Bay Area:'
        #print(transpo_findings_str)
        transpo_findings_str += '<br>'
        for item, count in event_count.items():
            #print(f'{item}: {count}')
            transpo_findings_str += f'{item}: {count}\n<br>'

        # Calculate the total count for areas
        area_total_count = sum(area_count.values())
        # Normalize counts to percentages
        normalized_area_counts = {item: count / area_total_count * 100 for item, count in area_count.items()}
        # Print normalized percentages
        #print('\nBreakdown of where the traffic events are occuring:')
        transpo_findings_str += '<br>Breakdown of where the traffic events are occuring:<br>'
        high_areas = ''
        for area, percentage in normalized_area_counts.items():
            #print(f'{area}: {percentage:.1f}%')
            transpo_findings_str += f'{area}: {percentage:.1f}%<br>'
            if percentage >= 20:
                high_areas += f'({area})'

        #print('\nRoads with more than one type of traffic event are occuring:')
        transpo_findings_str +='<br>Roads with more than one type of traffic event are occuring:<br>'
        avoid_roads = ''
        for item, count in road_count.items():
            if count > 1:
                #print(f'{item}: {count}')
                transpo_findings_str += f'{item}: {count}<br>'
                avoid_roads += f'{item} '

        #print('\nRECOMMENDATIONS')
        transpo_rec_str= 'Based on the traffic alerts, most traffic events are occuring in: ' + str(high_areas) +\
              '. Expect delays in these areas and consider avoiding: ' + str(avoid_roads)
        #print(transpo_rec_str)

        return transpo_findings_str,transpo_rec_str, html_div
    transpo_f, transpo_rec, html_div = transportation_recommendation()

    """------------------------------------------------------------------------------"""
    """This section is for setting up the css and html information for transportation"""
    """------------------------------------------------------------------------------"""
    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
       <head>
          <meta charset="UTF-8">
          <title>Transportation in San Francisco</title>
          <style></style>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Traffic Alerts in San Francisco</title>
            <!-- Include Plotly.js -->
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
       </head>
       <body>
          <div class="content">
          <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFTransportationLogo.jpg?raw=true" alt="Icon"> </p>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Traffic Alerts:</h1>
            <!-- Display the Plotly figure -->
                <div class="my-div">
                    {}
                </div>
          <p>{}</p>
          <p><b>Recommendations: </b>{}</p>
          </div>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format(html_div, transpo_f, transpo_rec)

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return my_final_page

@app.route("/attractions")
def get_attractions(
        start: str = datetime.datetime.strftime(datetime.date.today(), "%Y-%m-%d"),
        end: str = datetime.datetime.strftime(datetime.date.today() + datetime.timedelta(days=21), "%Y-%m-%d"),
        family: str = 'yes',
        category: str = None
):
    """
        Accesses Top SF Attractions webpage and Ticketmaster's API to provide information
            on upcoming events in San Francisco and draw insights.
        Args:
            start: The beginning of the desired date range
            end: The end of the desired date range
            family: Filter for family friendly events
            category: Desired category of the event
        Returns:
            HTML content displaying analysis of attractions website and upcoming events
        """

    response = requests.get('https://www.sftravel.com/article/top-20-attractions-san-francisco')

    site = BeautifulSoup(response.text, features="html.parser")
    museums = pd.read_csv('https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/attractions_texts/museums.txt',
                          sep=' ',
                          header=None)
    nature = pd.read_csv('https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/attractions_texts/nature.txt',
                         sep=' ',
                         header=None)
    shops = pd.read_csv('https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/attractions_texts/shops.txt', sep=' ',
                        header=None)

    headers = []
    paragraphs = []
    for header in site.find_all('h2', attrs={"class": ["h3", "h3 sft-member"]}):
        headers.append(header.get_text().strip().split('\n')[0])
        p = ''
        if len(header.get_text().strip().split('\n')) == 1:
            for e in header.next_siblings:
                if e.name == 'p':
                    p += e.get_text() + ' '
        else:
            for stuff in header.get_text().strip().split('\n'):
                p += stuff + ' '
        p = p.replace('\xa0', ' ')
        paragraphs.append(p)

    data = pd.DataFrame({"attraction": headers, "paragraph": paragraphs})

    nature_matches = []
    museums_matches = []
    shops_matches = []

    for i in range(len(paragraphs)):
        museum_words = 0
        nature_words = 0
        shop_words = 0
        for j in range(len(museums)):
            museum_words += paragraphs[i].lower().count(museums.iloc[j, 0])
        museums_matches.append(museum_words)
        for k in range(len(nature)):
            nature_words += paragraphs[i].lower().count(nature.iloc[k, 0])
        nature_matches.append(nature_words)
        for l in range(len(shops)):
            shop_words += paragraphs[i].lower().count(shops.iloc[l, 0])
        shops_matches.append(shop_words)

    data['nature_matches'] = nature_matches
    data['museums_matches'] = museums_matches
    data['shops_matches'] = shops_matches

    data['category'] = data.iloc[:, 2:5].idxmax(axis=1).str.split('_').str[0]
    data.iloc[19, 5] = None

    words = site.find_all('p')
    all_words = ''
    for p in words:
        all_words += p.get_text() + ' '

    all_words = all_words.replace('\n', '').strip()
    all_words = all_words.replace('\xa0', '')

    comment_words = ''

    # split the value
    tokens = all_words.split()

    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    comment_words += " ".join(tokens) + " "

    categories = pd.DataFrame(data['category'].value_counts()).reset_index()
    categories.columns = ['category', 'counts']
    fig2 = px.pie(categories, values='counts', names='category', title='Attraction Categories')

    fig3 = make_subplots(
        rows=3, cols=1, subplot_titles=('Matches on Museums Criteria', 'Matches on Nature Criteria'
                                        , 'Matches on Shops Criteria')
    )

    fig3.add_trace(go.Bar(x=data['attraction'], y=data['museums_matches'], name='Museums'), row=1, col=1)
    fig3.add_trace(go.Bar(x=data['attraction'], y=data['nature_matches'], name='Nature'), row=2, col=1)
    fig3.add_trace(go.Bar(x=data['attraction'], y=data['shops_matches'], name='Shops'), row=3, col=1)
    fig3.update_layout(height=1400, width=1400, title_text="Matches on Each Criteria")

    melted = pd.melt(data, id_vars=['attraction', 'paragraph', 'category'], var_name='column', value_name='matches')
    melted['category'] = melted['column'].str.split('_').str[0]
    fig4 = px.bar(melted, x='attraction', y='matches', color='category',
                  title='Distribution of Matches By Category for Each Attraction')

    # Ticketmaster API analysis
    startDate = datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    endDate = datetime.datetime.strptime(end, "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    city = "San Francisco"
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&startDateTime={startDate}&endDateTime={endDate}&includeFamily={family}&size=200&sort=date,asc&apikey=PwGXOQ1zZdeKvDBUxCw4SReTU0h8leBn"
    response = requests.get(url)
    my_data = response.json()

    event = []
    date = []
    categories = []
    min_prices = []
    max_prices = []
    info = []
    for i in range(len(my_data['_embedded']['events'])):
        name = my_data['_embedded']['events'][i]['name']
        local_date = my_data['_embedded']['events'][i]['dates']['start']['localDate']
        url = my_data['_embedded']['events'][i]['url']
        cat = my_data['_embedded']['events'][i]['classifications'][0]['segment']['name']
        minPrice = None
        maxPrice = None
        event.append(name)
        date.append(local_date)
        categories.append(cat)
        if 'priceRanges' in my_data['_embedded']['events'][i].keys() and 'min' in \
                my_data['_embedded']['events'][i]['priceRanges'][0].keys():
            minPrice = my_data['_embedded']['events'][i]['priceRanges'][0]['min']
            maxPrice = my_data['_embedded']['events'][i]['priceRanges'][0]['max']
            min_prices.append(minPrice)
            max_prices.append(maxPrice)
        else:
            min_prices.append(minPrice)
            max_prices.append(maxPrice)
        if minPrice is None:
            line = f'Event Name: {name} <br>Event Date: {local_date} <br> Event Category: {cat} <br> Get Tickets At: <a href="{url}">{url}</a>'
        else:
            line = f'Event Name: {name} <br>Event Date: {local_date} <br> Event Category: {cat} <br> Price Range: ${minPrice} to ${maxPrice} USD <br> Get Tickets At: <a href="{url}">{url}</a>'
        if category is not None and category == cat:
            info.append(line)
        elif category is None:
            info.append(line)

    data = pd.DataFrame({'event': event,
                         'date': date,
                         'category': categories,
                         'minPrice': min_prices,
                         'maxPrice': max_prices})

    cat_counts = data.groupby(['category']).size().reset_index(name='counts')
    fig1 = px.bar(cat_counts, x="category", y="counts", title="Event Category Counts")

    if category is None:
        fig5 = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Min Price Range by Category", "Max Price Range by Category")
        )

        fig5.add_trace(go.Box(y=data["minPrice"], x=data["category"], name="Min Prices"), row=1, col=1)
        fig5.add_trace(go.Box(y=data["maxPrice"], x=data["category"], name="Max Prices"), row=1, col=2)

        fig5.update_layout(
            yaxis_title='Dollars (USD)'
        )
    else:
        fig5 = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Min Price Range", "Max Price Range")
        )

        fig5.add_trace(go.Box(y=data["minPrice"], name="Min Prices"), row=1, col=1)
        fig5.add_trace(go.Box(y=data["maxPrice"], name="Max Prices"), row=1, col=2)

        fig5.update_layout(
            yaxis_title='Dollars (USD)')

    html_content = """
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <title> Attractions in San Francisco </title>
                            <style></style>

                        </head>
                        <div class="content">
                        <body2>
                            <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/SFAttractionLogo.jpg" alt="Icon"> </p>
                            <p><a href="/">Go back to Main Page</a></p>
                            <h1>Top Attractions in San Francisco</h1>
                            <p> The following information is based on the Top 20 Attractions in San Francisco as recommended
                                by <a href="https://www.sftravel.com/article/top-20-attractions-san-francisco">
                                sftravel.com</a> <br> </p>
                            <p> Word Cloud for the words used to describe each of the attractions. <br> </p>
                            <h1> <img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/attraction_plots/wordcloud_attractions.png" border="1"> </h1>
                            <p> No surprise, words related to the location, San Francisco, city, bay, etc. are most common.
                                But we also see some words relating to tourism like bridge, view, garden and visitor
                                are also quite common. </p>
                            <p><div class="my-div"> {} </div></p>
                            <p> Here we have a pie chart showing the distribution of categories amongst the attractions
                                listed in the site. Nature related attractions are the most common, museums and shop
                                attractions are tied for 2nd most common. </p>
                            <p> <div class="my-div"> {} </div> </p>
                            <p> Here we have bar charts showing the word matches in the descriptions for each attraction
                                for each category. As expected, based on the pie chart, nature has the most matches most
                                often followed by shops and museums. That said, shops does have the strongest match, 
                                with The Ferry Building having 9 matches in the shop category. </p>
                            <p>  {} </p>
                            <p> Here we have a stacked bar chart showing the distributions of matches by category for
                                each attraction. Most have a mix of matches between nature, museums and/or shops. </p>
                            <h1>Recommendations</h1>
                            <p> <b> For those looking for a museum: </b> Museum of the African Diaspora,
                                the San Francisco Zoo and Gardens or the San Francisco Museum of Modern Art. <br> 
                                <b> For those looking for a nature attraction:</b> PIER 39, The Presidio, de Young Museum,
                                or Salesforce Park. <br> 
                                <b> For those looking for shops: </b> The Ferry Building.</p>

                            <h1> Ticket Information for Upcoming Events in San Francisco </h1>
                            <p> The following summarizes the upcoming events happening in San Francisco, based on
                                data obtained through Ticketmaster's Discovery API. </p>
                            <p> <b> Choose a category from: </b> {} <br> </p>
                            <p> <b>Category Chosen: {} </b> <br> </p>
                            <p> <b>Filtered to family friendly events only:</b>  {}</p>
                            <p> <b>Date Range of the Current Query: </b>  {} to {}</p>
                            <p> <b>Number of Events that fit the search query (max 200):</b>  {}</p>
                            <p> <div class="my-div">{} </div> </p>
                            <p> <div class="my-div">{} </div> </p>
                            <p> <b> Upcoming Events in order of Date (earliest first!): </b> <br> </p>
                            <p> {} </p>
                        </div>
                        </body>

                        </html>
                        """

    # adding all the dynamic data to the html code
    my_page = html_content.format(fig2.to_html(full_html=False),
                                  fig3.to_html(full_html=False),
                                  fig4.to_html(full_html=False),
                                  data['category'].unique(),
                                  category, family,
                                  start, end,
                                  len(info),
                                  fig1.to_html(full_html=False),
                                  fig5.to_html(full_html=False),
                                  "<br>".join([f"{i} <br>" for i in info])
                                  )
    # adding the style settings to html
    final = my_page.replace('<style></style>', my_css)
    return final


@app.route("/safety")
def get_safety():
    api_url = "https://data.sfgov.org/resource/wg3w-h783.json"

    # parameter filters
    params = {
        # "$limit": 1000,
        "$$app_token": "qHVb4aAcnhiRAx0wHvI9NxNxK",
        "$select": "incident_date, incident_time, analysis_neighborhood, incident_category",
        "$order": "incident_date DESC",
    }

    def fetch_data(url, parameters):
        try:
            response = requests.get(url, params=parameters)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return None

    # fetch data from API
    data = fetch_data(api_url, params)
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the API")

    # analyze data for crime count by district, incident count by category, day vs night count, and date range
    district_crime_count = {}
    incident_category_count = {}
    day_count = 0
    night_count = 0
    dates = []

    for incident in data:
        district = incident.get("analysis_neighborhood", "Unknown")
        district_crime_count[district] = district_crime_count.get(district, 0) + 1

        category = incident.get("incident_category", "Unknown")
        incident_category_count[category] = incident_category_count.get(category, 0) + 1

        incident_time = incident.get("incident_time", "")
        if incident_time:
            hour = int(incident_time.split(":")[0])
            if 6 <= hour < 18:
                day_count += 1
            else:
                night_count += 1

        incident_date = incident.get("incident_date", "")
        if incident_date:
            dates.append(incident_date)

    # sort crime count by district and incident count by category
    sorted_district_crime_count = dict(sorted(district_crime_count.items(), key=lambda x: x[1], reverse=True))
    sorted_incident_category_count = dict(sorted(incident_category_count.items(), key=lambda x: x[1], reverse=True))

    # calculate date range
    min_date = min(dates)[:10]
    max_date = max(dates)[:10]

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
       <body2>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Safety Insights:</h1>

    """
    for district, count in sorted_district_crime_count.items():
        html_content += f"<li>{district}: {count} incidents</li>"

    html_content += """
                </ul>
                <h1>Incident count by category:</h1>
                <ul>
        """
    for category, count in sorted_incident_category_count.items():
        html_content += f"<li>{category}: {count} incidents</li>"

    html_content += """
                </ul>
                <h1>Count of crimes that occurred in the day vs night:</h1>
                <p>Day: {day_count} incidents</p>
                <p>Night: {night_count} incidents</p>
                <h1>Date range of incidents:</h1>
                <p>From: {min_date}</p>
                <p>To: {max_date}</p>
                <h1> Insights from scraping Data </h1>
                <h1><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/safety_plots/bk_image1.jpg" alt="Icon" border="1"> </h1>
                <h1><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/safety_plots/bk_image2.jpg" alt="Icon" border="1"> </h1>
                <h1><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/safety_plots/bk_image3.jpg" alt="Icon" border="1"> </h1>

            </body2>
            </html>
        """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format(day_count=day_count, night_count=night_count, min_date=min_date,
                                           max_date=max_date)

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return my_final_page


@app.route("/restaurants")
def get_restaurants():
    # HTML content
    html_content = """
        <!DOCTYPE html>
        <html lang="en">
           <head>
              <meta charset="UTF-8">
              <title>Restaurants in San Francisco</title>
              <style></style>
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
           </head>
           <body>
           <div class="content">
               <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/SFRestaurantLogo.jpg" alt="Icon"> </p>
              <p><a href="/">Go back to Main Page</a></p>
              <h1>Restaurant Analysis:</h1>
              <p> Below are insights and recommendations on San Francisco Restaurants based on data scraped by Aman Sran from <b> Stacker.com </b> </p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/restaurant_plots/TopRateRestaurants.png" alt="Icon" border="1"> </p>
              <p> <b>Top 3 Restaurants are: </b> </p>
              <p> #1 Akari Japanese Bistro </p>
              <p> #2 Al Carajo </p>
              <p> #3 The check in Lounge </p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/restaurant_plots/ReviewCounts.png" alt="Icon" border="1"> </p>
              <p>The histogram above shows the distribution of review counts for a set of restaurants. Most of the restaurants have a small number of reviews, 
              with a few establishments receiving a larger number. Looking at that, it indicates a skewed distribution where few restaurants are much more reviewed than the rest.</p>

              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/restaurant_plots/RestaurantRatings.png" alt="Icon" border="1"> </p>
              <p>From the pie chart seen above, Each of the restaurant is rated 4.5 and above. This gives consumer some confidence as all the places to eat are rated highly</p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/restaurant_plots/Top10Restaurants.png" alt="Icon" border="1"> </p>
              <p><img src="https://raw.githubusercontent.com/epanal/Python/main/tourism_project_final/restaurant_plots/Top5RestaurantsReviewCount.png" alt="Icon" border="1"> </p>
              <p>This charts above illustrates the proportion of review counts for the top restaurants, with one restaurant dominating the conversation significantly. This visualization highlights where the majority of customer feedback is concentrated, which may suggest a starting point for recommendations based on popularity.</p>
              <h1>Findings: </h1>
              <p><b/>#1 High Overall Ratings: </b>The fact that every restaurant in the sample is rated 4.5 or above indicates an exceptional level of quality across these top San Francisco dining spots. This suggests that diners are generally very satisfied with their experiences.</p>
              <p><b/>#2 Dominant Popularity:</b>The pie chart shows a significant skew towards one restaurant ( Marrakech Magic Theater) in terms of review count, suggesting that it has a dominant popularity, which could be due to various factors like cuisine, service quality, or location.</p>
              <p><b/>#3 Top Rated Diversity: </b>The top three restaurants — Akari Japanese Bistro, Al Carajo, and The Check-In Lounge — represent a variety of dining experiences from different cuisines and styles, indicating that there is no single formula to success when it comes to the preferences of diners in San Francisco. This gives SF tourists the options to indulge in various cuisines of highly rated restaurants.</p>

              <h1>Recommendations: </h1>
              <p><b/>#1 Prioritize Highly Reviewed Restaurants: </b>Tourists of the city can culinary adventure at the most reviewed restaurants. The high number of reviews is a strong indicator of popularity and consistent diner satisfaction. Make sure to reserve in advance, as these spots may be in high demand.</p>
              <p><b/>#2 Explore a Variety of Cuisines:</b>The diversity in top-rated restaurants highlights San Francisco's rich culinary tapestry. Tourists should take advantage of this variety to experience different flavors, from traditional Japanese at Akari Japanese Bistro to the unique offerings at Al Carajo.</p>
              <p><b/>#3 Seek Out Exceptional Experiences: </b>Even restaurants with fewer reviews hold high ratings, which suggests that quality is widespread. Tourists looking for unique and potentially quieter dining experiences should consider these less-reviewed yet highly-rated restaurants.</p>
              <p><b/>#4 Ratings for Confidence: </b>With all reviewed restaurants boasting ratings above 4.5, tourists can confidently explore beyond the top-rated list, knowing that the overall quality across the city's dining establishments is likely to meet their expectations.</p>
              <p><b/>#5 Utilize Review Count as a Guide: </b>While a higher review count often signifies popularity, it doesn't always equate to the best personal experience. Tourists should use the number of reviews as a guide but also consider their personal preferences and seek out restaurants that align with their tastes and desired atmosphere.</p>
           </div>
           </body>
        </html>
        """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format()

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return my_final_page
