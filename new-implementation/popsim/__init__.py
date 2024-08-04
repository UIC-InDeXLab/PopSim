from .utils import dataframeToHtml, fetch_variables, fetch_datasets, fetch_geography

# Define a function that initializes package-level state
def initialize():
    global counter
    counter = 0