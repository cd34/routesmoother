import csv
import math

from geopy.distance import geodesic
import xml.etree.ElementTree as ET

def return_points(points, num_points):
    '''
    we'll always return the first and last point and fill in the rest
    '''
    export_latlongs = []
    x_delta = points[0][0] - points[1][0]
    y_delta = points[0][1] - points[1][1]
    export_latlongs.append({'pos':[ points[0][0], points[0][1] ]})
    for ctr in range(1, num_points):
        export_latlongs.append({'pos':[ points[0][0] - x_delta / num_points * ctr,
            points[0][1] - y_delta / num_points * ctr]})
    export_latlongs.append({'pos':[ points[1][0], points[1][1] ]})
    return(export_latlongs)

def smoother(latlongs, meters):
    prev_latlong = latlongs[0]['pos']   
    export_latlongs = [{'pos':prev_latlong}]

    distance = 0
    for x in latlongs[1:-1]:
        distance += x['distance']
        if distance > meters:
            point_distance = geodesic(x['pos'], prev_latlong).meters
            num_points = math.floor(point_distance / meters) - 2
            if num_points < 1:
                num_points = 1

            '''
            some weird smoothing artifacts happen if we try to play the length, so,
            we'll take the number of points we should have and rather than stay at
            our fixed distance, we'll squish them a little so we don't have a corner
            point off the road.
            '''

            export_latlongs.extend(return_points([prev_latlong, x['pos']], num_points))
            x['pos'] = export_latlongs[-1]['pos']
            distance = 0
        prev_latlong = x['pos']
    
    export_latlongs.append({'pos':latlongs[-1]['pos']})

    return (export_latlongs)

def process_csv(filename):
    with open(filename) as csvfile:
        input_file = csv.reader(csvfile, delimiter=',')
        latlongs = []
        prev_latlong = ()

        for line in input_file:
            distance = 0
            latitude, longitude, description = line
            latitude = float(latitude)
            longitude = float(longitude)
            if prev_latlong:
                distance = geodesic((latitude, longitude),prev_latlong).meters
            prev_latlong = (latitude, longitude)
            latlongs.append({'pos': (latitude, longitude), 'distance': distance, 'description':description})
        return(latlongs)

def process_tcx(filename=None, contents=None):
    tree = ''
    root = ''
    if filename:
        tree = ET.parse(filename)
        root = tree.getroot()
    if contents:
        root = ET.fromstring(contents)

    latlongs = []
    prev_latlong = ()

    for child in root.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Courses'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Course'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Track'). \
            findall('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint'):
        latitude = float(child.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees').text)
        longitude = float(child.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees').text)
        
        distance = 0
        if prev_latlong:
            distance = geodesic((latitude, longitude),prev_latlong).meters
            
        prev_latlong = (latitude, longitude)

        latlongs.append({'pos': (latitude, longitude), 'distance': distance})
    return latlongs
