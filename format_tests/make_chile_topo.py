""" imports chile topography into the TOPO directory (for testing) """
import os

from clawpack.geoclaw import topotools
from clawpack.clawutil import data

TOPO_DIR = os.environ['TOPO']

def make_chile_topo():
	""" If the file is not already downloaded, download it. """
	topo_fname = 'etopo10min120W60W60S0S.asc'
	url = 'http://www.geoclaw.org/topo/etopo/' + topo_fname
	data.get_remote_file(url, output_dir = TOPO_DIR, file_name = topo_fname)
	
	inpath = os.path.join(TOPO_DIR, topo_fname)
	outname = 'chile_topo.tt3'
	outpath = os.path.join(TOPO_DIR, outname)
	
	topo = topotools.Topography(inpath, topo_type = 2)
	print topo.X
	print topo.Y
	print topo.Z
	topo.write(outpath, topo_type = 3)

if __name__ == '__main__':
	make_chile_topo()
	
