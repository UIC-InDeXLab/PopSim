import sys
import us
from census import Census

# Provide your Census API key here
CENSUS_API_KEY = "a5773d6a02d112006c99d937a349668f50604b5d"

def list_all_states():
    print("All U.S. states and territories with their FIPS codes:")
    for state in us.states.STATES_AND_TERRITORIES:
        print(state.name, state.abbr, state.fips)

def get_tract_data(state_fips: str):
    census_api = Census(CENSUS_API_KEY)
    data = census_api.acs5.get(('NAME',), geo={'for': 'tract:*', 'in': f'state:{state_fips}'})
    return data

def get_block_data(state_fips: str, county_fips: str, tract_code: str):
    census_api = Census(CENSUS_API_KEY)
    data = census_api.sf1.get(('NAME', 'P001001'), geo={'for': 'block:*', 'in': f'state:{state_fips} county:{county_fips} tract:{tract_code}'})
    return data

def get_tigerline_url(geographical_level: str, state_fips: str = None, county_fips: str = None, tract_code: str = None):
    base_url = "https://www2.census.gov/geo/tiger/TIGER2021/"
    
    if geographical_level == "state":
        return f"{base_url}STATE/"
    elif geographical_level == "county":
        if state_fips:
            return f"{base_url}COUNTY/tl_2021_{state_fips}_county.zip"
        else:
            return f"{base_url}COUNTY/"
    elif geographical_level == "tract":
        if state_fips and county_fips:
            return f"{base_url}TRACT/tl_2021_{state_fips}{county_fips}_tract.zip"
        else:
            return f"{base_url}TRACT/"
    elif geographical_level == "block":
        if state_fips and county_fips and tract_code:
            return f"{base_url}TABBLOCK/tl_2021_{state_fips}{county_fips}{tract_code}_tabblock10.zip"
        else:
            return f"{base_url}TABBLOCK/"
    else:
        return None



if __name__ == "__main__":
    list_all_states()
    state_abbr = input("Enter the two-letter state abbreviation: ")
    state = us.states.lookup(state_abbr)
    
    if state:
        geographical_level = input("Enter the grouping level (tract, block): ")
        
        if geographical_level == "tract":
            tract_data = get_tract_data(state.fips)
            print("Tract-level data:")
            for tract in tract_data:
                print(tract)
                
            tigerline_url = get_tigerline_url("tract", state_fips=state.fips)
            print(f"TIGER/Line Shapefile URL for tract level: {tigerline_url}")
            
        elif geographical_level == "block":
            county_fips = input("Enter the county FIPS code: ")
            tract_code = input("Enter the tract code: ")
            block_data = get_block_data(state.fips, county_fips, tract_code)
            print("Block-level data:")
            for block in block_data:
                print(block)
                
            tigerline_url = get_tigerline_url("block", state_fips=state.fips, county_fips=county_fips, tract_code=tract_code)
            print(f"TIGER/Line Shapefile URL for block level: {tigerline_url}")
            
        else:
            print("Invalid geographical level entered.")
            sys.exit(1)
    else:
        print("Invalid state abbreviation entered.")
        sys.exit(1)

