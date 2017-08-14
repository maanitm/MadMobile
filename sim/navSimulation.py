import sys
import const
from modules.navigation import mapping
import geojsonio
import json

def run(start, end):
    print("Navigation Simulation")

    maps = mapping.Mapping()

    routes = maps.getDirection(start, end).geojson()
    geojsonio.display(json.dumps(routes['features'][0], indent = 0))
    distanceMeters = maps.distanceBetweeenLocations(start, end)

    print(str(distanceMeters / 1000) + "km . " + str(distanceMeters * 0.000621371) + " mi")

    print("Press enter to continue calculations or ^C to exit")
    res = input()

    coordinates = maps.routeCoordinates(start, end)
    altitudes = maps.altitudesFromCoordinates(coordinates)

    print(len(coordinates))

    i = 0
    print("# | Coordinate | Distance | Elevation")
    for i in range(len(coordinates)):
        distance = 0
        elevation = 0
        if i is not 0:
            distance = maps.distanceFromCoordinates(coordinates[i-1][0], coordinates[i-1][1], coordinates[i][0], coordinates[i][1])
            elevation = altitudes[i]['elevation'] - altitudes[i - 1]['elevation']
        print(str(i) + " " + str(coordinates[i]) + " " + str(distance) + " " + str(elevation))
        i += 1
