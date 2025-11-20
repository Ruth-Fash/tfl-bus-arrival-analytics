import requests



def get_lat_lon():
    url = "https://api.tfl.gov.uk/Place/Search"
    params = {"name":"barking and dagenham",
            "types":"Boroughs",}

    response = requests.get(url, params=params) # HTTP response
    print(f"url:{response.url}")
    print(f"response code:{response.status_code}")

    data = response.json()
    # print(type(data)) # type = list - so i knwo how to call the relevant data

    if not data:
        raise ValueError("ERROR: No data retrieved from API")

    else:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        if lat is None or lon is None:
            raise ValueError("ERROR: No data retrieved from API")
        return lat,lon


# Check stop types against API 
def check_stop_type():
    stop_types = ["NaptanPublicBusCoachTram",
                  "NaptanOnstreetBusCoachStopPair", "NaptanBusWayPoint",
                  "NaptanOnstreetBusCoachStopCluster"]

    url = "https://api.tfl.gov.uk/StopPoint/Meta/StopTypes"

    response = requests.get(url)
    data = response.json()
    missing_stop_type = [t for t in stop_types if t not in data]

    if missing_stop_type:
        raise ValueError(f"Stop type {missing_stop_type} does not exist")
    else:
        return stop_types



def get_stop_points():
    stop_point_list = []

    url = "https://api.tfl.gov.uk/StopPoint/"
    lat, lon = get_lat_lon()
    print(lat,lon)
    
    stop_type = check_stop_type()

    for t in stop_type:
        params = {"lat": lat, 
                "lon": lon,
                "stopTypes": t,
                "modes":"bus",
                "radius": 1500}
        
        response = requests.get(url, params=params)
        data = response.json()
        stop_points = data.get("stopPoints", [])
        naptan_id = [stop["naptanId"] for stop in stop_points]
        
        print(t)
        stop_point_list.extend(naptan_id)
        print (stop_point_list)
            








get_stop_points()

