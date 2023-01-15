import googlemaps
from datetime import datetime


ApiKey=""
  # Place Key here 

gmaps = googlemaps.Client(key=ApiKey)
DriverStart = input("Where are you starting from: ") 
PassengerLocations = ["Fresno", "UCSB","CSUSB","UCSC","Museum of Modern Art"]
Destination = input("Where are you going: ")
ExtraMinPerLocation = {
  "Fresno": [] ,
  "UCSB": [],
  "CSUSB": [],
  "UCSC":[],
  "Museum of Modern Art": [],
  }
ExtraMin = []
now = datetime.now()

for locations in PassengerLocations:
    OrignalTime = gmaps.directions( DriverStart,
                                      Destination,
                                      optimize_waypoints = True,
                                      mode = "driving",
                                      traffic_model = "best_guess",
                                      departure_time = now)

    Firstleg = gmaps.directions(    DriverStart,
                                      locations,
                                      optimize_waypoints = True,
                                      mode = "driving",
                                      traffic_model = "best_guess",
                                      departure_time = now)

    Secondleg = gmaps.directions(    locations,
                                      Destination,
                                      optimize_waypoints = True,
                                      mode = "driving",
                                      traffic_model = "best_guess",
                                      departure_time = now)

    OrignalTime = OrignalTime[0]['legs'][0]['duration']['value']
    FirstLegDuration = Firstleg[0]['legs'][0]['duration']['value']
    SecondLegDuration = Secondleg[0]['legs'][0]['duration']['value']

    TotalDuration = FirstLegDuration + SecondLegDuration 
    ExtraTime = TotalDuration - OrignalTime 

    ExtraMin.append(ExtraTime)
    ExtraMinPerLocation[locations].append(ExtraTime)


sorted(ExtraMinPerLocation)
ExtraMin.sort()

BestOption = str(next(iter(ExtraMinPerLocation)))

minutes = round(ExtraMin[0] / 60,2)

print(f"There is someone you can pick up at {BestOption}. And it will only add {minutes} minutes to your route!")
