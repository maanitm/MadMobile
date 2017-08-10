import sys
import const
import googlemaps
import geojsonio
from mapbox import Directions
from modules.navigation import mapping

def run():
    print "Battery Simulation"

    maps = mapping.Mapping()

    coordinates = maps.routeCoordinates('4986 Weathervane Drive, Johns Creek, GA', '11585 Jones Bridge Rd Ste 500, Johns Creek, GA 30022')
    altitudes = maps.altitudesFromCoordinates(coordinates)

    i = 0
    print "# | Coordinate | Distance | Elevation"
    for i in range(len(altitudes)):
        distance = 0
        elevation = 0
        if i is not 0:
            distance = maps.distanceFromCoordinates(coordinates[i-1][0], coordinates[i-1][1], coordinates[i][0], coordinates[i][1])
            elevation = altitudes[i]['elevation'] - altitudes[i - 1]['elevation']
        print str(i) + " " + str(coordinates[i]) + " " + str(distance) + " " + str(elevation)
        i += 1
