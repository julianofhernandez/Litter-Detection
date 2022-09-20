## Python
Download and install [Python 3.7.9](https://www.python.org/downloads/release/python-379/)

## Packages
pip install requirements.txt
install GDAL, rasterio, and Fiona packages from https://www.lfd.uci.edu/~gohlke/pythonlibs/
or using these links using ```python37 -m pip install <wheel_file_path>```

[rasterio-1.2.10-cp37-cp37m-win_amd64.whl](https://download.lfd.uci.edu/pythonlibs/archived/cp37/rasterio-1.2.10-cp37-cp37m-win_amd64.whl)

[GDAL-3.3.3-cp37-cp37m-win_amd64.whl](https://download.lfd.uci.edu/pythonlibs/archived/cp37/GDAL-3.3.3-cp37-cp37m-win_amd64.whl)

[Fiona-1.8.20-cp37-cp37m-win_amd64.whl](https://download.lfd.uci.edu/pythonlibs/archived/cp37/Fiona-1.8.21-cp37-cp37m-win_amd64.whl)


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

## Models
/src/models should hold these three files for yolov3 to work, which can be downloaded from https://pjreddie.com/darknet/yolo/
models/yolov3-pretrained-coco.weights
models/yolov3-pretrained-coco.cfg
models/coco-labels.txt
## Mask RCNN Setup
You must install
https://docs.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170
