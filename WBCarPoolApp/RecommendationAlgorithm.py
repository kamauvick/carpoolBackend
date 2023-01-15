import googlemaps
from datetime import datetime


ApiKey=""
# Place Key here 

DriverStart = "UC Irvine"
PassengerStart = "Disneyland"
Destination = "UC Riverside"


gmaps = googlemaps.Client(key=ApiKey)


now = datetime.now()
Firstleg = gmaps.directions(        DriverStart,
                                    PassengerStart,
                                     optimize_waypoints = True,
                                     mode = "driving",
                                     traffic_model = "best_guess",
                                     departure_time = now)

Secondleg = gmaps.directions(        PassengerStart,
                                     Destination,
                                     optimize_waypoints = True,
                                     mode = "driving",
                                     traffic_model = "best_guess",
                                     departure_time = now)


FirstLegDuration = Firstleg[0]['legs'][0]['duration']['value']
SecondLegDuration = Secondleg[0]['legs'][0]['duration']['value']

TotalDuration = FirstLegDuration + SecondLegDuration 

print(TotalDuration)
#should output to csv rather than printing 
