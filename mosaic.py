#import main
from osgeo import gdal
from file_handler import image_arrays
from file_handler import images_directories
import os

mosaic_directory = os.path.join(os.path.dirname(__file__),'data','mosaic_output')

if not os.path.exists(mosaic_directory):
    os.mkdir('mosaic_output')

os.chdir(mosaic_directory)
for i in range (1, len(image_arrays)+1):
     os.chdir(images_directories[i-1])
     mosaic_band_1 = gdal.Warp(os.path.join(mosaic_directory,'mosaiced_band_{}.tif'.format(i)), list(os.listdir(images_directories[i-1])), format='GTiff', resampleAlg = 'bilinear')
     

#os.listdir
