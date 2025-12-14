import requests
import pandas as pd
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
from src.bigquery_load import *
from src.get_city import get_city_from_latlon
from dotenv import load_dotenv
import os
load_dotenv()

def get_open_charge_map_poi(countrycode):
    """
    Retrieve POI (charging station) data from OpenChargeMap by country code.
    
    Parameters:
        country_code (str): ISO country code (e.g., "US", "UK", "LK")

    Returns:
        list: JSON list of charging points
    """

    base_url = "https://api.openchargemap.io/v3/poi/"

    # Your OpenChargeMap API Key
    api_key = os.getenv("OCM_API_KEY")

    params = {
        "output": "json",
        "countrycode": countrycode,
        "maxresults": 60000,
        "compact": False,
        "verbose": False
    }

    headers = {
        "X-API-Key": api_key
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    return response.json()


def normalize_poi_data(data):
    """
    Normalize POI JSON data into a flat Pandas DataFrame.

    Parameters
    ----------
    data : list of dict
        List of POI records containing address and connection details.

    Returns
    -------
    pandas.DataFrame
        Flattened DataFrame with one row per connection.
    """
    rows = []

    for item in data:
        addr = item.get("AddressInfo", {})

        base = {
            # Root-level
            "ID": item.get("ID"),
            "UUID": item.get("UUID"),
            "UsageCost": item.get("UsageCost"),
            "NumberOfPoints": item.get("NumberOfPoints"),
            "StatusTypeID": item.get("StatusTypeID"),

            # AddressInfo fields
            "AddressInfoID": addr.get("ID"),
            "Title": addr.get("Title"),
            "AddressLine1": addr.get("AddressLine1"),
            "AddressLine2": addr.get("AddressLine2"),
            "Town": addr.get("Town"),
            "StateOrProvince": addr.get("StateOrProvince"),
            "Postcode": addr.get("Postcode"),
            "CountryID": addr.get("CountryID"),
            "Latitude": addr.get("Latitude"),
            "Longitude": addr.get("Longitude"),
            "DistanceUnit": addr.get("DistanceUnit"),
        }

        # Expand each connection as a row
        for conn in item.get("Connections", []):
            row = base.copy()
            row.update({
                "ConnectionID": conn.get("ID"),
                "PowerKW": conn.get("PowerKW"),
                "Amps": conn.get("Amps"),
                "Voltage": conn.get("Voltage"),
                "Quantity": conn.get("Quantity"),
                "LevelID": conn.get("LevelID"),
                "ConnectionTypeID": conn.get("ConnectionTypeID"),
                "StatusTypeID_Connection": conn.get("StatusTypeID"),
                "CurrentTypeID": conn.get("CurrentTypeID"),
            })
            rows.append(row)

    return pd.DataFrame(rows)


def get_data_for_city():
    """
    Fetch POI data, filter points inside City of London, fill missing town values.

    Returns:
        dataframe: dataframe with charging points information
    """

    countrycode = "GB"
    place_name = "City of London, Greater London, England, United Kingdom"

    try:
        # Fetch POI data from OpenChargeMap
        data = get_open_charge_map_poi(countrycode)
        print(f"Total results: {len(data)}")

        if not data:
            print("No data found.")
            return

        # Normalize JSON into dataframe
        df = normalize_poi_data(data)

        # Get city boundary polygon from OSM for London City
        gdf_boundary = ox.geocode_to_gdf(place_name)
        central_london_polygon = gdf_boundary.loc[0, 'geometry']

        # Convert lat/lon to GeoDataFrame
        geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
        gdf_points = gpd.GeoDataFrame(df, geometry=geometry, crs=gdf_boundary.crs)

        # Filter points inside polygon
        central_london_gdf = gdf_points[gdf_points.within(central_london_polygon)]

        # Drop geometry column for final CSV
        central_london_df = pd.DataFrame(central_london_gdf.drop(columns='geometry'))

        # Fill missing Town values using reverse geocoding
        for idx, row in central_london_df[central_london_df['Town'].isna()].iterrows():
            city = get_city_from_latlon(row['Latitude'], row['Longitude'])
            central_london_df.at[idx, 'Town'] = city

        # Save filtered results
        central_london_df.to_csv("geo_london.csv", index=False)

        #return dataframe
        return central_london_df

    except Exception as e:
        print("An error occurred:", e)

        return None
    
        

if __name__ == "__main__":

    df = get_data_for_city()

    load_and_merge_to_bigquery(
        df=df,
        project_id="stone-passage-247604",
        dataset_id="staging_ev",
        staging_table="staging_tbl",
        key_path="service-account.json")