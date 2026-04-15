RouteSmoother
=============

A tool to take a .tcx or .csv file and create a .csv file with fewer points during turns and filled
in points in long, straight stretches.

For Garmin Nuvi or TomTom Via units.

To install:

    python3 -m venv venv
    source venv/bin/activate
    pip install -e .

Usage:

    python process.py --garmin route.tcx      # Output Garmin CSV
    python process.py --tomtom route.tcx       # Output TomTom CSV
    python process.py --google route.csv       # Output Google Maps JS
    python process.py --spacing 200 route.tcx  # Custom spacing (default 150m)
    python process.py --nosmooth route.tcx     # Convert without smoothing

TomTom OV2 File Creation:

    For TomTom, create an .ov2 file using http://www.poieditor.com/
