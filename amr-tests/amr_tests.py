""" 
Some tests for creating fake amr data to import into paraview.
"""
import numpy


class AMRGrid(object):
	""" Class of amr objects (just for my tests) """
	
	def __init__(self):
		pass
	
	
	def create_polygrid(self):
		""" 
		Creates a polygrid mesh object (eventually to be turned into a VTK source
		object and passed to paraview).  Alternatively, we might just try writing
		it to a VTK file format to be read into paraview via the import functions.
		
		TBD:
			Do we want to do filtering at this stage to avoid huge files?
		
		"""
		pass

class SingleGrid(object):
	""" Class of rectilinear grid objects """
	def __init__(self, x_lower, x_upper, y_lower, y_upper, dx, dy,
	             data_function = None):
		self.x_lower = x_lower
		self.x_upper = x_upper
		self.y_lower = y_lower
		self.y_upper = y_upper
		self.nx = round((x_upper - x_lower)/dx) + 1
		self.ny = round((y_upper - y_lower)/dy) + 1
		self.data = None
		
		if data_function == None:
			self.data = numpy.zeros([self.nx + 1, self.ny + 1])
		else:
			self.fill_data(data_function)
				
		
	
	
	def fill_data(self, data_function):
		""" Fills in the grid by evaluating data_function at every point """
		(xgrid, ygrid,_) = self.get_grid()
		self.data = data_function(xgrid, ygrid)
	
	
	def get_grid(self):
		""" Return a tuple containing meshgrid expansions of the grid """
		xvec = numpy.linspace(self.x_lower, self.x_upper, self.nx + 1)
		yvec = numpy.linspace(self.y_lower, self.y_upper, self.ny + 1)
		
		(xgrid, ygrid) = numpy.meshgrid(xvec, yvec)
		
		return (xgrid, ygrid, self.data)


def surface_test(xgrid, ygrid):
	""" 
	Returns the test surface evaluated at the points specified in the input
	structured grids
	"""
	xfactor = 2*numpy.pi/20
	yfactor = 2*numpy.pi/11
	return numpy.sin(xgrid*xfactor) * numpy.cos(ygrid*yfactor)


def make_grid(surface, x_range, y_range, dx, dy):
	""" Make the level one grid for this particular test """
	x_lower = x_range[0]
	x_upper = x_range[1]
	y_lower = y_range[0]
	y_upper = y_range[1]
	
	n_x = round((x_upper - x_lower)/dx) + 1
	n_y = round((y_upper - y_lower)/dy) + 1
	
	xvec = numpy.linspace(x_lower, x_upper, n_x + 1)
	yvec = numpy.linspace(y_lower, y_upper, n_y + 1)
	
	(xgrid, ygrid) = numpy.meshgrid(xvec, yvec)
	
	hgrid = surface(xgrid, ygrid)
	
	return (xgrid, ygrid, hgrid)





def __test__():
	import matplotlib.pyplot as plt
	
	#surface function for test
	def f(xgrid, ygrid):
		""" test surface elevation """
		xfactor = 2*numpy.pi/20
		yfactor = 2*numpy.pi/11
		return numpy.sin(xgrid*xfactor) * numpy.cos(ygrid*yfactor)
	
	#first make larger grid
	(xgrid_1, ygrid_1, hgrid_1) = make_grid(f, [-10, 10], [-10, 10], 0.5, 0.5)
	#make refined grid
	(xgrid_2, ygrid_2, hgrid_2) = make_grid(f, [-5, 5], [-5, 5], 0.25, 0.25)
	#make finest grid
	(xgrid_3, ygrid_3, hgrid_3) = make_grid(f, [-2, 2], [-1, 3], 0.125, 0.125)
	
	plt.figure(1)
	plt.pcolor(xgrid_1, ygrid_1, hgrid_1)
	
	plt.figure(1)
	plt.contourf(xgrid_2, ygrid_2, hgrid_2)
	
	plt.figure(1)
	plt.pcolor(xgrid_3, ygrid_3, hgrid_3)
	
	plt.show()


def __test2__():
	import matplotlib.pyplot as plt
	
	#surface function for test
	def f(xgrid, ygrid):
		""" test surface elevation """
		xfactor = 2*numpy.pi/20
		yfactor = 2*numpy.pi/11
		return numpy.sin(xgrid*xfactor) * numpy.cos(ygrid*yfactor)
	
	#make a single grid
	grid1 = SingleGrid(-10, 10, -10, 10, 0.5, 0.5, data_function = f)
	
	#plot tests
	(xgrid1, ygrid1, hgrid1) = grid1.get_grid()
	
	print xgrid1
	
	plt.figure(1)
	plt.pcolor(xgrid1, ygrid1, hgrid1)
	plt.show()


if __name__ == '__main__':
	__test2__()

