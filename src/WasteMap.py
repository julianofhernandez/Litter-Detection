from math import e
import geopandas
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point
import os
import json
from data_sources.Mapillary import Mapillary
from detectors.YOLOv3 import YOLOv3
# from detectors.MaskRCNN import MaskRCNN
import contextily as cx
import requests
from data_sources.Mapillary import Mapillary
import glob
from tqdm import tqdm

class WasteMap:
	def __init__(self, file_path):
		self.file_path = file_path
		self.read(file_path)
		self.detector = YOLOv3()
		self.mapillary = Mapillary()

	def print_map(self):
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
			coordinates = self.mapillary.get_coordinates(image_id)
			new_row = [{
				'image_path': image_path,
				'waste': self.detector.detect(image_path),
				'geometry': Point(coordinates)
			}]
			self.dataframe = self.dataframe.append(geopandas.GeoDataFrame(new_row), ignore_index=True)
		except Exception as e:
			print(e)

	def add_images(self,images_path):
		images = glob.glob(os.path.join(images_path, '*.*'), recursive=True)
		print(f'Processing {len(images)} images')
		for i in tqdm(range(len(images))):
			self.add_image(images[i])

	def get_coordinates(self, image_path):
		id = os.path.splitext(os.path.basename(image_path))[0]
		responce = requests.get('https://graph.mapillary.com/2265641036902438?access_token=MLY|3461141010677895|c26e4e4b32b90d5cb1db934c54ebe2c8&fields=id,computed_geometry,thumb_1024_url')
		responce_json = json.loads(responce.content.decode('utf-8'))
		coordinates = responce_json['computed_geometry']['coordinates']
		#TODO: need to be converted to epsg3857 before returning
		# lon = random.randrange(-121,-130,-1)
		# lat = random.randrange(30,40)
		return coordinates

	def read(self, file_path=None):
		if file_path:
			self.dataframe = geopandas.read_file(file_path)
		else:
			self.dataframe = geopandas.read_file(self.file_path)

	def write(self):
		self.dataframe.to_file(self.file_path, driver="GeoJSON")
