##############################################################################
#
# Copyright (c) 2022 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
#
##############################################################################
import struct
import unittest

from .... import zope
from ....zope import interface as ___vendorize__0
zope.interface = ___vendorize__0


class TestFloatingPoint(unittest.TestCase):

    def test_no_fast_math_optimization(self):
        # Building with -Ofast enables -ffast-math, which sets certain FPU
        # flags that can cause breakage elsewhere.  A library such as BTrees
        # has no business changing global FPU flags for the entire process.
        zero_bits = struct.unpack("!Q", struct.pack("!d", 0.0))[0]
        next_up = zero_bits + 1
        smallest_subnormal = struct.unpack("!d", struct.pack("!Q", next_up))[0]
        self.assertNotEqual(smallest_subnormal, 0.0)
