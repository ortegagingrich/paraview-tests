""" Create a simple vtk file from a numpy array """
import numpy as np

TESTING = False

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
	xs = np.linspace(0, 20, npts + 1)
	ys = np.linspace(0, 20, npts + 1)
	(xgrid, ygrid) = np.meshgrid(xs, ys)
	zgrid = wavy(xgrid, ygrid)
	
	return (xgrid, ygrid, zgrid)


def __test_main__():
	import matplotlib.pyplot as plt
	
	(xgrid, ygrid, zgrid) = __create_sample_data__(npts = 1000)
	
	#just for testing
	if TESTING:
		plt.contourf(xgrid, ygrid, zgrid)
		plt.show()
	
	#export to file
	export_to_vtk(xgrid, ygrid, zgrid, 'topo')


if __name__ == '__main__':
	__test_main__()
