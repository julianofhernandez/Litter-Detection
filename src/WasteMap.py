from detectors.MaskRCNN import MaskRCNN
import geopandas
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import os
from data_sources.Mapillary import Mapillary
from data_sources.ExifData import ExifData
# from detectors.YoloV3 import YOLOv3
import contextily as cx
import glob
from tqdm import tqdm
from shapely.geometry import Point
from exif import Image
import random

class WasteMap:
	def __init__(self, file_path, model_path=None, confidence=0.5):
		self.file_path = file_path
		self.read(file_path)
		# self.data_source = Mapillary()
		self.data_source = ExifData()
		# Zoom to the area around Sac State
		self.mapExtent = (-121.435,-121.415, 38.55, 38.57)
		self.colorMap = {	
			'Other':'#ff0000', # red
			'Can':'#ff8c00', # orange
			'Cup':'#fff100', # yellow 
			'Bottle':'#ec008c', # magenta
			'Lid':'#68217a', # purple
			'Straw':'#00188f', # blue
			'Pop tab':'#00bcf2', # cyan
			'Cigarette':'#00b294', # teal
			'Plastic bag + wrapper':'#009e49', # green
			'Bottle cap':'#bad80a'} # lime
		matplotlib.use('Qt5Agg')
		if model_path is None:
			self.detector = None
		else:
			self.detector = MaskRCNN(model_path, confidence=confidence)

	def print_map(self):
		'''print map from the loaded geoJSON file'''
		randomWiggle = 0.0001
		fig, ax = plt.subplots(1,1, figsize=(12,12))
		ax.set_title('Waste around Sac State')
		# Iterate through images
		for i, row in self.dataframe.iterrows():
			# iterate through each object in an image
			for trashItem in row.waste:
				rand_x = random.uniform(-1*randomWiggle, randomWiggle)
				rand_y = random.uniform(-1*randomWiggle, randomWiggle)
				size = row.waste[trashItem]*30
				ax.scatter(self.dataframe.loc[i].geometry.x+rand_x, self.dataframe.loc[i].geometry.y+rand_y, 
					s=size,
					color=self.colorMap[trashItem])
		ax.axis(self.mapExtent)
		cx.add_basemap(ax, crs=self.dataframe.crs.to_string(), source=cx.providers.Esri.WorldGrayCanvas)
		ax.legend(loc = "upper right", handles=self.createLegend())
		plt.show()

	def add_image(self, image_path):
		image_id = os.path.splitext(os.path.basename(image_path))[0]
		if not os.path.isfile(image_path):
			print("Not a valid image path")
			return
		# try:
		# coordinates = self.data_source.get_coordinates(image_id)
		coordinates = self.data_source.get_coordinates(image_path)
		exif_data = self.get_all_exif(image_path)
		# coordinates = self.get_coordinates(image_path)
		if (coordinates is not None):
			new_row = [{
				'image_path': image_path,
				'waste': self.detector.detect(image_path, image_path + '_processed.png'),
				# 'waste': self.detector.detect(image_path),
				'geometry': Point(coordinates),
				# 'exif': exif_data
			}]
			self.dataframe = self.dataframe.append(geopandas.GeoDataFrame(new_row), ignore_index=True)
		# except Exception as e:
		# 	print("Error:" + str(e))

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

	# def get_coordinates(self, imagePath):
	# 	img_path = imagePath
	# 	with open(img_path, 'rb') as src:
	# 		img = Image(src)
	# 		if img.has_exif:
	# 			lon = self.decimal_coords(img.gps_longitude, img.gps_longitude_ref)
	# 			lat = self.decimal_coords(img.gps_latitude, img.gps_latitude_ref)
	# 			return (lon,lat)
	# 		else:
	# 			print(imagePath + " doesn't contain coordinate data")
	# 			return None

	# def decimal_coords(self, coords, ref):
	# 	decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
	# 	if ref == "S" or ref == "W":
	# 		decimal_degrees = -decimal_degrees
	# 	return decimal_degrees

	# def metersToDegrees(meters):
	# 	return meters/1582

	def createLegend(self):
		legend_elements = []
		for color in self.colorMap:
			legend_elements.append(Line2D([0], [0], color=self.colorMap[color], label=color, markersize=15))
		return legend_elements

	def get_all_exif(self, image_path):
		with open(image_path, 'rb') as src:
			img = Image(src)
			exif_dict = {}
			if not img.has_exif:
				return None
			else:
				for exif_category in img.list_all():
					try:
						exif_dict[str(exif_category)] = img[str(exif_category)]
					except:
						pass
			return exif_dict