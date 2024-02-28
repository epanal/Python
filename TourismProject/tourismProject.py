from fastapi import FastAPI, Body, Query
from typing import Literal
from fastapi.responses import HTMLResponse  # Import HTMLResponse

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
                    background-color: #f9f9f9;
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
        </head>
        <body>
            <h1>Welcome to ABC to the E page for San Francisco tourism !</h1>
            <p>Explore our content to discover San Francisco food spots and landmarks. Check the latest transportation, weather, and safety information!</p>
        </body>
        </html>
        """

    return HTMLResponse(content=html_content)

#print(json_data_downtownSF['properties']['periods'])

@app.get("/weather")
def get_weather(
        place: Literal["DowntownSF", "SFO", "SJC", "OAK"]
):
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

    # Folder Path
    path = r"C:\Users\epana\PycharmProjects\tourismProject"

    # Change the directory
    os.chdir(path)

    words = []
    # get weather requirements
    with open("WeatherReqs.txt", encoding='utf-8') as fd:
        for line in fd:
            words.append(line[:-1])

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

            # call read text file function
            word_count = text_file_counter(words, file_path)
            file_dict[file] = word_count

    def file_ranks(file_counts, n):
        # Sort the files based on word counts in descending order
        sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)

        # Take the top n items
        top_n = sorted_files[:n]
        return top_n

    top_files = file_ranks(file_dict, 3)

    # This section is for setting up the cascading style sheet
    my_css = """<style>
                /* Add some CSS styles for a fancy look */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
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
                h2 {
                    color: #007bff;
                    font-size: 36px;
                    margin-bottom: 20px;
                    text-align: left;
                }
                p {
                    color: #333;
                    font-size: 18px;
                }
            </style>"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Weather in {}</title>
        <style></style>
                 
    </head>
    <body>
        <h0>Ethan Panal's Endpoint for Tourism Startup</h0>
        <h1>Short Term Weather in {}</h1>
        <p><img src="{}" alt="Icon"> <b>{}</b> : {}</p>
        <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
        <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
        <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
        <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
        <p><img src="{}" alt="Icon"> <b>{}</b>: {}</p>
        
        <h2>Long Term Weather in San Francisco</h2>
        <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting <b>{}</b></p>
        <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting <b>{}</b></p>
        <p><b>{}</b> contains {} instances of words related to nice weather so we recommend visiting <b>{}</b></p>

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
               top_files[0][0], top_files[0][1], top_files[0][0].replace('FarmersAlmanac','').replace('SF.txt','').strip(),
               top_files[1][0], top_files[1][1], top_files[1][0].replace('FarmersAlmanac','').replace('SF.txt','').strip(),
               top_files[2][0], top_files[2][1], top_files[2][0].replace('FarmersAlmanac','').replace('SF.txt','').strip()
               )

    # Replace the style strings with the CSS
    my_final_page = my_page.replace('<style></style>', my_css)
    return HTMLResponse(content=my_final_page, media_type="text/html")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
