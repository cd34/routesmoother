#!/usr/bin/env python3

import argparse

import routesmoother


def main(args):
    latlongs = []
    if args.filename.endswith('.tcx'):
        latlongs = routesmoother.process_tcx(filename=args.filename)
    if args.filename.endswith('.csv'):
        latlongs = routesmoother.process_csv(args.filename)
    if len(latlongs) > 0:
        smoothed_latlongs = latlongs
        if not args.nosmooth:
            smoothed_latlongs = routesmoother.smoother(latlongs, args.spacing)

        for count, latlong in enumerate(smoothed_latlongs):
            if args.garmin:
                print('{}, {}, {}, {}'.format(latlong['pos'][1], latlong['pos'][0], count, count))
            if args.tomtom:
                print('{}, {}, "{}"'.format(latlong['pos'][1], latlong['pos'][0], count))
            if args.google:
                print('{{ lat:{}, lng:{} }},'.format(latlong['pos'][0], latlong['pos'][1]))
    else:
        print("Didn't get any Lat/Longs")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Smooth a .tcx or .csv route file.')
    parser.add_argument('--garmin', action='store_true',
                        help='output .csv for Garmin')
    parser.add_argument('--tomtom', action='store_true',
                        help='output .csv for TomTom')
    parser.add_argument('--google', action='store_true',
                        help='output Javascript for Google Maps')
    parser.add_argument('--nosmooth', action='store_true',
                        help="just convert, don't smooth")
    parser.add_argument('--spacing', action='store', type=int,
                        default=150, help='default of 150 meters between dots')
    parser.add_argument('filename', type=str,
                        help='file to be converted')
    args = parser.parse_args()
    main(args)
