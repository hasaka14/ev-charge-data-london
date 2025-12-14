import requests

def get_city_from_latlon(lat, lon):
    """
    Get city name from latitude and longitude.

    Parameters
    ----------
    lat : float
        Latitude value.
    lon : float
        Longitude value.

    Returns
    -------
    str or None
        City name if found, otherwise None.
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1
        }
        response = requests.get(url, params=params, headers={"User-Agent": "geoapi"})
        response.raise_for_status()
        data = response.json()
        
        address = data.get("address", {})
        city = address.get("city") or address.get("town") or address.get("village")
 
        return city
    except Exception as e:
        print(f"Error fetching city: {e}")
        return None