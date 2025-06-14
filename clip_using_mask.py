import rasterio
from rasterio import mask
import fiona
from osgeo import gdal
import os
import numpy  as np
from matplotlib import pyplot as plt
import geopandas as gpd
gdal.UseExceptions()

folder_name = 'shape_file' #paste your shape file folder name
vector_directory = os.path.join(os.path.dirname(__file__),'data','inputs','aoi_shape_file',f'{folder_name}')
vector_file_directory = []
mosaicked_imgs_dir = os.path.join(os.path.dirname(__file__), 'data','mosaic_output')
mosaicked_imgs_dir_files = []
clipped_output_dir = os.path.join(os.path.dirname(__file__),'data','clipped_output')

for i in os.listdir(vector_directory):
    if i.endswith('.shp'):
        vector_file_directory.append(os.path.join(vector_directory, f'{i}'))
print('Vector file directory is: ',vector_file_directory[0])

for j in os.listdir(mosaicked_imgs_dir):
    if j.endswith('.tif'):
        mosaicked_imgs_dir_files.append(j)
print('Mosaiced Image files are: ', mosaicked_imgs_dir_files)


with fiona.open(vector_file_directory[0], "r") as shapefile:
    shapes = [feature["geometry"] for feature in shapefile]

opened_raster_image = []

for i in range(0, len(mosaicked_imgs_dir_files)):
    with rasterio.open(os.path.join(mosaicked_imgs_dir, f'{mosaicked_imgs_dir_files[i]}'), 'r') as src:
        out_image, out_transform = rasterio.mask.mask(src, shapes, crop=True)
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})

    with rasterio.open(os.path.join(clipped_output_dir,f"masked_band_{i+1}.tif"), "w", **out_meta) as dest:
        dest.write(out_image)

clipped_array = []
for i in range (1, len(os.listdir(clipped_output_dir))+1):
    os.chdir(clipped_output_dir)
    opn = gdal.Open(f'masked_band_{i}.tif')
    arr = opn.ReadAsArray()
    clipped_array.append(arr)


gpd.read_file(vector_file_directory[0]).plot()
plt.axis('off')
plt.title('Vector File')
plt.show()

plt.figure(figsize=(8,8))
plt.imshow((np.dstack((clipped_array[2], clipped_array[1], clipped_array[0]))))
plt.axis('off')
plt.title('FCC of Masked Image')
plt.show()