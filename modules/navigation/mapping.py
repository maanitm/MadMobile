import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import const
import googlemaps
from mapbox import Directions
from math import radians, cos, sin, asin, sqrt

class Mapping(object):
    gmaps = googlemaps.Client(key=const.googleMapsApiKey)

    def __init__(self, ):
        pass

    def addressToCoordinate(self, address):
        geocode = self.gmaps.geocode(address)
        return [geocode[0]['geometry']['location']['lat'], geocode[0]['geometry']['location']['lng']]

    def routeCoordinates(self, fromLoc, toLoc):
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

        response = service.directions([origin, destination], 'mapbox.driving')
        routes = response.geojson()

        return routes['features'][0]['geometry']['coordinates']

    def altitudesFromCoordinates(self, coordinates):
            altitudes = self.gmaps.elevation_along_path(coordinates, len(coordinates))
            return altitudes

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
