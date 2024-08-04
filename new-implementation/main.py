# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import Union, List

from fastapi.templating import Jinja2Templates
import json
import pandas as pd
from popsim import dataframeToHtml, fetch_datasets, fetch_variables, fetch_geography
app = FastAPI()
# app.mount("", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class JsonData(BaseModel):
    key: str
    data: Union[object, List[str]]
    
storage = {}

@app.on_event("startup")
def initialize():
    global storage
    storage = {}


@app.get("/")
async def read_root(request: Request):
    print('storage', storage)
    # datasets = fetch_datasets()
    datasets = pd.read_json("datasets.json") 
    storageVariables = None
    storageGeography = None
    if "variables" in storage:
        geography = fetch_geography(storage["dataset"]["c_geographyLink"])
        variables = fetch_variables(storage["dataset"]["c_variablesLink"])
        if "variables" in storage:
            storageVariables = variables.loc[variables.index.isin(json.loads(storage["variables"]))]
        if "geography" in storage:
            storageGeography = geography.loc[geography['name'] == storage["geography"]]
    return templates.TemplateResponse("index.html", {"request": request, "chosen_data":storage["dataset"] if ("dataset" in storage) else None , "variables": dataframeToHtml(storageVariables) if ("variables" in storage) else None , "geography": dataframeToHtml(storageGeography) if ("geography" in storage) else None , "table":dataframeToHtml(datasets)})
    
    return templates.TemplateResponse("index.html", {"request": request,  "chosen_data":storage["dataset"] if ("dataset" in storage) else None , "variables": storage["variables"]if ("variables" in storage) else None , "geography": storage["geography"] if ("geography" in storage) else None , "table":dataframeToHtml(datasets)})

@app.get("/variable")
async def read_variables(request: Request):
    print('storage', storage)
    if "dataset" in storage:
        print(storage["dataset"])
        geography = fetch_geography(storage["dataset"]["c_geographyLink"])
        variables = fetch_variables(storage["dataset"]["c_variablesLink"])
        storageVariables = None
        storageGeography = None
        if "variables" in storage:
            storageVariables = variables.loc[variables.index.isin(json.loads(storage["variables"]))]
        if "geography" in storage:
            storageGeography = geography.loc[geography['name'] == storage["geography"]]
        return templates.TemplateResponse("variable_page.html", {"request": request, "dataset": storage["dataset"], "variables": dataframeToHtml(storageVariables) if ("variables" in storage) else None , "geography": dataframeToHtml(storageGeography) if ("geography" in storage) else None , "table":dataframeToHtml(variables)})
    else:
        return RedirectResponse(url="/", status_code=303)

@app.get("/geography")
async def read_variables(request: Request):
    print('storage', storage)
    if "dataset" in storage:
        print(storage["dataset"])
        geography = fetch_geography(storage["dataset"]["c_geographyLink"])
        variables = fetch_variables(storage["dataset"]["c_variablesLink"])
        storageVariables = None
        storageGeography = None
        if "variables" in storage:
            storageVariables = variables.loc[variables.index.isin(json.loads(storage["variables"]))]
        if "geography" in storage:
            storageGeography = geography.loc[geography['name'] == storage["geography"]]
        return templates.TemplateResponse("geography.html", {"request": request, "dataset": storage["dataset"], "variables": dataframeToHtml(storageVariables) if ("variables" in storage) else None , "geography": dataframeToHtml(storageGeography) if ("geography" in storage) else None , "table":dataframeToHtml(geography)})
    else:
        return RedirectResponse(url="/", status_code=303)

@app.post("/send-json/")
async def send_json(json_data: JsonData):
    print('\n\n\njson_data', json_data)

    if(json_data.key == "dataset"):
        if("datasets" in storage and json_data.data in storage["datasets"]):
            return {"detail": "Data already exists"}
        storage[json_data.key] = json.loads(json_data.data)
        if("variables" in storage):
            del storage["variables"]
        # del storage["variables"]
    elif(json_data.key == "variables"):
        storage[json_data.key] = json_data.data
    elif(json_data.key == "geography"):
        storage[json_data.key] = json.loads(json_data.data)
    return {"detail": "Data received and stored"}

def get_census_data(dataset_url, chosen_variables, chosen_geography):
    """
    Fetch data from the Census API for a given dataset, variables, and geography level.

    Args:
        dataset_url (str): The dataset API endpoint URL.
        chosen_variables (dict): A dictionary of selected variable names and their metadata.
        chosen_geography (dict): A dictionary of selected geography level and its metadata.

    Returns:
        list: The retrieved data in JSON format.
    """
    print('chosen_variables', chosen_variables)
    print('chosen_geography', chosen_geography)
    print('dataset_url', dataset_url)
    # Extract variable names from the chosen_variables dictionary
    variables_str = ','.join(chosen_variables)


    # Extract the geography level and its hierarchy from the chosen_geography dictionary
    geography_level = chosen_geography["name"]
    geography_hierarchy = chosen_geography["requires"]

    # Build the API request
    request_url = f"{dataset_url}?get={variables_str}&for={geography_level}:*"
    request_url += "".join([f"&in={hierarchy}:<YOUR_CHOICE>" for hierarchy in geography_hierarchy])

    request_url += f"&key=<YOUR_API_KEY>"


    return request_url

@app.get("/get-full-url/")
async def get_full_url(request: Request):
    if "dataset" in storage and "variables" in storage and "geography" in storage:
        geography = fetch_geography(storage["dataset"]["c_geographyLink"])
        variables = fetch_variables(storage["dataset"]["c_variablesLink"])
        c_dataset = storage["dataset"]['c_dataset']
        c_dataset_url = "https://api.census.gov/data/" + "/".join(c_dataset[1:-1].split(", "))
        storageGeography = geography.loc[geography['name'] == storage["geography"]].to_dict('records')[0]
        print("storageGeography", storageGeography)
        storageVariables = variables.loc[variables.index.isin(json.loads(storage["variables"]))].index.tolist()
        print(storageVariables)
        print(storageGeography)
        return  get_census_data(c_dataset_url, storageVariables, storageGeography)
    return None



@app.get("/get-json/{key}")
async def get_json(key: str):
    if key in storage:
        return storage[key]
    return None
