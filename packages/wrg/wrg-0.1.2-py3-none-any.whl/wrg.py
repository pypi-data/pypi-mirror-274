# -*- coding: utf-8 -*-
#
# wrg.py
#
# Copyright 2017 - 2024 Goyo <goyodiaz@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.


"""Module wrg"""

import itertools

import numpy as np
from scipy.special import gamma

__version__ = "0.1.2"


# return (start, end) pairs from iterable of widths
def _widths2slices(widths):
    cuts = itertools.accumulate(itertools.chain([0], widths))
    a, b = itertools.tee(cuts)
    return tuple(zip(a, itertools.islice(b, 1, None)))


class WRG:
    """Abstraction for WAsP .wrg files."""

    def __init__(self, nx, ny, xmin, ymin, cell_size, names, data):
        """Initialize a WRG instance.

        The parameters are stored as attributes of the same name.

        Parameters
        ----------
        nx, ny : positive int
            Number of columns and rows in the grid.
        xmin, ymin : float
            Coordinates of the point on the SE corner of the grid.
        cell_size : float
            The cell size in meters.
        names : 1D array of strings
            Strings identifying each grid point.
        data : 2d array of numbers
            Each row contains the results for a grid point.
        """
        self.nsectors, mod = divmod(data.shape[1] - 8, 3)
        self.nx = nx
        self.ny = ny
        self.xmin = xmin
        self.ymin = ymin
        self.cell_size = cell_size
        self.names = names
        self.data = data

        if data.shape[0] != nx * ny:
            raise self._wrong_number_of_lines()

        if mod != 0:
            raise self._wrong_number_of_columns()

    def _wrong_number_of_lines(self):
        msg = f"Expected {self.nx * self.ny} rows in data, {self.data.shape[0]} rows found"
        return ValueError(msg)

    def _wrong_number_of_columns(self):
        columns = self.data.shape[1]
        msg = f"Data has {columns} columns, but {columns} - 8 = {columns - 8} is not divisible by 3"
        return ValueError(msg)

    @classmethod
    def from_file(cls, buf, dtype=np.float32):
        """Create a WRG instance from a .wrg file.

        Parameters
        ----------
        buf : readable text file
           Buffer to read from.

        dtype : numpy dtype
            dtype used to store the data.

        Returns
        -------
        grid : WRG
        """
        line = next(buf).split()
        nx, ny = [int(x) for x in line[:2]]
        xmin, ymin, cell_size = [dtype(x) for x in line[2:]]
        line = next(buf)
        nsectors = int(line[69:72])
        buf = itertools.chain([line], buf)

        widths = [10, 10, 10, 8, 5, 5, 6, 15, 3] + nsectors * [4, 4, 5]
        slices = _widths2slices(widths)
        name_start, name_end = slices[0]
        s_result = slices[1:]

        names = []
        data = np.empty((ny * nx, 8 + 3 * nsectors), dtype=dtype)

        for i, line in enumerate(buf):
            names.append(line[name_start:name_end].strip())
            data[i] = [dtype(line[start:end]) for start, end in s_result]

        names = np.array(names)
        return cls(nx, ny, xmin, ymin, cell_size, names, data)

    def raw_shape(self):
        """Return the weibull shape by sector.

        The values returned are multiplied by 100 like in the .wrg file.

        Returns
        -------
        ret : array of shape (ny * nx, nsectors)
        """
        return self.data[:, 10::3]

    def raw_scale(self):
        """Return the weibull scale by sector.

        The values returned are multiplied by 10 like in the .wrg file.

        Returns
        -------
        ret : array of shape (ny * nx, nsectors)
        """
        return self.data[:, 9::3]

    def raw_freq(self):
        """Return the frequencies by sector.

        The values returned are multiplied by 1000 like in the .wrg file.

        Returns
        -------
        ret : array of shape (ny * nx, nsectors)
        """
        return self.data[:, 8::3]

    def scale(self):
        """Return directional weibull scale.

        Returns
        -------
        ret : array of shape (ny, nx, nsectors)
        """
        return self.raw_scale().reshape(self.ny, self.nx, self.nsectors) / 10

    def shape(self):
        """Return directional weibull shape.

        Returns
        -------
        ret : array of shape (ny, nx, nsectors)
        """
        return self.raw_shape().reshape(self.ny, self.nx, self.nsectors) / 100

    def global_scale(self):
        """Return global weibull scale.

        Returns
        -------
        ret : array of shape (ny, nx)
        """
        return self.data[:, 4].reshape(self.ny, self.nx)

    def global_shape(self):
        """Return global weibull shape.

        Returns
        -------
        ret : array of shape (ny, nx)
        """
        return self.data[:, 5].reshape(self.ny, self.nx)

    def global_speed(self):
        """Return global mean speed.

        Compute as the weighted average of the directional mean speed.

        Returns
        -------
        ret : array of shape (ny, nx)
        """
        return np.average(
            self.speed(),
            axis=2,
            weights=self.raw_freq().reshape(self.ny, self.nx, self.nsectors),
        )

    def speed(self):
        """Return the mean speed by sector.

        The speed is computed from the weibull parameters.

        Returns
        -------
        ret : array of shape (ny, nx, nsectors)
        """
        # This is the straightforward way to calculate the mean speed:
        # result = scale / 10 * gamma(1 + 100 / shape)
        # But we do it in several steps in order to improve memory
        # performance.
        result = 100 / self.raw_shape()
        result += 1
        result = gamma(result, out=result)
        result *= self.raw_scale()
        result /= 10
        result = result.reshape(self.ny, self.nx, self.nsectors)
        return result

    def freq(self):
        """Return the frequency of each sector.

        Returns
        -------
        ret : array of shape (ny, nx, nsectors)
        """
        result = self.raw_freq() / 1000
        result = result.reshape(self.ny, self.nx, self.nsectors)
        result = result / np.atleast_3d(result.sum(axis=-1))
        return result

    def elev(self):
        """Return the elevation map.

        Returns
        -------
        ret : array of shape (ny, nx)
        """
        return self.data[:, 2].reshape(self.ny, self.nx)

    def extent(self):
        """Return the extent as (left, right, bottom, top).

        The location of the lower-left and upper-right corners. Helpful
        for plotting with matplotlib's imshow().

        Returns
        -------
        extent : scalars (left, right, bottom, top)
        """
        left = self.xmin - self.cell_size / 2
        right = left + self.nx * self.cell_size
        bottom = self.ymin - self.cell_size / 2
        top = bottom + self.ny * self.cell_size
        return left, right, bottom, top

    def hub_height(self):
        return self.data[0, 3]
