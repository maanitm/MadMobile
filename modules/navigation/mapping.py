import const
import googlemaps
from mapbox import Directions
from math import radians, cos, sin, asin, sqrt

# this class is used to get navigation based data and convert values
class Mapping(object):
    # connect to the googlemaps client using GMaps API Key
    gmaps = googlemaps.Client(key=const.googleMapsApiKey)

    # initialize class with no arguments
    def __init__(self):
        pass

    def getDirection(self, fromLoc, toLoc):
        loc1 = self.addressToCoordinate(fromLoc)
        loc2 = self.addressToCoordinate(toLoc)

        service = Directions(access_token=const.mapboxApiKey)
        origin = {
            'type': 'Feature',
            'properties': {'name': fromLoc},
            'geometry': {
                'type': 'Point',
                'coordinates': [loc1[1], loc1[0]]
            }
        }
        destination = {
            'type': 'Feature',
            'properties': {'name': toLoc},
            'geometry': {
                'type': 'Point',
                'coordinates': [loc2[1], loc2[0]]
            }
        }

        return service.directions([origin, destination], 'mapbox.walking')

    def distanceBetweeenLocations(self,fromLoc, toLoc):
        response = self.getDirection(fromLoc, toLoc)
        routes = response.geojson()
        return routes['features'][0]['properties']['distance']

    # convert address to coordinate using GMaps Geocode API
    def addressToCoordinate(self, address):
        geocode = self.gmaps.geocode(address)
        return [geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']]

    # convert a route to geojson using Mapbox Direction API then coordinates from LineString
    def routeCoordinates(self, fromLoc, toLoc):
        response = self.getDirection(fromLoc, toLoc)

        routes = response.geojson()

        return routes['features'][0]['geometry']['coordinates']

    # get altitude of each coordinate in array using GMaps Elevation API
    def altitudesFromCoordinates(self, coordinates):
            if len(coordinates) < 512:
                altitudes = self.gmaps.elevation_along_path(coordinates, len(coordinates))
            else:
                altitudes = []
                for coord in coordinates:
                    altitudes.append(self.gmaps.elevation([coord])[0])
            return altitudes

    # get distance between lat and lon of 2 coordinates (default to imperial system)
    def distanceFromCoordinates(self, lon1, lat1, lon2, lat2, metric=False):
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
