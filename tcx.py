from geopy.distance import vincenty
import xml.etree.ElementTree as ET

def process_tcx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

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
            distance = vincenty((latitude, longitude),prev_latlong).meters
            
        prev_latlong = (latitude, longitude)

        latlongs.append({'pos': (latitude, longitude), 'distance': distance})
    return latlongs
