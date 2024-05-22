from __future__ import annotations

from typing import List, Tuple

import healpy as hp
import numpy as np
from typing_extensions import TypeAlias

from hipscat.pixel_math import HealpixPixel
from hipscat.pixel_math.filter import get_filtered_pixel_list
from hipscat.pixel_tree.pixel_tree import PixelTree

# Pair of spherical sky coordinates (ra, dec)
SphericalCoordinates: TypeAlias = Tuple[float, float]

# Sky coordinates on the unit sphere, in cartesian representation (x,y,z)
CartesianCoordinates: TypeAlias = Tuple[float, float, float]


def filter_pixels_by_polygon(
    pixel_tree: PixelTree, vertices: List[CartesianCoordinates]
) -> List[HealpixPixel]:
    """Filter the leaf pixels in a pixel tree to return a list of healpix pixels that
    overlap with a polygonal region.

    Args:
        pixel_tree (PixelTree): The catalog tree to filter pixels from.
        vertices (List[CartesianCoordinates]): The vertices of the polygon to filter points
            with, in lists of (x,y,z) points on the unit sphere.

    Returns:
        List of HealpixPixel, representing only the pixels that overlap
        with the specified polygonal region, and the maximum pixel order.
    """
    max_order = pixel_tree.get_max_depth()
    polygon_tree = _generate_polygon_pixel_tree(vertices, max_order)
    return get_filtered_pixel_list(pixel_tree, polygon_tree)


def _generate_polygon_pixel_tree(vertices: np.array, order: int) -> PixelTree:
    """Generates a pixel_tree filled with leaf nodes at a given order that overlap within
    a polygon. Vertices is an array of 3D coordinates, in cartesian representation (x,y,z)
    and shape (Num vertices, 3), representing the vertices of the polygon."""
    polygon_pixels = hp.query_polygon(hp.order2nside(order), vertices, inclusive=True, nest=True)
    pixel_list = [HealpixPixel(order, polygon_pixel) for polygon_pixel in polygon_pixels]
    return PixelTree.from_healpix(pixel_list)
