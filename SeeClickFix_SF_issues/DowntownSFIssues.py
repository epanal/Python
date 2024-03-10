# Ethan Panal
# ANLT 224 Data Wrangling

import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
from jinja2 import Template
import plotly.express as px
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
app = FastAPI()

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="C:/Users/epana/PycharmProjects/March2Class/")

# url and get request
url = 'https://seeclickfix.com/api/v2/issues?place_url=downtown_san-francisco'
r = requests.get(url)
json_data = r.json()

# Get the issues and extract lat/long, addresses and name of the issue
coords, names, addresses = [], [], []
for i,j in enumerate(json_data['issues']):
    names.append(json_data['issues'][i]['summary'])
    coords.append([json_data['issues'][i]['lng'],json_data['issues'][i]['lat']])
    addresses.append(json_data['issues'][i]['address'])

# Put the information in a data frame
coords_df = pd.DataFrame(coords,columns = ['long','lat'])
coords_df['names'] = names
coords_df['address'] = addresses

# Create the plot
fig = px.scatter_mapbox(coords_df, title='Issues In Downtown San Francisco',
                        lat="lat", lon="long", hover_name = 'names', text = 'address',
                        zoom=14, height=500, width=500)
fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(marker_size=18)

# Get index.html to display on the main page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Render the template passing the Plotly figure HTML and the coordinates dataframe
    return templates.TemplateResponse("index.html",
        {"request": request, "plotly_figure": fig.to_html(), "coords_df": coords_df.to_html()})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)