import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import const
sys.path.append('../libraries/directions/')
import directions
import googlemaps
from math import radians, cos, sin, asin, sqrt

print const.projectName

gmaps = googlemaps.Client(key=const.googleMapsApiKey)

def routeCoordinates(fromLoc, toLoc):
    mq = directions.Google(const.googleMapsApiKey)
    routes = mq.route(fromLoc, toLoc)
    json = routes[0].geojson()
    features = json['features']
    feature = features[0]
    geometry = feature['geometry']
    coordinates = geometry['coordinates']
    return coordinates

def altitudesFromCoordinates(coordinates):
        altitudes = gmaps.elevation_along_path(coordinates, len(coordinates))
        return altitudes

def distanceFromCoordinates(lon1, lat1, lon2, lat2, metric=False):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c

    if metric:
        return km
    else:
        return km * 0.62

coordinates = routeCoordinates('4986 Weathervane Drive, Johns Creek, GA', '11585 Jones Bridge Rd Ste 500, Johns Creek, GA')
altitudes = altitudesFromCoordinates(coordinates)

i = 0
print "# | Coordinate | Distance | Elevation"
for i in range(len(altitudes)):
    distance = 0
    elevation = 0
    if i is not 0:
        distance = distanceFromCoordinates(coordinates[i-1][0], coordinates[i-1][1], coordinates[i][0], coordinates[i][1])
        elevation = altitudes[i]['elevation'] - altitudes[i - 1]['elevation']
    print str(i) + " " + str(coordinates[i]) + " " + str(distance) + " " + str(elevation)
    i += 1
