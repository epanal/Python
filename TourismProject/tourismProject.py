from fastapi import FastAPI, Body, Query
from typing import Literal
from fastapi.responses import HTMLResponse  # Import HTMLResponse
from fastapi.templating import Jinja2Templates

import uvicorn
import requests
import os
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
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
             text-align: left;
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
          <p><a href="/food">Food</a></p>
          <p><a href="/weather">Weather</a></p>
          <p><a href="/transportation">Transportation</a></p>
          <p><a href="/safety">Safety</a></p>
       </body>
    </html>
    """

    return HTMLResponse(content=html_content)

@app.get("/weather")
def get_weather(place: str = None):
    """Fetches weather information based on place entered.

    Args:
        place: identifier for weather information of the location

    Returns:
        HTML content about the short term and long range forecast to display on a webpage,
        If no place parameter is queried, a general HTML page displays with links for the
        various place parameters
    """

    # Display if a parameter query is entered into the URL
    if place:
        # Assign URL to variable: url of the json weather forecast of SF locations
        url_downtownSF = 'https://api.weather.gov/gridpoints/MTR/84,105/forecast'
        url_SFO = 'https://api.weather.gov/gridpoints/MTR/85,98/forecast'
        url_SJC = 'https://api.weather.gov/gridpoints/MTR/98,83/forecast'
        url_OAK = 'https://api.weather.gov/gridpoints/MTR/91,101/forecast'

        # send a request using the SF url
        r_dSF = requests.get(url_downtownSF)
        r_SFO = requests.get(url_SFO)
        r_SJC = requests.get(url_SJC)
        r_OAK = requests.get(url_OAK)

        # parse in as a JSON
        json_data_downtownSF = r_dSF.json()
        json_data_SFO = r_SFO.json()
        json_data_SJC = r_SJC.json()
        json_data_OAK = r_OAK.json()

        weather = {
            'DowntownSF': json_data_downtownSF['properties']['periods'],
            'SFO': json_data_SFO['properties']['periods'],
            'SJC': json_data_SJC['properties']['periods'],
            'OAK': json_data_OAK['properties']['periods']
        }

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
              <h1>Long Term Weather in San Francisco</h1>
              <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting San Francisco in <b>{}</b></p>
              <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting San Francisco in <b>{}</b></p>
              <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting San Francisco in <b>{}</b></p>
           </body>
        </html>
        """
        # format the html content with the corresponding {} arguments
        my_page = html_content.format(place, place,
                   forecast1, weather[place][0]['name'],weather[place][0]['detailedForecast'],
                   forecast2, weather[place][1]['name'],weather[place][1]['detailedForecast'],
                   forecast3, weather[place][2]['name'],weather[place][2]['detailedForecast'],
                   forecast4, weather[place][3]['name'], weather[place][3]['detailedForecast'],
                   forecast5, weather[place][4]['name'], weather[place][4]['detailedForecast'],
                   forecast6, weather[place][5]['name'], weather[place][5]['detailedForecast'],
                   top_files[0][0], top_files[0][1], top_files[0][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip(),
                   top_files[1][0], top_files[1][1], top_files[1][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip(),
                   top_files[2][0], top_files[2][1], top_files[2][0].replace('FarmersAlmanac','').replace('-','').replace('SF.txt','').strip()
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
def get_weather(place: str = None):
    """Fetches weather information based on place entered.

    Args:
        place: identifier for weather information of the location

    Returns:
        HTML content about the short term and long range forecast to display on a webpage,
        If no place parameter is queried, a general HTML page displays with links for the
        various place parameters
    """
    """------------------------------------------------------------------------------"""
    """This section is used for reading in the text files and ranking the text files """
    """------------------------------------------------------------------------------"""

    # Folder Path
    path = r"C:\Users\epana\PycharmProjects\tourismProject"

    # Change the directory
    os.chdir(path)

    transpo_words = []
    # get weather requirements
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
    """This section is for setting up the css and html information for transportation"""
    """------------------------------------------------------------------------------"""

    # Cascading style sheet
    my_css = """
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
       <head>
          <meta charset="UTF-8">
          <title>Transportation in San Francisco</title>
          <style></style>
          <p><img src="https://github.com/epanal/Python/blob/main/TourismProject/SFTransportationLogo.jpg?raw=true" alt="Icon"> </p>
       </head>
       <body>
          <p><a href="/">Go back to Main Page</a></p>
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
    my_page = html_content.format(transpo_words,
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
