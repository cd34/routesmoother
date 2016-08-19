RouteSmoother
=============

A tool to take a .tcx or .csv file and create a .csv file with fewer points during turns and filled
in points in long, straight stretches.

For Garmin Nuvi or TomTom Via units.

To install:

    virtualenv /var/www/routesmoother
    cd /var/www/routesmoother
    source bin/activate
    git clone git@github.com:cd34/routesmoother.git rs
    cd rs
    python setup.py develop

TomTom File Creation
====================

For TomTom, create an .ov2 file

    http://www.poieditor.com/
