""" Create a simple vtk file from a numpy array """
import numpy as np

TESTING = True

def export_to_vtk(xgrid, ygrid, data, data_name):
	""" Export the specified 2D structured grid to file """
	from evtk.vtk import VtkFile, VtkStructuredGrid
	
	
	#stupid reshape data
	oldshape = data.shape
	newshape = oldshape + (1,)
	data = data.reshape(newshape)
	xgrid = xgrid.reshape(newshape)
	ygrid = ygrid.reshape(newshape)
	
	
	path = './{}'.format(data_name)
	w = VtkFile(path, VtkStructuredGrid)
	
	#Header stuff?
	nx, ny = oldshape[0] - 1, oldshape[1] - 1
	w.openGrid(start = (0, 0, 0), end = (nx, ny, 0))
	w.openPiece(start = (0, 0, 0), end = (nx, ny, 0))
	
	w.openElement("Points")
	w.addData("points", (xgrid, ygrid, data))
	w.closeElement("Points")
	
	w.openData("Point", scalars = data_name)
	w.addData(data_name, data)
	w.closeData("Point")
	
	w.closePiece()
	w.closeGrid()
	
	#Now add the actual data?
	w.appendData((xgrid, ygrid, data))
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
	
	#temp; find a better solution (e.g. convert from lat/lon to actual space)
	#xgrid = 1.e4 * xgrid
	#ygrid = 1.e4 * ygrid
	
	#test only
	shape = zgrid.shape
	ny, nx = shape[0], shape[1]
	#for iy in range(0,ny):
		#zgrid[iy, 0] = zgrid[iy,0]+1e4
	#for ix in range(0,nx):
		#zgrid[1, ix] = zgrid[1,ix]-1e4
	
	def wavy(x, y):
		return np.sin(0.2*np.pi*x)*np.cos(0.4*np.pi*y)
	
	wavyz = wavy(xgrid, ygrid)
	
	
	for ix in range(0,250):
		for iy in range(0,400):
			zgrid[iy, ix] = 1e4*wavyz[iy, ix]
	
	zgrid = 1e-4 * zgrid
	
	return (xgrid, ygrid, zgrid)
		
	


def __test_main__():
	import matplotlib.pyplot as plt
	import os
	
	topo_dir = os.environ['TOPO']
	topo_file = os.path.join(topo_dir, 'etopo1-131122039053.tt3')
	(xgrid, ygrid, zgrid) = __load_topography__(topo_file)
	
	
	#(xgrid, ygrid, zgrid) = __create_sample_data__(npts = 1000)
	
	#just for testing
	if TESTING:
		print xgrid
		print ygrid
		print zgrid.shape
		plt.contourf(xgrid, ygrid, zgrid)
		plt.show()
	
	#export to file
	export_to_vtk(xgrid, ygrid, zgrid, 'topo_grays')


if __name__ == '__main__':
	__test_main__()
