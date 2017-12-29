#!/usr/bin/python

import os
from math import log2

class DiskUsage:
    _suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']

    def disk_usage(self, path):
        if not os.path.exists(path):
            raise Exception('Path %s not exits' % path)

        total = os.path.getsize(path)

        if os.path.isdir(path):
            for fileName in os.listdir(path):
                child = os.path.join(path, fileName)
                total += self.disk_usage(child)

        return total

    def format_size(self, size):
        # determine binary order in steps of size 10
        # (coerce to int, // still returns a float)
        order = int(log2(size) / 10) if size else 0
        # format file size
        # (.4g results in rounded numbers for exact matches and max 3 decimals,
        # should never resort to exponent values)
        return '{:.4g} {}'.format(size / (1 << (order * 10)), self._suffixes[order])