#!/usr/bin/env python

import argparse
import os

import routesmoother
import coursepoints

PULLOUT_TYPE = { 'D':'D', 'DP':'D', 'L':'L', 'LD':'LD', 'LP':'L', 'P':'P', 'XL':'XL' }

def main(args):
    latlongs = []
    file = {}
    if args.filename.endswith('.tcx'):
        latlongs = coursepoints.process_tcx(filename=args.filename)
    for count,latlong in enumerate(latlongs):
        if latlong['name'] in PULLOUT_TYPE:
           name = PULLOUT_TYPE[latlong['name']]
           if name not in file:
               file[name] = open(os.path.join(args.path, f'{name}.csv'), 'w')
           file[name].write('{}, {}, "{} {}"\n'.format(latlong['pos'][1], latlong['pos'][0], name, str(count)))

parser = argparse.ArgumentParser(description='generate coursepoint .csvs')
parser.add_argument('filename', type=str,
                    help='file to be converted')
parser.add_argument('path', type=str,
                    help='path for files')
args = parser.parse_args()
main(args)
