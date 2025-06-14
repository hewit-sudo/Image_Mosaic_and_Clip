from matplotlib import pyplot as plt
from osgeo import gdal
from rasterio import plot
import os
import numpy as np

mosaic_op_dir = r'D:\Programming\ImageProcessing\data\mosaic_output'
print(mosaic_op_dir)

mosaic_array = []
for i in range (1, len(os.listdir(mosaic_op_dir))+1):
    os.chdir(mosaic_op_dir)
    opn = gdal.Open(f'mosaiced_band_{i}.tif')
    arr = opn.ReadAsArray()
    mosaic_array.append(arr)


plt.figure(figsize=(10,10))
plt.imshow((np.dstack((mosaic_array[2], mosaic_array[1], mosaic_array[0]))))
plt.axis('off')
plt.title('FCC of Mosaicked Image')
plt.show()