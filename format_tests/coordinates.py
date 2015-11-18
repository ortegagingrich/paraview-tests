""" Simple utilities for converting from lat/lon/elev to 3D cartesian """
import numpy as np

EARTH_RADIUS = 6.371e6 #in meters


def latlon_to_cart(lon, lat, elev, radius = None, scale_factor = 1.0):
	""" 
	convert lon lat elev to points on sphere in 3D, centered at zero 
	scale_factor sets the average radius of the sphere after data is applied.
	"""
	if radius == None:
		radius = EARTH_RADIUS
	
	#local radius including elevation
	r = scale_factor * (radius + elev)
	
	lonrad = np.deg2rad(lon)
	latrad = np.deg2rad(lat)
	
	xgrid = r * np.cos(lonrad) * np.cos(latrad)
	ygrid = r * np.sin(lonrad) * np.cos(latrad)
	zgrid = r * np.sin(latrad)
	
	return (xgrid, ygrid, zgrid)
