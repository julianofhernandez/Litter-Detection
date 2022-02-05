from math import e
import geopandas
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
import os
import json
from data_sources.Mapillary import Mapillary
from detectors.YoloV3 import YOLOv3
# from detectors.MaskRCNN import MaskRCNN
import contextily as cx
import requests
from data_sources.Mapillary import Mapillary
import glob
from tqdm import tqdm

class WasteMap:
	def __init__(self, file_path, model_path=None, confidence=0.7):
		self.file_path = file_path
		self.read(file_path)
		self.data_source = Mapillary()
		if model_path is None:
			self.detector = None
		else:
			self.detector = YOLOv3(model_path, confidence=confidence)

	def print_map(self):
		'''print map from the loaded geoJSON file'''
		ax = self.dataframe.plot(markersize=10, color="red", figsize=(9, 9))
		cx.add_basemap(ax, crs=self.dataframe.crs.to_string(), source=cx.providers.CartoDB.Voyager)
		# fig = matplotlib.pyplot.gcf()
		# fig.set_size_inches(15, 8, forward=True)
		plt.show()

	def interactive_map(self):
		#not currently working
		self.dataframe.explore()

	def add_image(self, image_path):
		image_id = os.path.splitext(os.path.basename(image_path))[0]
		if not os.path.isfile(image_path):
			print("Not a valid image path")
			return
		try:
			coordinates = self.data_source.get_coordinates(image_id)
			new_row = [{
				'image_path': image_path,
				'waste': self.detector.detect(image_path, image_path + '_processed.png'),
				'geometry': Point(coordinates)
			}]
			self.dataframe = self.dataframe.append(geopandas.GeoDataFrame(new_row), ignore_index=True)
		except Exception as e:
			print("error:" + str(e))

	def add_images(self,images_path):
		images = glob.glob(os.path.join(images_path, '*.*'), recursive=True)
		print(f'Processing {len(images)} images')
		for i in tqdm(range(len(images))):
			self.add_image(images[i])

	def read(self, file_path=None):
		'''Opens geoJSOn save file'''
		if file_path:
			self.dataframe = geopandas.read_file(file_path)
		else:
			self.dataframe = geopandas.read_file(self.file_path)

	def write(self):
		'''Write geodataframe to geoJSON save file'''
		self.dataframe.to_file(self.file_path, driver="GeoJSON")
