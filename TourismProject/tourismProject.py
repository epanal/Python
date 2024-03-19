from fastapi import FastAPI, Body, Query, Request
from typing import Literal
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import uvicorn
import requests
import os
from collections import Counter
import json
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="C:/Users/epana/PycharmProjects/tourismProject/")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("main.html",
                                      {"request": request})

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

        """------------------------------------------------------------------------------"""
        """This section is used for reading in the text files and ranking the text files """
        """------------------------------------------------------------------------------"""
        # Folder Path
        path = r"C:\Users\epana\PycharmProjects\tourismProject"

        # Change the directory
        os.chdir(path)
        print('\n-----HOMEWORK 2 OUTPUT-----\n')
        words = []
        # get weather requirements
        with open("WeatherReqs.txt", encoding='utf-8') as fd:
            for line in fd:
                words.append(line.strip('\n'))
        # print criteria words
        print('Searching Farmers Almanac text files for these words:',words)

        # Function parses through the given file and counts how many types words
        # from the word list appear in the file. This count is returned
        def text_file_counter(word_list, file_path):
            word_count = 0
            with open(file_path, 'r') as file:
                for line in file:
                    words = line.split()
                    for word in words:
                        word = word.strip('.,!?').lower()
                        if word in word_list:
                            word_count += 1
            return word_count

        file_dict = {}

        # iterate through all files
        for file in os.listdir():
            # Check whether file is in text format or not
            if file.endswith(".txt") and file.startswith("FarmersAlmanac"):
                # count how many files
                file_path = f"{path}\{file}"

                # call text file counter
                word_count = text_file_counter(words, file_path)
                file_dict[file] = word_count

        def file_ranks(file_counts, n):
            # Sort the files based on word counts in descending order
            sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

            #print the ranking of the sorted files in the terminal
            for i,j in enumerate(sorted_files):
                print('Rank is:', i+1, j[0],'contains',j[1],'words from the criteria file')
            # Take the top n items
            top_n = sorted_files[:n]
            return top_n

        top_files = file_ranks(file_dict, 3)

        """------------------------------------------------------------------------------"""
        """       This section is for setting up the css and html information            """
        """------------------------------------------------------------------------------"""

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
              
              <h1>Long Term Weather in San Francisco</h1>
              <p> Based on Farmer's Almanac descriptions in the next 90 days, we recommend visiting San Francisco these days due to the forecast
              described with words related to nice weather: </p>
              <p><b>{}</b></p>
              <p><b>{}</b></p>
              <p><b>{}</b></p>
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

        # format the html content with the corresponding {} arguments
        my_page = html_content.format(place, place,
                   forecast1, weather[place][0]['name'],weather[place][0]['detailedForecast'],
                   forecast2, weather[place][1]['name'],weather[place][1]['detailedForecast'],
                   forecast3, weather[place][2]['name'],weather[place][2]['detailedForecast'],
                   forecast4, weather[place][3]['name'], weather[place][3]['detailedForecast'],
                   forecast5, weather[place][4]['name'], weather[place][4]['detailedForecast'],
                   forecast6, weather[place][5]['name'], weather[place][5]['detailedForecast'],
                   findings_str['temp'], findings_str['rain'], findings_str['wind'],recommendation_str,
                   top_files[0][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip(),
                   top_files[1][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip(),
                   top_files[2][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip()
                   )

        # Replace the style strings with the CSS
        my_final_page = my_page.replace('<style></style>', my_css)
        return HTMLResponse(content=my_final_page, media_type="text/html")
    else:
        """------------------------------------------------------------------------------"""
        """       This section is for setting displaying just the /weather page          """
        """------------------------------------------------------------------------------"""
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
           </head>
           <body>
              <h0>Ethan Panal's Weather Endpoint for Tourism Startup</h0>
              <h1>Places</h1>
              <p>Check weather at <a href="/weather?place=DowntownSF">Downtown SF</a>, <a href="/weather?place=SFO">SFO</a>, <a href="/weather?place=SJC">SJC</a>, or <a href="/weather?place=OAK">OAK</a></p>
              <p><a href="/">or Go to Main Page</a></p>
           </body>
        </html>
        """
        my_page = html_content.format()
        my_final_page = my_page.replace('<style></style>', my_css)
        return HTMLResponse(content=my_final_page, media_type="text/html")


@app.get("/transportation")
def get_transportation():
    """Fetches transportation information related to neighborhoods based on desired type.

    Args:
        None

    Returns:
        HTML content about the top 3 neighborhoods in San Francisco with text files with desired
        transportation types.
    """
    """------------------------------------------------------------------------------"""
    """This section is used for reading in the text files and ranking the text files """
    """------------------------------------------------------------------------------"""

    # Folder Path
    path = r"C:\Users\epana\PycharmProjects\tourismProject"

    # Change the directory
    os.chdir(path)

    transpo_words = []
    # get transportation requirements
    with open("TransportationReqs.txt", encoding='utf-8') as fd:
        for line in fd:
            transpo_words.append(line.lower().strip('\n'))
    # print criteria words
    print('Searching Neighborhood transportation option text files for these words:', transpo_words)

    # Function parses through the given file and counts how many types words
    # from the word list appear in the file. This count is returned
    def text_file_counter(word_list, file_path):
        word_count = 0
        with open(file_path, 'r') as file:
            for line in file:
                words = line.split()
                for word in words:
                    word = word.strip('.,!?').lower()
                    if word in word_list:
                        word_count += 1
        return word_count

    file_dict = {}

    # iterate through all files
    for file in os.listdir():
        # Check whether file is in text format or not
        if file.endswith(".txt") and file.startswith("Neighborhood"):
            # count how many files
            file_path = f"{path}\{file}"

            # call text file counter
            word_count = text_file_counter(transpo_words, file_path)
            file_dict[file] = word_count

    def file_ranks(file_counts, n):
        # Sort the files based on word counts in descending order
        sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

        # print the ranking of the sorted files in the terminal
        for i, j in enumerate(sorted_files):
            print('Rank is:', i + 1, j[0], 'contains', j[1], 'words from the criteria file')
        # Take the top n items
        top_n = sorted_files[:n]
        return top_n

    top_files = file_ranks(file_dict, 3)
    """------------------------------------------------------------------------------"""
    """This section is used for reading in 511 JSON data and providing recommendations """
    """------------------------------------------------------------------------------"""
    def transportation_recommendation():
        """
        This function prints out recommendations due to 511 traffic alerts

        Parameters:
        None

        Returns:
        None, findings and recommendations are printed out on the console
        """
        # Open the JSON file with the appropriate encoding
        with open('511traffic.json', 'r', encoding='utf-8') as file:
            try:
                # Load the JSON data
                data = json.load(file)
                # Process the JSON data as needed
            except json.JSONDecodeError as e:
                print("JSONDecodeError:", e)
        traffic_events = data['events']

        event_type, areas, roads = [], [], []
        # Loop through the days and append the data to the lists
        for te in traffic_events:
            event_type.append(te['event_type'])
            areas.append(te['areas'][0]['name'])
            roads.append(te['roads'][0]['name'])

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
        for area, percentage in normalized_area_counts.items():
            print(f'{area}: {percentage:.1f}%')
            transpo_findings_str += f'{area}: {percentage:.1f}%<br>'

        print('\nRoads with more than one type of traffic event are occuring:')
        transpo_findings_str +='<br>Roads with more than one type of traffic event are occuring:<br>'
        for item, count in road_count.items():
            if count > 1:
                print(f'{item}: {count}')
                transpo_findings_str += f'{item}: {count}<br>'

        print('\nRECOMMENDATIONS')
        transpo_rec_str= 'Based on the traffic alerts, most traffic events are occuring in Alameda followed by San Mateo.' \
              'Expect delays in these areas and consider avoiding CA-84 E, CA-1N, CA-84 W, CA-29N, and I-280 S'
        print(transpo_rec_str)

        return transpo_findings_str,transpo_rec_str
    transpo_f, transpo_rec = transportation_recommendation()

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
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
          <h1>Traffic Alerts:</h1>
          <p>{}</p>
          <p><b>Recommendations: </b>{}</p>
          <h1>Transportation Requirements:</h1>
          <p>You're looking for best neighborhoods with these transportation options <b>{}</b></p>
          <h1>Neighborhood Transportation Options:</h1>
          <p><b>{}</b> contains {} instances of words related to your desired transportation options</p>
          <p><b>{}</b> contains {} instances of words related to your desired transportation options</p>
          <p><b>{}</b> contains {} instances of words related to your desired transportation options</p>
       </body>
    </html>
    """
    # format the html content with the corresponding {} arguments
    my_page = html_content.format(transpo_f, transpo_rec,
                                  transpo_words,
                                  top_files[0][0].replace('Neighborhood', '').replace('-', '').strip(), top_files[0][1],
                                  top_files[1][0].replace('Neighborhood', '').replace('-', '').strip(), top_files[1][1],
                                  top_files[2][0].replace('Neighborhood', '').replace('-', '').strip(), top_files[2][1]
                                  )

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")
# Main function
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
