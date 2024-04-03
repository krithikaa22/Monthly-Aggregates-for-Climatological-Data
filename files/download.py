import os
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from zipfile import ZipFile
import yaml

## get path of current directory
SCRIPTDIR = os.path.dirname(__file__)

## set path of the config file
YAMLFILE = os.path.join(SCRIPTDIR, 'config.yaml')

## extract data from the config yaml file
with open(YAMLFILE, 'r') as file:
    params = yaml.safe_load(file)

year = params['year']
url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/'

## send api call to the url
response = requests.get(url)

## parse the html content
soup = BeautifulSoup(response.content, 'html.parser')
rows = soup.find("table").find_all("tr")[2:-2]

fileName = []

total = params.get('n_locs')

## extract data and file name
for i in range(total):
    index = random.randint(0, len(rows))
    data = rows[index].find_all("td")
    fileName.append(data[0].text)

## write the data to the file
for name in fileName:
 newUrl = url+name
 response = requests.get(newUrl)
 open(name,'wb').write(response.content)

## zip the files
with ZipFile(os.path.join(SCRIPTDIR, '/zippedWeather.zip'),'w') as zip:
 for file in fileName:
  zip.write(file)

