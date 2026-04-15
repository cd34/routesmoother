#!/usr/bin/env python3

# Original Author: Barry John Williams
# Creative Commons Attribute-Share Alike 2.5 UK:Scotland Licence

import struct
import sys

# OV2 Format extract from:
# http://lists.gnumonks.org/pipermail/opentom/2005-November/000083.html
# Author: Tor Arntsen tor at spacetec.no

_CHARSET = 'cp1252'
_LATLONG_MULTIPLIER = 100000


def writeOV2(data, filename):
    with open(filename, 'wb') as f:
        type_buf = struct.pack("<B", 2)
        count = 0
        for poiset in data:
            name_str = poiset[0] + '\0'
            name = name_str.encode(_CHARSET)
            lat = poiset[1]
            lng = poiset[2]

            lat_buf = struct.pack("<i", int(lat * _LATLONG_MULTIPLIER))
            lng_buf = struct.pack("<i", int(lng * _LATLONG_MULTIPLIER))
            name_buf = struct.pack("<%ds" % len(name), name)
            name_length = struct.calcsize("<%ds" % len(name))
            size_buf = struct.pack("<I", name_length + 13)

            f.write(type_buf)
            f.write(size_buf)
            f.write(lat_buf)
            f.write(lng_buf)
            f.write(name_buf)

            count += 1

    return count


def readOV2(filename):
    data = set()
    type0s = 0
    type1s = 0

    with open(filename, 'rb') as f:
        while True:
            buf = f.read(1)
            if not buf:
                break

            record_type = struct.unpack_from("<B", buf)[0]

            if record_type == 0:
                # Deleted Record
                type0s += 1
                size = struct.unpack_from("<I", f.read(4))[0]
                f.read(size - 5)
            elif record_type == 1:
                # Proprietary Record
                type1s += 1
                f.read(20)
            elif record_type == 2:
                # Normal Record
                size = struct.unpack_from("<I", f.read(4))[0]
                lng = struct.unpack_from("<i", f.read(4))[0] / _LATLONG_MULTIPLIER
                lat = struct.unpack_from("<i", f.read(4))[0] / _LATLONG_MULTIPLIER
                namesize = size - 13
                if namesize < 256:
                    name_bytes = f.read(namesize)
                    name = struct.unpack_from("<%ds" % namesize, name_bytes)[0]
                    stripped = name[:-1].decode(_CHARSET).replace('"', '').strip()
                    data.add((stripped, lat, lng))
            elif record_type == 3:
                # Extended Record
                size = struct.unpack_from("<I", f.read(4))[0]
                lng = struct.unpack_from("<i", f.read(4))[0] / _LATLONG_MULTIPLIER
                lat = struct.unpack_from("<i", f.read(4))[0] / _LATLONG_MULTIPLIER
                datasize = size - 13
                if datasize < 256:
                    data_bytes = f.read(datasize)
                    databuffer = struct.unpack_from("<%ds" % datasize, data_bytes)[0]
                    name_part = databuffer.split(b'\0')[0]
                    stripped = name_part.decode(_CHARSET).replace('"', '').strip()
                    data.add((stripped, lat, lng))
            else:
                print("FATAL: OV2 Type %s Parsing Not Implemented (%s)" % (record_type, filename))
                print("Aborting")
                break

    if type0s > 1:
        print("INFO: %s OV2 Type 0 (Deleted Record) Ignored" % type0s)
    if type1s > 1:
        print("INFO: %s OV2 Type 1 (Proprietary Records) Ignored" % type1s)

    return data


if __name__ == '__main__':
    load_filename = sys.argv[1]
    print("Reading %s" % load_filename)
    dataset = readOV2(load_filename)
    for node in dataset:
        print("%s: %s,%s" % node)
