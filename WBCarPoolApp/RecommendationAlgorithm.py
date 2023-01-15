import googlemaps
from datetime import datetime


ApiKey = ""
# Place Key here 

gmaps = googlemaps.Client(key=ApiKey)
# Passes api key to each query 

DriverStart = input("Where are you starting from: ") 
PassengerLocations = ["Castle Park", "California Citrus State Historic Park","UC Riverside Botanic Gardens","Andulka Park",]
Destination = input("Where are you going: ")
# Collecting data from user as well as defining locations of potenial riders
  
ExtraMinPerLocation = {
  "Castle Park": [] , 
  "California Citrus State Historic Park": [],
  "UC Riverside Botanic Gardens": [],
  "Andulka Park":[],
  "Riverside Art Museum": [],
  }
ExtraMin = []
# Sets up a dic and list wich will be used for operations later 
now = datetime.now()
# Gets current time 

for locations in PassengerLocations: 
  # For every location in the list of passenger locations the following caluclations are completed 
    OrignalTime = gmaps.directions( DriverStart,
                                      Destination,
                                      optimize_waypoints = True,
                                      mode = "driving",
                                      traffic_model = "best_guess",
                                      departure_time = now)
# Calls first query asking for duration of the drivers orginal dirve 
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
# Second two queries are from drivers start to riders start and riders start to the destination 

    OrignalTime = OrignalTime[0]['legs'][0]['duration']['value']
    FirstLegDuration = Firstleg[0]['legs'][0]['duration']['value']
    SecondLegDuration = Secondleg[0]['legs'][0]['duration']['value']
# Parses Data from API 

    TotalDuration = FirstLegDuration + SecondLegDuration 
    ExtraTime = TotalDuration - OrignalTime 

    ExtraMin.append(ExtraTime)
    ExtraMinPerLocation[locations].append(ExtraTime)
    # Finds how much added time the ride will take and adds it to the list and dic from before 


sorted(ExtraMinPerLocation)
ExtraMin.sort()
# Sorts so the shortest time will come first

BestOption = str(next(iter(ExtraMinPerLocation)))
# Grabs the best option from the front of the list

minutes = round(ExtraMin[0] / 60,2)
# Grabs the added time in seconds thne turns it into min and rounds 

print(f"There is someone you can pick up at {BestOption}. And it will only add {minutes} minutes to your route!")
# Prints results
