import os
from osgeo import gdal
from matplotlib import pyplot as plt
#import mosaic
gdal.UseExceptions() 

dir = os.path.join(os.path.dirname(__file__),'data','inputs','satellite_images')
folders_and_files = os.listdir(dir)

images_directories = [] # to store the all folder's directories alone, each folder has images
image_arrays = {} #to store the raster as array of the images in all folders
gdal_opened = {} # to store all the gdal opened files
inside_folders_len = []


for i in range(0, len(folders_and_files)):
    dir_1 = os.path.join(dir, str(folders_and_files[i]))
    if os.path.isfile(dir_1) == False: # to check whether it is file or folder, and omit the files
        images_directories.append(dir_1)


for j in range(0, len(images_directories)): #to print the all files inside the folder
    #print(f'These are the files inside the folder : {inside_folders[j]}','\n',os.listdir(inside_folders[j]))
    inside_folders_len.append(len(os.listdir(images_directories[j])))
    

count = 0
for k in images_directories: # to open and read the bands as array
    os.chdir(k)
    count += 1

    gdal_opened_file = []
    opened_array = []
    for directory in os.listdir(k):
        if directory.endswith('.tif'):
            gdal_open = gdal.Open(directory)
            gdal_opened_file.append(gdal_open)
            array = gdal_open.ReadAsArray()
            opened_array.append(array)

    image_arrays[count] = opened_array
    gdal_opened[count] = gdal_opened_file


print('All images have read successfully')