
## WeatherPy

In this example, you'll be creating a Python script to visualize the weather of 500+ cities across the world of varying distance from the equator. To accomplish this, you'll be utilizing a [simple Python library](https://pypi.python.org/pypi/citipy), the [OpenWeatherMap API](https://openweathermap.org/api), and a little common sense to create a representative model of weather across world cities.

Your objective is to build a series of scatter plots to showcase the following relationships:

* Temperature (F) vs. Latitude
* Humidity (%) vs. Latitude
* Cloudiness (%) vs. Latitude
* Wind Speed (mph) vs. Latitude

Your final notebook must:

* Randomly select **at least** 500 unique (non-repeat) cities based on latitude and longitude.
* Perform a weather check on each of the cities using a series of successive API calls. 
* Include a print log of each city as it's being processed with the city number, city name, and requested URL.
* Save both a CSV of all data retrieved and png images for each scatter plot.

As final considerations:

* You must use the Matplotlib and Seaborn libraries.
* You must include a written description of three observable trends based on the data. 
* You must use proper labeling of your plots, including aspects like: Plot Titles (with date of analysis) and Axes Labels.
* You must include an exported markdown version of your Notebook called  `README.md` in your GitHub repository.  
* See [Example Solution](WeatherPy_Example.pdf) for a reference on expected format. 

## Hints and Considerations

* You may want to start this assignment by refreshing yourself on 4th grade geography, in particular, the [geographic coordinate system](http://desktop.arcgis.com/en/arcmap/10.3/guide-books/map-projections/about-geographic-coordinate-systems.htm). 

* Next, spend the requisite time necessary to study the OpenWeatherMap API. Based on your initial study, you should be able to answer  basic questions about the API: Where do you request the API key? Which Weather API in particular will you need? What URL endpoints does it expect? What JSON structure does it respond with? Before you write a line of code, you should be aiming to have a crystal clear understanding of your intended outcome.

* Though we've never worked with the [citipy Python library](https://pypi.python.org/pypi/citipy), push yourself to decipher how it works, and why it might be relevant. Before you try to incorporate the library into your analysis, start by creating simple test cases outside your main script to confirm that you are using it correctly. Too often, when introduced to a new library, students get bogged down by the most minor of errors -- spending hours investigating their entire code -- when, in fact, a simple and focused test would have shown their basic utilization of the library was wrong from the start. Don't let this be you!

* Part of our expectation in this challenge is that you will use critical thinking skills to understand how and why we're recommending the tools we are. What is Citipy for? Why would you use it in conjunction with the OpenWeatherMap API? How would you do so?

* In building your script, pay attention to the cities you are using in your query pool. Are you getting coverage of the full gamut of latitudes and longitudes? Or are you simply choosing 500 cities concentrated in one region of the world? Even if you were a geographic genius, simply rattling 500 cities based on your human selection would create a biased dataset. Be thinking of how you should counter this. (Hint: Consider the full range of latitudes).

* Lastly, remember -- this is a challenging activity. Push yourself! If you complete this task, then you can safely say that you've gained a strong mastery of the core foundations of data analytics and it will only go better from here. Good luck!

### Three observable trends based on the data
- Cities nearest to the equator (latitude 0) tend to have the highest max temperature.  Cities further away (latitude <-45 or >+45) tend to have lower max temperatures.
- City wind speeds are lowest around the equator, and are higher at latitudes away from the equator.  This suggests that wind speed and max temperature are inversely correlated.
- In this sampling of data, there were no cities found below -60 degrees latitude south of the equator.


```python
import openweathermapy as ow
from citipy import citipy
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import random
import requests
import datetime as dt

from localenv import api_key
```


```python
# set up parameters dictionary and base url
params = {"appid": api_key,
          "units": "Imperial"}
url = "http://api.openweathermap.org/data/2.5/weather?"
# api_key = "25bc90a1196e6f153eece0bc0b0fc9eb", saved into localenv file
```


```python
# Generate list of 500 cities (generate smaller list while testing)
cities = []
count = 0
total = 500

while (count<total):
    lat = random.randint(-90,91)
    lon = random.randint(-180,181)
    city = citipy.nearest_city(lat,lon)
    city_name = city.city_name
    # if statement to avoid duplicate cities
    if city_name not in cities:
        cities.append(city_name)
    # set count to number of cities, exits loop once # of cities requirement met
    count = len(cities)
    
count
```




    500




```python
# set up dataframe to store city weather metrics
cities_df = pd.DataFrame({"City": cities})
cities_df['Max Temperature'] = ""
cities_df['Humidity'] = ""
cities_df['Cloudiness'] = ""
cities_df['Wind Speed'] = ""
cities_df['Latitude'] = ""
cities_df['Longitude'] = ""
cities_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Max Temperature</th>
      <th>Humidity</th>
      <th>Cloudiness</th>
      <th>Wind Speed</th>
      <th>Latitude</th>
      <th>Longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ruteng</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>mudgee</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>avarua</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>kaduqli</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>granada</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
# Loop through the cities_df and search for weather data of each city
print(f"Begin Data Retrieval")
print(f"-"*60)
# record date data retrieval occurred
date = dt.date.today()

for index, row in cities_df.iterrows():
    # update parameter to city
    params['q'] = f"{row['City']}"

    # make request, print url
    response = requests.get(url,params = params)
    print(f"Processing Record {index+1} of {count} | {row['City']} \
          \n{response.url}")
    # convert to json
    response_json = response.json()
    
    try:
        cities_df.at[index, "Max Temperature"]=response_json["main"]["temp_max"]
        cities_df.at[index, "Humidity"]= response_json["main"]["humidity"]
        cities_df.at[index, "Cloudiness"]= response_json["clouds"]["all"]
        cities_df.at[index, "Wind Speed"]= response_json["wind"]["speed"]
        cities_df.at[index, "Latitude"]= response_json["coord"]["lat"]
        cities_df.at[index, "Longitude"]= response_json["coord"]["lon"]
    except (KeyError, IndexError) as e:
        print(f"Error at {row['City']}, dropping city: {e}")
        cities_df.drop(index,axis=0,inplace=True)

print(f"-"*60)
print(f"End Data Retrieval")
print(f"-"*60)   
```

    Begin Data Retrieval
    ------------------------------------------------------------
    Processing Record 1 of 500 | ruteng           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ruteng
    Processing Record 2 of 500 | mudgee           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mudgee
    Processing Record 3 of 500 | avarua           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=avarua
    Processing Record 4 of 500 | kaduqli           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kaduqli
    Processing Record 5 of 500 | granada           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=granada
    Processing Record 6 of 500 | ankara           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ankara
    Processing Record 7 of 500 | nome           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nome
    Processing Record 8 of 500 | ulaangom           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ulaangom
    Processing Record 9 of 500 | albany           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=albany
    Processing Record 10 of 500 | atuona           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=atuona
    Processing Record 11 of 500 | ushuaia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ushuaia
    Processing Record 12 of 500 | kangaatsiaq           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kangaatsiaq
    Processing Record 13 of 500 | shaunavon           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=shaunavon
    Processing Record 14 of 500 | elk city           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=elk+city
    Processing Record 15 of 500 | pisco           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=pisco
    Processing Record 16 of 500 | taolanaro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=taolanaro
    Error at taolanaro, dropping city: 'main'
    Processing Record 17 of 500 | sopelana           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sopelana
    Processing Record 18 of 500 | lavrentiya           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lavrentiya
    Processing Record 19 of 500 | carbonia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=carbonia
    Processing Record 20 of 500 | dikson           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=dikson
    Processing Record 21 of 500 | punta arenas           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=punta+arenas
    Processing Record 22 of 500 | metro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=metro
    Processing Record 23 of 500 | dwarka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=dwarka
    Processing Record 24 of 500 | kapaa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kapaa
    Processing Record 25 of 500 | sao jose da coroa grande           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+jose+da+coroa+grande
    Processing Record 26 of 500 | mogadishu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mogadishu
    Processing Record 27 of 500 | moose factory           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=moose+factory
    Processing Record 28 of 500 | rikitea           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=rikitea
    Processing Record 29 of 500 | puerto ayora           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=puerto+ayora
    Processing Record 30 of 500 | mataura           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mataura
    Processing Record 31 of 500 | hobyo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hobyo
    Processing Record 32 of 500 | gizo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gizo
    Processing Record 33 of 500 | bluff           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bluff
    Processing Record 34 of 500 | pospelikha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=pospelikha
    Processing Record 35 of 500 | jamestown           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=jamestown
    Processing Record 36 of 500 | ligayan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ligayan
    Processing Record 37 of 500 | tuktoyaktuk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tuktoyaktuk
    Processing Record 38 of 500 | saldanha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saldanha
    Processing Record 39 of 500 | khartoum           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=khartoum
    Processing Record 40 of 500 | gushikawa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gushikawa
    Processing Record 41 of 500 | butaritari           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=butaritari
    Processing Record 42 of 500 | barrow           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=barrow
    Processing Record 43 of 500 | nokaneng           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nokaneng
    Processing Record 44 of 500 | lebu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lebu
    Processing Record 45 of 500 | dunedin           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=dunedin
    Processing Record 46 of 500 | mount gambier           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mount+gambier
    Processing Record 47 of 500 | qaanaaq           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=qaanaaq
    Processing Record 48 of 500 | hobart           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hobart
    Processing Record 49 of 500 | bubaque           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bubaque
    Processing Record 50 of 500 | nefteyugansk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nefteyugansk
    Processing Record 51 of 500 | saint-georges           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saint-georges
    Processing Record 52 of 500 | lompoc           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lompoc
    Processing Record 53 of 500 | saint-philippe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saint-philippe
    Processing Record 54 of 500 | vaini           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vaini
    Processing Record 55 of 500 | magistralnyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=magistralnyy
    Processing Record 56 of 500 | busselton           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=busselton
    Processing Record 57 of 500 | sisimiut           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sisimiut
    Processing Record 58 of 500 | cape town           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cape+town
    Processing Record 59 of 500 | upernavik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=upernavik
    Processing Record 60 of 500 | saskylakh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saskylakh
    Processing Record 61 of 500 | khatanga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=khatanga
    Processing Record 62 of 500 | kahului           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kahului
    Processing Record 63 of 500 | torrington           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=torrington
    Processing Record 64 of 500 | lasa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lasa
    Processing Record 65 of 500 | ribeira grande           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ribeira+grande
    Processing Record 66 of 500 | port alfred           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+alfred
    Processing Record 67 of 500 | karasburg           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=karasburg
    Processing Record 68 of 500 | kadoma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kadoma
    Processing Record 69 of 500 | abha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=abha
    Processing Record 70 of 500 | tyrma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tyrma
    Processing Record 71 of 500 | moramanga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=moramanga
    Processing Record 72 of 500 | arroio grande           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=arroio+grande
    Processing Record 73 of 500 | amapa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=amapa
    Processing Record 74 of 500 | korla           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=korla
    Error at korla, dropping city: 'main'
    Processing Record 75 of 500 | yaan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yaan
    Processing Record 76 of 500 | wajima           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=wajima
    Processing Record 77 of 500 | castro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=castro
    Processing Record 78 of 500 | bengkulu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bengkulu
    Error at bengkulu, dropping city: 'main'
    Processing Record 79 of 500 | chokurdakh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chokurdakh
    Processing Record 80 of 500 | tasiilaq           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tasiilaq
    Processing Record 81 of 500 | mantua           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mantua
    Processing Record 82 of 500 | bredasdorp           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bredasdorp
    Processing Record 83 of 500 | airai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=airai
    Processing Record 84 of 500 | damietta           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=damietta
    Processing Record 85 of 500 | primo tapia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=primo+tapia
    Processing Record 86 of 500 | monrovia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=monrovia
    Processing Record 87 of 500 | mananjary           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mananjary
    Processing Record 88 of 500 | hithadhoo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hithadhoo
    Processing Record 89 of 500 | tidore           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tidore
    Error at tidore, dropping city: 'main'
    Processing Record 90 of 500 | fernley           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=fernley
    Processing Record 91 of 500 | xingyi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=xingyi
    Processing Record 92 of 500 | hermanus           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hermanus
    Processing Record 93 of 500 | muroto           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=muroto
    Processing Record 94 of 500 | sambava           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sambava
    Processing Record 95 of 500 | morwa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=morwa
    Processing Record 96 of 500 | raga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=raga
    Error at raga, dropping city: 'main'
    Processing Record 97 of 500 | talnakh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=talnakh
    Processing Record 98 of 500 | port elizabeth           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+elizabeth
    Processing Record 99 of 500 | jumla           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=jumla
    Processing Record 100 of 500 | hofn           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hofn
    Processing Record 101 of 500 | hilo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hilo
    Processing Record 102 of 500 | belushya guba           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=belushya+guba
    Error at belushya guba, dropping city: 'main'
    Processing Record 103 of 500 | maridi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=maridi
    Error at maridi, dropping city: 'main'
    Processing Record 104 of 500 | novikovo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=novikovo
    Processing Record 105 of 500 | yellowknife           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yellowknife
    Processing Record 106 of 500 | almaznyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=almaznyy
    Processing Record 107 of 500 | krasnoarmeysk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=krasnoarmeysk
    Processing Record 108 of 500 | illoqqortoormiut           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=illoqqortoormiut
    Error at illoqqortoormiut, dropping city: 'main'
    Processing Record 109 of 500 | belmonte           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=belmonte
    Processing Record 110 of 500 | srednekolymsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=srednekolymsk
    Processing Record 111 of 500 | parkes           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=parkes
    Processing Record 112 of 500 | louisbourg           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=louisbourg
    Error at louisbourg, dropping city: 'main'
    Processing Record 113 of 500 | longyearbyen           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=longyearbyen
    Processing Record 114 of 500 | georgetown           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=georgetown
    Processing Record 115 of 500 | havre-saint-pierre           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=havre-saint-pierre
    Processing Record 116 of 500 | keetmanshoop           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=keetmanshoop
    Processing Record 117 of 500 | tocache           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tocache
    Processing Record 118 of 500 | sept-iles           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sept-iles
    Processing Record 119 of 500 | alihe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=alihe
    Processing Record 120 of 500 | kruisfontein           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kruisfontein
    Processing Record 121 of 500 | vao           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vao
    Processing Record 122 of 500 | najran           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=najran
    Processing Record 123 of 500 | te anau           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=te+anau
    Processing Record 124 of 500 | saint-pierre           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saint-pierre
    Processing Record 125 of 500 | bud           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bud
    Processing Record 126 of 500 | mar del plata           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mar+del+plata
    Processing Record 127 of 500 | nishihara           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nishihara
    Processing Record 128 of 500 | vaitupu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vaitupu
    Error at vaitupu, dropping city: 'main'
    Processing Record 129 of 500 | barentsburg           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=barentsburg
    Error at barentsburg, dropping city: 'main'
    Processing Record 130 of 500 | amderma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=amderma
    Error at amderma, dropping city: 'main'
    Processing Record 131 of 500 | thompson           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=thompson
    Processing Record 132 of 500 | arraial do cabo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=arraial+do+cabo
    Processing Record 133 of 500 | amahai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=amahai
    Processing Record 134 of 500 | maloshuyka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=maloshuyka
    Error at maloshuyka, dropping city: 'main'
    Processing Record 135 of 500 | sabang           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sabang
    Processing Record 136 of 500 | takoradi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=takoradi
    Processing Record 137 of 500 | enshi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=enshi
    Processing Record 138 of 500 | new norfolk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=new+norfolk
    Processing Record 139 of 500 | sitka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sitka
    Processing Record 140 of 500 | paamiut           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=paamiut
    Processing Record 141 of 500 | troianul           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=troianul
    Processing Record 142 of 500 | namatanai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=namatanai
    Processing Record 143 of 500 | petropavlovsk-kamchatskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=petropavlovsk-kamchatskiy
    Processing Record 144 of 500 | mineiros           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mineiros
    Processing Record 145 of 500 | galesong           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=galesong
    Processing Record 146 of 500 | bukachacha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bukachacha
    Processing Record 147 of 500 | winnemucca           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=winnemucca
    Processing Record 148 of 500 | mahebourg           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mahebourg
    Processing Record 149 of 500 | marawi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=marawi
    Processing Record 150 of 500 | bethel           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bethel
    Processing Record 151 of 500 | agva           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=agva
    Error at agva, dropping city: 'main'
    Processing Record 152 of 500 | galveston           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=galveston
    Processing Record 153 of 500 | port keats           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+keats
    Processing Record 154 of 500 | bindura           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bindura
    Processing Record 155 of 500 | russkaya polyana           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=russkaya+polyana
    Processing Record 156 of 500 | chuy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chuy
    Processing Record 157 of 500 | tsihombe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tsihombe
    Error at tsihombe, dropping city: 'main'
    Processing Record 158 of 500 | yar-sale           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yar-sale
    Processing Record 159 of 500 | kodiak           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kodiak
    Processing Record 160 of 500 | comodoro rivadavia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=comodoro+rivadavia
    Processing Record 161 of 500 | geraldton           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=geraldton
    Processing Record 162 of 500 | port-cartier           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port-cartier
    Processing Record 163 of 500 | mackay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mackay
    Processing Record 164 of 500 | mnogovershinnyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mnogovershinnyy
    Processing Record 165 of 500 | wanlaweyn           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=wanlaweyn
    Processing Record 166 of 500 | attawapiskat           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=attawapiskat
    Error at attawapiskat, dropping city: 'main'
    Processing Record 167 of 500 | angoche           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=angoche
    Processing Record 168 of 500 | samusu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=samusu
    Error at samusu, dropping city: 'main'
    Processing Record 169 of 500 | sentyabrskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sentyabrskiy
    Error at sentyabrskiy, dropping city: 'main'
    Processing Record 170 of 500 | vrangel           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vrangel
    Processing Record 171 of 500 | bathsheba           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bathsheba
    Processing Record 172 of 500 | okhotsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=okhotsk
    Processing Record 173 of 500 | beinamar           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=beinamar
    Processing Record 174 of 500 | mys shmidta           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mys+shmidta
    Error at mys shmidta, dropping city: 'main'
    Processing Record 175 of 500 | brae           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=brae
    Processing Record 176 of 500 | aklavik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=aklavik
    Processing Record 177 of 500 | ketchikan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ketchikan
    Processing Record 178 of 500 | clifton           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=clifton
    Processing Record 179 of 500 | solnechnyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=solnechnyy
    Processing Record 180 of 500 | erenhot           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=erenhot
    Processing Record 181 of 500 | morros           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=morros
    Processing Record 182 of 500 | sorland           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sorland
    Processing Record 183 of 500 | cananeia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cananeia
    Processing Record 184 of 500 | tysmenytsya           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tysmenytsya
    Processing Record 185 of 500 | tuatapere           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tuatapere
    Processing Record 186 of 500 | lianzhou           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lianzhou
    Processing Record 187 of 500 | hami           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hami
    Processing Record 188 of 500 | tumannyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tumannyy
    Error at tumannyy, dropping city: 'main'
    Processing Record 189 of 500 | ambanja           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ambanja
    Processing Record 190 of 500 | hendijan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hendijan
    Error at hendijan, dropping city: 'main'
    Processing Record 191 of 500 | fairbanks           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=fairbanks
    Processing Record 192 of 500 | ponta delgada           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ponta+delgada
    Processing Record 193 of 500 | finschhafen           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=finschhafen
    Processing Record 194 of 500 | east london           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=east+london
    Processing Record 195 of 500 | tailai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tailai
    Processing Record 196 of 500 | ijaki           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ijaki
    Error at ijaki, dropping city: 'main'
    Processing Record 197 of 500 | taltal           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=taltal
    Processing Record 198 of 500 | savinskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=savinskiy
    Processing Record 199 of 500 | aswan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=aswan
    Processing Record 200 of 500 | arkhangelos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=arkhangelos
    Error at arkhangelos, dropping city: 'main'
    Processing Record 201 of 500 | cururupu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cururupu
    Processing Record 202 of 500 | clyde river           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=clyde+river
    Processing Record 203 of 500 | pangai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=pangai
    Processing Record 204 of 500 | lima           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lima
    Processing Record 205 of 500 | tolaga bay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tolaga+bay
    Processing Record 206 of 500 | katsuura           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=katsuura
    Processing Record 207 of 500 | ponta do sol           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ponta+do+sol
    Processing Record 208 of 500 | verkhoyansk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=verkhoyansk
    Processing Record 209 of 500 | asau           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=asau
    Error at asau, dropping city: 'main'
    Processing Record 210 of 500 | ulety           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ulety
    Processing Record 211 of 500 | torbay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=torbay
    Processing Record 212 of 500 | harnosand           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=harnosand
    Processing Record 213 of 500 | imbituba           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=imbituba
    Processing Record 214 of 500 | inuvik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=inuvik
    Processing Record 215 of 500 | shakiso           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=shakiso
    Processing Record 216 of 500 | leningradskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=leningradskiy
    Processing Record 217 of 500 | tual           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tual
    Processing Record 218 of 500 | gat           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gat
    Processing Record 219 of 500 | mana           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mana
    Processing Record 220 of 500 | salym           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=salym
    Processing Record 221 of 500 | guerrero negro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=guerrero+negro
    Processing Record 222 of 500 | victor harbor           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=victor+harbor
    Processing Record 223 of 500 | copaceni           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=copaceni
    Processing Record 224 of 500 | marsa matruh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=marsa+matruh
    Processing Record 225 of 500 | ayan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ayan
    Processing Record 226 of 500 | raudeberg           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=raudeberg
    Processing Record 227 of 500 | cabedelo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cabedelo
    Processing Record 228 of 500 | puerto madero           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=puerto+madero
    Processing Record 229 of 500 | high level           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=high+level
    Processing Record 230 of 500 | antalaha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=antalaha
    Processing Record 231 of 500 | tiksi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tiksi
    Processing Record 232 of 500 | gamba           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gamba
    Processing Record 233 of 500 | cravo norte           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cravo+norte
    Processing Record 234 of 500 | la palma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=la+palma
    Processing Record 235 of 500 | lorengau           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lorengau
    Processing Record 236 of 500 | araouane           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=araouane
    Processing Record 237 of 500 | riyadh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=riyadh
    Processing Record 238 of 500 | nizhniy tagil           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nizhniy+tagil
    Processing Record 239 of 500 | cap malheureux           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cap+malheureux
    Processing Record 240 of 500 | cayenne           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cayenne
    Processing Record 241 of 500 | kyren           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kyren
    Processing Record 242 of 500 | port blair           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+blair
    Processing Record 243 of 500 | provideniya           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=provideniya
    Processing Record 244 of 500 | new haven           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=new+haven
    Processing Record 245 of 500 | taunggyi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=taunggyi
    Processing Record 246 of 500 | cidreira           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cidreira
    Processing Record 247 of 500 | ha giang           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ha+giang
    Processing Record 248 of 500 | saint anthony           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saint+anthony
    Processing Record 249 of 500 | diamantino           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=diamantino
    Processing Record 250 of 500 | port augusta           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+augusta
    Processing Record 251 of 500 | medina           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=medina
    Processing Record 252 of 500 | russell           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=russell
    Processing Record 253 of 500 | maniitsoq           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=maniitsoq
    Processing Record 254 of 500 | kapuskasing           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kapuskasing
    Processing Record 255 of 500 | luderitz           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=luderitz
    Processing Record 256 of 500 | bjornevatn           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bjornevatn
    Processing Record 257 of 500 | iqaluit           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=iqaluit
    Processing Record 258 of 500 | presidencia roque saenz pena           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=presidencia+roque+saenz+pena
    Processing Record 259 of 500 | rawson           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=rawson
    Processing Record 260 of 500 | severobaykalsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=severobaykalsk
    Processing Record 261 of 500 | motygino           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=motygino
    Processing Record 262 of 500 | mehamn           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mehamn
    Processing Record 263 of 500 | katangli           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=katangli
    Processing Record 264 of 500 | avera           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=avera
    Processing Record 265 of 500 | san-pedro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san-pedro
    Processing Record 266 of 500 | khor           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=khor
    Processing Record 267 of 500 | udachnyy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=udachnyy
    Processing Record 268 of 500 | labuhan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=labuhan
    Processing Record 269 of 500 | haverfordwest           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=haverfordwest
    Processing Record 270 of 500 | balakovo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=balakovo
    Processing Record 271 of 500 | touros           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=touros
    Processing Record 272 of 500 | nikolskoye           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nikolskoye
    Processing Record 273 of 500 | pyshma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=pyshma
    Processing Record 274 of 500 | auki           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=auki
    Processing Record 275 of 500 | xining           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=xining
    Processing Record 276 of 500 | port macquarie           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+macquarie
    Processing Record 277 of 500 | tiruchchendur           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tiruchchendur
    Processing Record 278 of 500 | yook           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yook
    Processing Record 279 of 500 | gerardmer           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gerardmer
    Processing Record 280 of 500 | codrington           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=codrington
    Processing Record 281 of 500 | zhigansk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=zhigansk
    Processing Record 282 of 500 | sterling           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sterling
    Processing Record 283 of 500 | dakar           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=dakar
    Processing Record 284 of 500 | margate           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=margate
    Processing Record 285 of 500 | taoudenni           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=taoudenni
    Processing Record 286 of 500 | salinopolis           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=salinopolis
    Processing Record 287 of 500 | saltpond           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saltpond
    Processing Record 288 of 500 | anloga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=anloga
    Processing Record 289 of 500 | lilongwe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lilongwe
    Processing Record 290 of 500 | cacu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cacu
    Processing Record 291 of 500 | shouguang           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=shouguang
    Processing Record 292 of 500 | san cristobal           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+cristobal
    Processing Record 293 of 500 | carnarvon           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=carnarvon
    Processing Record 294 of 500 | vila velha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vila+velha
    Processing Record 295 of 500 | nizhneyansk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nizhneyansk
    Error at nizhneyansk, dropping city: 'main'
    Processing Record 296 of 500 | kavieng           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kavieng
    Processing Record 297 of 500 | hamilton           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hamilton
    Processing Record 298 of 500 | vanimo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vanimo
    Processing Record 299 of 500 | regina           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=regina
    Processing Record 300 of 500 | fortuna           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=fortuna
    Processing Record 301 of 500 | rio grande           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=rio+grande
    Processing Record 302 of 500 | kiruna           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kiruna
    Processing Record 303 of 500 | broome           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=broome
    Processing Record 304 of 500 | beringovskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=beringovskiy
    Processing Record 305 of 500 | sao filipe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+filipe
    Processing Record 306 of 500 | todos santos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=todos+santos
    Processing Record 307 of 500 | vila franca do campo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vila+franca+do+campo
    Processing Record 308 of 500 | flin flon           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=flin+flon
    Processing Record 309 of 500 | yakeshi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yakeshi
    Processing Record 310 of 500 | beyneu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=beyneu
    Processing Record 311 of 500 | santa cruz del sur           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=santa+cruz+del+sur
    Processing Record 312 of 500 | veraval           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=veraval
    Processing Record 313 of 500 | ambon           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ambon
    Processing Record 314 of 500 | kolpashevo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kolpashevo
    Processing Record 315 of 500 | constitucion           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=constitucion
    Processing Record 316 of 500 | viransehir           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=viransehir
    Processing Record 317 of 500 | jinchang           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=jinchang
    Processing Record 318 of 500 | san rafael           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+rafael
    Processing Record 319 of 500 | san patricio           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+patricio
    Processing Record 320 of 500 | lagos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=lagos
    Processing Record 321 of 500 | severo-kurilsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=severo-kurilsk
    Processing Record 322 of 500 | artyk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=artyk
    Error at artyk, dropping city: 'main'
    Processing Record 323 of 500 | placido de castro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=placido+de+castro
    Processing Record 324 of 500 | halalo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=halalo
    Error at halalo, dropping city: 'main'
    Processing Record 325 of 500 | kodinsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kodinsk
    Processing Record 326 of 500 | yerbogachen           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yerbogachen
    Processing Record 327 of 500 | antsohihy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=antsohihy
    Processing Record 328 of 500 | salalah           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=salalah
    Processing Record 329 of 500 | saint george           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=saint+george
    Processing Record 330 of 500 | gorontalo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gorontalo
    Processing Record 331 of 500 | bolobo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bolobo
    Processing Record 332 of 500 | warqla           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=warqla
    Error at warqla, dropping city: 'main'
    Processing Record 333 of 500 | ojinaga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ojinaga
    Processing Record 334 of 500 | strezhevoy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=strezhevoy
    Processing Record 335 of 500 | fevralsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=fevralsk
    Error at fevralsk, dropping city: 'main'
    Processing Record 336 of 500 | henties bay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=henties+bay
    Processing Record 337 of 500 | banjar           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=banjar
    Processing Record 338 of 500 | poum           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=poum
    Processing Record 339 of 500 | cazaje           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cazaje
    Error at cazaje, dropping city: 'main'
    Processing Record 340 of 500 | faya           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=faya
    Processing Record 341 of 500 | tabas           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tabas
    Processing Record 342 of 500 | ariquemes           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ariquemes
    Processing Record 343 of 500 | ondorhaan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ondorhaan
    Error at ondorhaan, dropping city: 'main'
    Processing Record 344 of 500 | nanortalik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nanortalik
    Processing Record 345 of 500 | samarai           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=samarai
    Processing Record 346 of 500 | santiago del estero           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=santiago+del+estero
    Processing Record 347 of 500 | palabuhanratu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=palabuhanratu
    Error at palabuhanratu, dropping city: 'main'
    Processing Record 348 of 500 | mandurah           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mandurah
    Processing Record 349 of 500 | sao mateus           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+mateus
    Processing Record 350 of 500 | sioux lookout           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sioux+lookout
    Processing Record 351 of 500 | samus           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=samus
    Processing Record 352 of 500 | komsomolskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=komsomolskiy
    Processing Record 353 of 500 | ardabil           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ardabil
    Processing Record 354 of 500 | izhma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=izhma
    Processing Record 355 of 500 | grand river south east           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=grand+river+south+east
    Error at grand river south east, dropping city: 'main'
    Processing Record 356 of 500 | damaturu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=damaturu
    Processing Record 357 of 500 | the valley           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=the+valley
    Processing Record 358 of 500 | kaitangata           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kaitangata
    Processing Record 359 of 500 | kadykchan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kadykchan
    Error at kadykchan, dropping city: 'main'
    Processing Record 360 of 500 | manicore           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=manicore
    Processing Record 361 of 500 | mokhsogollokh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mokhsogollokh
    Processing Record 362 of 500 | skjervoy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=skjervoy
    Processing Record 363 of 500 | kavaratti           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kavaratti
    Processing Record 364 of 500 | cabo san lucas           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cabo+san+lucas
    Processing Record 365 of 500 | chumikan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chumikan
    Processing Record 366 of 500 | santarem           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=santarem
    Error at santarem, dropping city: 'main'
    Processing Record 367 of 500 | chagda           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chagda
    Error at chagda, dropping city: 'main'
    Processing Record 368 of 500 | portland           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=portland
    Processing Record 369 of 500 | gorno-altaysk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=gorno-altaysk
    Processing Record 370 of 500 | ust-nera           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ust-nera
    Processing Record 371 of 500 | solenzo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=solenzo
    Processing Record 372 of 500 | basco           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=basco
    Processing Record 373 of 500 | aksu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=aksu
    Processing Record 374 of 500 | ondjiva           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ondjiva
    Processing Record 375 of 500 | rio gallegos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=rio+gallegos
    Processing Record 376 of 500 | makakilo city           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=makakilo+city
    Processing Record 377 of 500 | umzimvubu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=umzimvubu
    Error at umzimvubu, dropping city: 'main'
    Processing Record 378 of 500 | neiafu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=neiafu
    Processing Record 379 of 500 | brownsville           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=brownsville
    Processing Record 380 of 500 | totness           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=totness
    Processing Record 381 of 500 | warrnambool           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=warrnambool
    Processing Record 382 of 500 | karpathos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=karpathos
    Processing Record 383 of 500 | zhangye           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=zhangye
    Processing Record 384 of 500 | yondo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yondo
    Processing Record 385 of 500 | cherskiy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cherskiy
    Processing Record 386 of 500 | sur           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sur
    Processing Record 387 of 500 | sakakah           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sakakah
    Error at sakakah, dropping city: 'main'
    Processing Record 388 of 500 | alice springs           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=alice+springs
    Processing Record 389 of 500 | victoria           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=victoria
    Processing Record 390 of 500 | vardo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=vardo
    Processing Record 391 of 500 | chililabombwe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chililabombwe
    Processing Record 392 of 500 | road town           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=road+town
    Processing Record 393 of 500 | bolungarvik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bolungarvik
    Error at bolungarvik, dropping city: 'main'
    Processing Record 394 of 500 | faanui           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=faanui
    Processing Record 395 of 500 | tarnow           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tarnow
    Processing Record 396 of 500 | namibe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=namibe
    Processing Record 397 of 500 | kindia           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kindia
    Processing Record 398 of 500 | berezayka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=berezayka
    Processing Record 399 of 500 | sao francisco           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+francisco
    Processing Record 400 of 500 | prince rupert           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=prince+rupert
    Processing Record 401 of 500 | narsaq           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=narsaq
    Processing Record 402 of 500 | kuryk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kuryk
    Processing Record 403 of 500 | ask           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ask
    Processing Record 404 of 500 | play cu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=play+cu
    Error at play cu, dropping city: 'main'
    Processing Record 405 of 500 | knysna           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=knysna
    Processing Record 406 of 500 | beatrice           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=beatrice
    Processing Record 407 of 500 | sao gabriel da cachoeira           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+gabriel+da+cachoeira
    Processing Record 408 of 500 | santa maria del oro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=santa+maria+del+oro
    Processing Record 409 of 500 | awallan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=awallan
    Processing Record 410 of 500 | hornepayne           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hornepayne
    Processing Record 411 of 500 | chippewa falls           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=chippewa+falls
    Processing Record 412 of 500 | ilinskoye-khovanskoye           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ilinskoye-khovanskoye
    Processing Record 413 of 500 | sao joao da barra           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sao+joao+da+barra
    Processing Record 414 of 500 | laguna           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=laguna
    Processing Record 415 of 500 | santa maria           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=santa+maria
    Processing Record 416 of 500 | olmos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=olmos
    Processing Record 417 of 500 | mahadday weyne           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mahadday+weyne
    Error at mahadday weyne, dropping city: 'main'
    Processing Record 418 of 500 | hualmay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hualmay
    Processing Record 419 of 500 | bambous virieux           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bambous+virieux
    Processing Record 420 of 500 | necochea           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=necochea
    Processing Record 421 of 500 | povenets           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=povenets
    Processing Record 422 of 500 | dokka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=dokka
    Processing Record 423 of 500 | hambantota           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hambantota
    Processing Record 424 of 500 | rosetta           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=rosetta
    Processing Record 425 of 500 | sapa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=sapa
    Processing Record 426 of 500 | nhulunbuy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nhulunbuy
    Processing Record 427 of 500 | nago           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nago
    Processing Record 428 of 500 | baykit           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=baykit
    Processing Record 429 of 500 | port lincoln           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=port+lincoln
    Processing Record 430 of 500 | barabinsk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=barabinsk
    Processing Record 431 of 500 | college           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=college
    Processing Record 432 of 500 | husavik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=husavik
    Processing Record 433 of 500 | la ronge           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=la+ronge
    Processing Record 434 of 500 | hasaki           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=hasaki
    Processing Record 435 of 500 | esperance           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=esperance
    Processing Record 436 of 500 | paros           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=paros
    Processing Record 437 of 500 | tautira           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tautira
    Processing Record 438 of 500 | arman           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=arman
    Processing Record 439 of 500 | marsh harbour           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=marsh+harbour
    Processing Record 440 of 500 | cockburn town           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=cockburn+town
    Processing Record 441 of 500 | tabou           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=tabou
    Processing Record 442 of 500 | adrar           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=adrar
    Processing Record 443 of 500 | mutoko           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mutoko
    Processing Record 444 of 500 | leh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=leh
    Processing Record 445 of 500 | ordu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ordu
    Processing Record 446 of 500 | kamogawa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kamogawa
    Processing Record 447 of 500 | bambanglipuro           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=bambanglipuro
    Processing Record 448 of 500 | pimentel           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=pimentel
    Processing Record 449 of 500 | san joaquin           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+joaquin
    Processing Record 450 of 500 | la paz           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=la+paz
    Processing Record 451 of 500 | kazanka           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kazanka
    Processing Record 452 of 500 | berlevag           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=berlevag
    Processing Record 453 of 500 | meulaboh           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=meulaboh
    Processing Record 454 of 500 | nalut           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nalut
    Processing Record 455 of 500 | jaramana           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=jaramana
    Error at jaramana, dropping city: 'main'
    Processing Record 456 of 500 | wodonga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=wodonga
    Processing Record 457 of 500 | inyonga           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=inyonga
    Processing Record 458 of 500 | yulara           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yulara
    Processing Record 459 of 500 | palmer           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=palmer
    Processing Record 460 of 500 | san carlos           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+carlos
    Processing Record 461 of 500 | garden acres           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=garden+acres
    Processing Record 462 of 500 | roma           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=roma
    Processing Record 463 of 500 | myitkyina           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=myitkyina
    Processing Record 464 of 500 | kuusamo           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kuusamo
    Processing Record 465 of 500 | manikpur           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=manikpur
    Processing Record 466 of 500 | panama city           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=panama+city
    Processing Record 467 of 500 | yeniseysk           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yeniseysk
    Processing Record 468 of 500 | yangjiang           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=yangjiang
    Processing Record 469 of 500 | huarmey           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=huarmey
    Processing Record 470 of 500 | canico           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=canico
    Processing Record 471 of 500 | fougamou           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=fougamou
    Processing Record 472 of 500 | garden city           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=garden+city
    Processing Record 473 of 500 | djambala           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=djambala
    Processing Record 474 of 500 | makarov           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=makarov
    Processing Record 475 of 500 | linkuva           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=linkuva
    Processing Record 476 of 500 | puerto escondido           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=puerto+escondido
    Processing Record 477 of 500 | grindavik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=grindavik
    Processing Record 478 of 500 | kawalu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kawalu
    Processing Record 479 of 500 | qitaihe           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=qitaihe
    Processing Record 480 of 500 | macheng           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=macheng
    Processing Record 481 of 500 | san matias           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=san+matias
    Processing Record 482 of 500 | odessa           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=odessa
    Processing Record 483 of 500 | am timan           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=am+timan
    Processing Record 484 of 500 | malinovoye ozero           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=malinovoye+ozero
    Processing Record 485 of 500 | linguere           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=linguere
    Error at linguere, dropping city: 'main'
    Processing Record 486 of 500 | jaguarao           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=jaguarao
    Processing Record 487 of 500 | firminy           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=firminy
    Processing Record 488 of 500 | ibra           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ibra
    Processing Record 489 of 500 | puqi           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=puqi
    Processing Record 490 of 500 | buribay           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=buribay
    Processing Record 491 of 500 | ocean city           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=ocean+city
    Processing Record 492 of 500 | mezen           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=mezen
    Processing Record 493 of 500 | havelock           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=havelock
    Processing Record 494 of 500 | leshukonskoye           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=leshukonskoye
    Processing Record 495 of 500 | urusha           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=urusha
    Processing Record 496 of 500 | nong chik           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=nong+chik
    Processing Record 497 of 500 | portmore           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=portmore
    Processing Record 498 of 500 | taybad           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=taybad
    Processing Record 499 of 500 | inhambane           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=inhambane
    Processing Record 500 of 500 | kathmandu           
    http://api.openweathermap.org/data/2.5/weather?appid=25bc90a1196e6f153eece0bc0b0fc9eb&units=Imperial&q=kathmandu
    ------------------------------------------------------------
    End Data Retrieval
    ------------------------------------------------------------
    


```python
# save data to CSV file
cities_df.to_csv("weatherpy_data.csv", encoding="utf-8",index=False)
cities_df.count()
```




    City               457
    Max Temperature    457
    Humidity           457
    Cloudiness         457
    Wind Speed         457
    Latitude           457
    Longitude          457
    dtype: int64




```python
#Temperature (F) vs. Latitude
#Humidity (%) vs. Latitude
#Cloudiness (%) vs. Latitude
#Wind Speed (mph) vs. Latitude

# set up short variables for plotting
lat = cities_df['Latitude']
lon = cities_df['Longitude']
maxtemp = cities_df['Max Temperature']
humid = cities_df['Humidity']
cloud = cities_df['Cloudiness']
windsp = cities_df['Wind Speed']

# set up plot properties
sns.set()
plt.figure(figsize=(10,6))
plt.title(f"City Max Temperature (F) vs. Latitude ({date})", fontsize=20)
plt.xlabel("Latitude", fontsize=14)
plt.xlim(-90,90)
plt.ylabel("Max Temperature (F)", fontsize=14)

# plot data and save
plt.scatter(x=lat,y=maxtemp,
            c='red', edgecolor='black', alpha=0.5, marker='o', linewidths=1)
plt.savefig("Temperature (F) vs. Latitude.png")
plt.show()
```


![png](output_8_0.png)



```python
# set up plot properties
sns.set()
plt.figure(figsize=(10,6))
plt.title(f"City Humidity (%) vs. Latitude ({date})", fontsize=20)
plt.xlabel("Latitude", fontsize=14)
plt.xlim(-90,90)
plt.ylabel("Humidity (%)", fontsize=14)

# plot data and save
plt.scatter(x=lat,y=humid,
            c='gold', edgecolor='black', alpha=0.5, marker='o', linewidths=1)
plt.savefig("Humidity (%) vs. Latitude.png")
plt.show()
```


![png](output_9_0.png)



```python
# set up plot properties
sns.set()
plt.figure(figsize=(10,6))
plt.title(f"City Cloudiness (%) vs. Latitude ({date})", fontsize=20)
plt.xlabel("Latitude", fontsize=14)
plt.xlim(-90,90)
plt.ylabel("Cloudiness (%)", fontsize=14)

# plot data and save
plt.scatter(x=lat,y=cloud,
            c='coral', edgecolor='black', alpha=0.5, marker='o', linewidths=1)
plt.savefig("Cloudiness (%) vs. Latitude.png")
plt.show()
```


![png](output_10_0.png)



```python
# set up plot properties
sns.set()
plt.figure(figsize=(10,6))
plt.title(f"City Wind Speed (mph) vs. Latitude ({date})", fontsize=20)
plt.xlabel("Latitude", fontsize=14)
plt.xlim(-90,90)
plt.ylabel("Wind Speed (mph)", fontsize=14)

# plot data and save
plt.scatter(x=lat,y=windsp,
            c='blue', edgecolor='black', alpha=0.5, marker='o', linewidths=1)
plt.savefig("Cloudiness (%) vs. Latitude.png")
plt.show()
```


![png](output_11_0.png)

