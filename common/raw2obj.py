"""
Copyright (C) 2015 Stanislav Bobovych

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import sys
import struct

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Tool that\'s used to read apitrace raw data dumps of vertex data and print wavefront obj vertices. It can also be used with any other raw data.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', nargs='?', help='Raw file')
    parser.add_argument('--type', required=True, choices=['indices', 'positions', 'texcoords'])
    parser.add_argument('-o', '--offset', default="0x0", help='Offset into file, in hex')
    parser.add_argument('-c', '--count', type=int, default=sys.maxsize, help='Number of vertices')

    args = parser.parse_args()
    path = args.file
    offset = int(args.offset, 16)
    count = args.count
    if count != sys.maxsize:
        if args.type == "indices":
            count = args.count * 3 * 2
        elif args.type == "positions":
            count = args.count * 3 * 4
        elif args.type == "texcoords":
            count = args.count * 2 * 4

    byte_count = 0
    with open(path, 'rb') as f:
        f.seek(offset)
        while byte_count < count:
            if args.type == "indices":
                buf = f.read(3 * 2)  # assume vertex indices are unsigned shorts
                if not buf:
                    break
                v1, v2, v3 = struct.unpack("HHH", buf)
                print("f %i/%i %i/%i %i/%i" % (v1+1, v1+1, v2+1, v2+1, v3+1, v3+1))
                byte_count += 3 * 2
            elif args.type == "positions":
                buf = f.read(3 * 4)
                if not buf:
                    break
                f1, f2, f3 = struct.unpack("fff", buf)
                print("v", f1, f2, f3)
                byte_count += 3 * 4
            elif args.type == 'texcoords':
                buf = f.read(2 * 4)  # assume texture coordinates are floats
                if not buf:
                    break
                u, v, = struct.unpack("ff", buf)
                print("vt", u, v)
                byte_count += 2 * 4

    print("# number of bytes", byte_count)
