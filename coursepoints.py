import xml.etree.ElementTree as ET

def process_tcx(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    latlongs = []
    prev_latlong = ()

    '''
      <CoursePoint>
        <Name>P</Name>
        <Time>2019-06-11T13:21:41Z</Time>
        <Position>
          <LatitudeDegrees>37.29355735411471</LatitudeDegrees>
          <LongitudeDegrees>-108.04525352743143</LongitudeDegrees>
        </Position>
        <PointType>Left</PointType>
        <Notes>P</Notes>
      </CoursePoint>
    '''

    for child in root.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Courses'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Course'). \
            findall('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}CoursePoint'):
        latitude = float(child.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LatitudeDegrees').text)
        longitude = float(child.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Position'). \
            find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}LongitudeDegrees').text)
        name = child.find('{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Name').text

        latlongs.append({'pos': (latitude, longitude), 'name': name})
    return latlongs
