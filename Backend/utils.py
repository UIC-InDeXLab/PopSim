import os
import requests
import pandas as pd
import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon

def getFIPS(lat, long, year = 2020, division = "block"):
    if division not in {"block", "county", "state"}:
        raise Exception("The administration division level is not correct")
    try:
        url = "https://geo.fcc.gov/api/census/block/find?latitude=" + \
            str(lat)+"&longitude="+str(long) + "&censusYear=" + \
            str(year)+"&showall=false&format=json"
        response = requests.get(url)
        print(response.text)
        return response.json()[division]["FIPS"]

    except requests.ConnectionError as error:
        print("Cannot connect to the GEO API")
        print(error)

def getDecennialData(fips, for_unit = 'block', dataField = "group(P1)", year = "2020"):
    if (for_unit not in {'state', 'county', 'tract', 'block'}):
        assert("for_unit must be 'state', 'county', 'tract', or 'block' ")
    if len(fips) < 2 :
        assert("FIPS must have length greater than 2")
    
    list_string = ['state:'+ fips[0:2],
                   'county:'+ (fips[2:5] if len(fips) >= 5 else '*'), 
                   'tract:' + (fips[5:11] if len(fips) >= 11 else '*'), 
                   'block:' + (fips[11:15] if len(fips) == 15 else '*')]
    
    while list_string[-1].find(for_unit) == -1 :
        list_string.pop()
    for_unit_string = list_string.pop()
    
    url = "https://api.census.gov/data/"+ year +"/dec/pl?get="+ dataField + \
          "&for="+ for_unit_string + ("&in=" if len(list_string) > 0 else "") + \
          "%20".join(list_string)
    filename = "_".join([for_unit_string, year]+list_string).replace(":", "-")+".csv"
    
    if os.path.exists(filename):
        df = pd.read_csv(filename)
        if (df.shape[0] == 1):
            return df.iloc[0]
        return df
    
    try:
        response = requests.get(url)
        JSONObject = response.json()
        
        if len(JSONObject)  == 2:
            series = pd.Series(JSONObject[1], index=JSONObject[0]).dropna()
            pd.DataFrame(series.to_dict(), index=[0]).to_csv(filename)
            return series
        else:
            dataframe = pd.DataFrame(data= JSONObject[1:], columns=JSONObject[0])
            dataframe.sort_values(by=["GEO_ID"], inplace=True, ignore_index=True)
            dataframe.to_csv(filename)
            return dataframe
            
    except requests.ConnectionError as error:
        print("Cannot connect to the Census API")
        print(error)

def randomize_location(num_pt, polygon):
    """
    Generate num_pt random location coordinates .
    :param num_pt INT number of random location coordinates
    :param polygon geopandas.geoseries.GeoSeries the polygon of the region
    :return x, y lists of location coordinates, longitude and latitude
    """
    # define boundaries
    minx, miny, maxx, maxy = polygon.bounds

    i = 0
    x = []
    y = []
    while i < num_pt:
        # generate random location coordinates
        x_t = np.random.uniform(minx, maxx)
        y_t = np.random.uniform(miny, maxy)
        # further check whether it is in the city area 
        if Point(x_t, y_t).within(polygon):
            x.append(x_t)
            y.append(y_t)
            i = i + 1

    return gpd.GeoSeries(gpd.points_from_xy(x, y), crs="EPSG:4326")

def downloadShapeFile(FIPS, unit_level = 'block'):
    try:
        if (unit_level == 'state'):
            url = "https://www2.census.gov/geo/tiger/TIGER2021/STATE/tl_2021_us_state.zip"
        elif (unit_level == 'county'):
            url = "https://www2.census.gov/geo/tiger/TIGER2021/COUNTY/tl_2021_us_county.zip"
        elif (unit_level == 'tract'):
            url = "https://www2.census.gov/geo/tiger/TIGER2021/TRACT/tl_2021_"+str(FIPS[0:2])+"_tract.zip"
        elif (unit_level == 'block'):
            url = "https://www2.census.gov/geo/tiger/TIGER2021/TABBLOCK20/tl_2021_"+str(FIPS[0:2])+"_tabblock20.zip"
        response = requests.get(url)
        filename = url.split('/')[-1]
        with open(filename,'wb') as output_file:
            output_file.write(response.content)
        print('Downloading Completed')
        response.close()
        return filename

    except requests.ConnectionError as error:
        print("Cannot download ShapeFile")
        print(error)

def loadShapeFile(FIPS, unit_level = 'block'):
        if (unit_level == 'state'):
            filename = "tl_2021_us_state.zip"
        elif (unit_level == 'county'):
            filename = "tl_2021_us_county.zip"
        elif (unit_level == 'tract'):
            filename = "tl_2021_"+str(FIPS[0:2])+"_tract.zip"
        elif (unit_level == 'block'):
            filename = "tl_2021_"+str(FIPS[0:2])+"_tabblock20.zip"
        else:
            raise Exception("Unknown unit level")

        if(not os.path.exists(filename)):
            filename = downloadShapeFile(FIPS, unit_level)

        sf = gpd.read_file(os.path.join(os.getcwd(),filename))
        return sf

        
def getSFDF(FIPS, for_unit='block'):
    df = loadShapeFile(FIPS, for_unit)
    columns = df.columns.values.tolist()
    new_columns = list(map((lambda x: x[:-2] if ("20" in x) else x), columns))
    df = df.rename(columns=dict(zip(columns, new_columns))) 
    print(df)
    df = df[df.GEOID.str.startswith(FIPS)]
    return df