""" Create a simple vtk file from a numpy array """
import numpy as np

TESTING = False

def export_to_vtk(xgrid, ygrid, zgrid, data_name, data = None):
	""" Export the specified 2D structured grid to file """
	from evtk.vtk import VtkFile, VtkStructuredGrid
	
	if data == None:
		data = np.array(zgrid)
	
	#reshape 2D data into (flat) 3D array
	oldshape = data.shape
	newshape = oldshape + (1,)
	data = data.reshape(newshape)
	xgrid = xgrid.reshape(newshape)
	ygrid = ygrid.reshape(newshape)
	zgrid = zgrid.reshape(newshape)
	
	
	path = './{}'.format(data_name)
	w = VtkFile(path, VtkStructuredGrid)
	
	#Header stuff?
	nx, ny = oldshape[0] - 1, oldshape[1] - 1
	w.openGrid(start = (0, 0, 0), end = (nx, ny, 0))
	w.openPiece(start = (0, 0, 0), end = (nx, ny, 0))
	
	w.openElement("Points")
	w.addData("points", (xgrid, ygrid, zgrid))
	w.closeElement("Points")
	
	w.openData("Point", scalars = data_name)
	w.addData(data_name, data)
	w.closeData("Point")
	
	w.closePiece()
	w.closeGrid()
	
	#Now add the actual data?
	w.appendData((xgrid, ygrid, zgrid))
	w.appendData(data)
	
	#finished
	w.save()


def __create_sample_data__(npts = 20):
	""" Create some numpy sample data to send to paraview """
	#data function
	def wavy(x, y):
		return np.sin(0.2*np.pi*x)*np.cos(0.4*np.pi*y)
	
	#make grid
	xs = np.linspace(0, 2*20, 2*npts + 1)
	ys = np.linspace(0, 20, npts + 1)
	(xgrid, ygrid) = np.meshgrid(xs, ys)
	zgrid = wavy(xgrid, ygrid)
	
	return (xgrid, ygrid, zgrid)


def __load_topography__(filepath):
	""" Load in topography to numpy arrays (to send to paraview as vtk) """
	from clawpack.geoclaw import topotools
	topo = topotools.Topography(filepath)
	
	if TESTING:
		import matplotlib.pyplot as plt
		topo.plot()
		plt.show()
	topo.topo_type = 3
	xgrid = topo.X
	ygrid = topo.Y
	zgrid = topo.Z
	
	return (xgrid, ygrid, zgrid)


def __load_topography_sphere__(filepath):
	""" Load in topography, but convert to cartesian coordinates first """
	from coordinates import latlon_to_cart
	
	(lon, lat, elev) = __load_topography__(filepath)
	(xgrid, ygrid, zgrid) = latlon_to_cart(lon, lat, elev)
	
	return (xgrid, ygrid, zgrid, elev)


def __test_main__():
	import matplotlib.pyplot as plt
	import os
	
	topo_dir = os.environ['TOPO']
	topo_file = os.path.join(topo_dir, 'chile_topo.tt3')
	
	(xgrid, ygrid, zgrid) = __load_topography__(topo_file)
	#temp; find a better solution (e.g. convert from lat/lon to actual space)
	zgrid = 1e-4 * zgrid
	
	#(xgrid, ygrid, zgrid, elev) = __load_topography_sphere__(topo_file)
	
	#(xgrid, ygrid, zgrid) = __create_sample_data__(npts = 1000)
	
	#just for testing
	if TESTING:
		print xgrid
		print ygrid
		print zgrid.shape
		plt.contourf(xgrid, ygrid, zgrid)
		plt.show()
	
	#export to file
	export_to_vtk(xgrid, ygrid, zgrid, 'topo_chile')
	#export_to_vtk(xgrid, ygrid, zgrid, 'topo_sphere', 1.e3*elev)


if __name__ == '__main__':
	__test_main__()
