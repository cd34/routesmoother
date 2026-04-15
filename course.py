#!/usr/bin/env python3

import argparse
import os

import coursepoints

PULLOUT_TYPE = {'D': 'D', 'DP': 'D', 'L': 'L', 'LD': 'LD', 'LP': 'L', 'P': 'P', 'XL': 'XL'}


def main(args):
    latlongs = []
    files = {}
    if args.filename.endswith('.tcx'):
        latlongs = coursepoints.process_tcx(filename=args.filename)
    try:
        for count, latlong in enumerate(latlongs):
            if latlong['name'] in PULLOUT_TYPE:
                name = PULLOUT_TYPE[latlong['name']]
                if name not in files:
                    files[name] = open(os.path.join(args.path, f'{name}.csv'), 'w')
                files[name].write('{}, {}, "{} {}"\n'.format(
                    latlong['pos'][1], latlong['pos'][0], name, count))
    finally:
        for f in files.values():
            f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate coursepoint .csvs')
    parser.add_argument('filename', type=str,
                        help='file to be converted')
    parser.add_argument('path', type=str,
                        help='path for files')
    args = parser.parse_args()
    main(args)
