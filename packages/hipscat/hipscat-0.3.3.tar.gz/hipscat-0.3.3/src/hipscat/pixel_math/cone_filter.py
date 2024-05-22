from typing import List

import healpy as hp
import numpy as np

from hipscat.pixel_math import HealpixPixel
from hipscat.pixel_math.filter import get_filtered_pixel_list
from hipscat.pixel_tree.pixel_tree import PixelTree


def filter_pixels_by_cone(
    pixel_tree: PixelTree, ra: float, dec: float, radius_arcsec: float
) -> List[HealpixPixel]:
    """Filter the leaf pixels in a pixel tree to return a partition_info dataframe with the pixels
    that overlap with a cone.

    Args:
        ra (float): Right Ascension of the center of the cone in degrees
        dec (float): Declination of the center of the cone in degrees
        radius_arcsec (float): Radius of the cone in arcseconds

    Returns:
        List of HealpixPixels representing only the pixels that overlap with the specified cone.
    """
    max_order = pixel_tree.get_max_depth()
    cone_tree = _generate_cone_pixel_tree(ra, dec, radius_arcsec, max_order)
    return get_filtered_pixel_list(pixel_tree, cone_tree)


def _generate_cone_pixel_tree(ra: float, dec: float, radius_arcsec: float, order: int):
    """Generates a pixel_tree filled with leaf nodes at a given order that overlap with a cone"""
    n_side = hp.order2nside(order)
    center_vec = hp.ang2vec(ra, dec, lonlat=True)
    radius_radians = np.radians(radius_arcsec / 3600.0)
    cone_pixels = hp.query_disc(n_side, center_vec, radius_radians, inclusive=True, nest=True)
    pixel_list = [HealpixPixel(order, cone_pixel) for cone_pixel in cone_pixels]
    return PixelTree.from_healpix(pixel_list)
