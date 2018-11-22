#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    fdg.vectors
    ~~~~~~~~~~~

    Abstraction for two-dimensional Euclidean vectors.

    © 2015, Public Domain, meisterluk
"""

import math


class Vector:
    """A two-dimensional vector"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def abs(self):
        """Return absolute vector (positive x/y coordinates)"""
        return Vector(abs(self.x), abs(self.y))

    def unit(self):
        """Return unit vector (same vector with length 1)"""
        if len(self) == 0:
            return Vector(0, 0)
        return Vector(1.0 * self.x / len(self), 1.0 * self.y / len(self))

    def length(self):
        """Return Euclidean length of the vector"""
        return math.sqrt(self.x**2 + self.y**2)

    def lengthSquared(self):
        return self.x**2 + self.y**2

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        try:
            return Vector(self.x + other, self.y + other)
        except TypeError:
            return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        try:
            return Vector(self.x - other, self.y - other)
        except TypeError:
            return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        try:
            return Vector(self.x * other, self.y * other)
        except TypeError:
            return Vector(self.x * other.x, self.y * other.y)

    def __pow__(self, power, modulo=None):
        return Vector(pow(self.x, power), pow(self.y, power))

    def scaleBy(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def __truediv__(self, other):
        try:
            return Vector(self.x / other, self.y / other)
        except TypeError:
            return Vector(self.x / other.x, self.y / other.y)

    def __len__(self):
        return int(math.sqrt(self.x**2 + self.y**2))

    def __str__(self):
        if self.x % 1 == 0 and self.y % 1 == 0:
            return '<{:d}, {:d}>'.format(int(self.x), int(self.y))
        else:
            return '<{:04f}, {:04f}>'.format(self.x, self.y)

    __repr__ = __str__
