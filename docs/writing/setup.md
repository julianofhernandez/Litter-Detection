## Packages
Use python 3.7.9
pip install requirements.txt
install GDAL, rasterio, and Fiona packages from https://www.lfd.uci.edu/~gohlke/pythonlibs/
rasterio-1.2.10-cp37-cp37m-win_amd64.whl
GDAL-3.3.3-cp37-cp37m-win_amd64.whl
Fiona-1.8.20-cp37-cp37m-win_amd64.whl

Install tensorflow 1.15
https://www.tensorflow.org/install/pip#windows

Install Mask-RCNN following the instructions at https://github.com/matterport/Mask_RCNN


## Notes
src/menu.py is the entry point
    1. Create map of all processed images stored in the geojson file
    2. prints out geopandas dataframe (debug only)
    3. Will run computer vision on all images in src/images and add them to the geoJSON file
    4. Exits and saved geoJSON file
    5. Downloads images from Mapillary in a set area to src/images
