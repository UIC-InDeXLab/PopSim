import requests
import pyld
import pandas as pd

def dataframeToHtml(dataframe):
    html = '<table border="1" class="dataframe">'

    # Add header row
    html += "<thead id='header' style='text-align: right;''><tr>"
    html+= '<th>index</th>'
    for column in dataframe.columns:
        html += '<th>' + column + '</th>'
    html += '</tr></thead>'

    # Add data rows
    html += '<tbody>'
    for index in dataframe.index:
        html += '<tr onclick="rowClick(event)">'
        html += '<th>' + str(index) + '</th>'
        for column in dataframe.columns:
            html += '<td>' + str(dataframe.loc[index, column]) + '</td>'
        html += '</th>'
    html += '</tbody>'

    html += '</table>'
    return html

def fetch_jsonld_data(url):
    """
    Fetches a JSON-LD file from the specified URL and returns it as a Python dictionary or a list of dictionaries.
    """
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        # Retrieve the JSON-LD data from the response
        jsonld_data = response.json()

        # Return the parsed data
        return jsonld_data
    else:
        # If the response was not successful, raise an exception
        raise Exception(f"Error: {response.status_code}")

def fetch_json_data(url):
    """
    Fetches a JSON file from the specified URL and returns it as a Python dictionary or a list of dictionaries.
    """
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the response was successful (status code 200)
    if response.status_code == 200:
        # Retrieve the JSON data from the response
        json_data = response.json()

        # Return the JSON data
        return json_data
    else:
        # If the response was not successful, raise an exception
        raise Exception(f"Error: {response.status_code}")

def load_jsonld_data(jsonld_data):
    """
    Parses the specified JSON-LD data into a Pandas DataFrame.
    """
    jsonld_data = jsonld_data["@graph"]
    # Check if the JSON-LD data is a dictionary or a list of dictionaries
    if isinstance(jsonld_data, dict):
        # Convert the dictionary to a Pandas DataFrame
        df = pd.DataFrame([jsonld_data])
    elif isinstance(jsonld_data, list):
        # Convert the list of dictionaries to a Pandas DataFrame
        df = pd.DataFrame(jsonld_data)
    else:
        # If the JSON-LD data is neither a dictionary nor a list, raise an exception
        raise Exception("Error: Invalid JSON-LD data")

    # Return the DataFrame
    return df


def fetch_variables(url):
    """
    Fetches a JSON file from the specified URL and returns it as a Pandas DataFrame.
    """
    # Fetch JSON data from the given URL
    
    json_data = fetch_json_data(url)
    json_data_variables = json_data["variables"]

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame.from_dict(json_data_variables, orient='index')

    return df


def fetch_datasets():
    """
    Fetches a total datasets file from the specified URL and returns it as a Pandas DataFrame.
    """
    # Define the URL of the JSON-LD file
    url = "https://api.census.gov/data.json"
    
    # Fetch JSON-LD data from the given URL
    jsonld_data = fetch_jsonld_data(url)

    # Parse the JSON-LD data into a Pandas DataFrame
    context = "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld"
    options = {
        'documentLoader': pyld.jsonld.requests_document_loader(),
        'remote_contexts': {}
    }
    # create a JSON-LD frame to extract only objects with dcat:Dataset @type
    frame = {
        "@context": "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld",
        "@type": "Dataset"
    }

    # extract only the JSON-LD objects with dcat:Dataset @type using the frame
    parsed_data = pyld.jsonld.compact(jsonld_data, context, options=options)
    filtered_jsonld = pyld.jsonld.frame(parsed_data, frame)
    flattened_data = pyld.jsonld.flatten(filtered_jsonld)
    dataset = pd.DataFrame.from_records(filtered_jsonld["@graph"])

    dataset = dataset[dataset["accessLevel"] == "public"]
    dataset = dataset.sort_values("temporal", ascending=False).reset_index(drop=True)
    dataset = dataset[ ['title'] + [ col for col in dataset.columns if col != 'title' ] ]

    return dataset

def fetch_geography(url):

    # Fetch JSON data from the given URL
    
    json_data = fetch_json_data(url)
    json_data_variables = json_data["fips"]

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(json_data_variables)

    return df

