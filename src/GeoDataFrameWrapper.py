import geopandas
import matplotlib.pyplot as plt
import random

class GeoDataFrameWrapper:
	def __init__(self, file_path):
		self.file_path = file_path
		self.__read(file_path)
		self.detector = "add detector"

	def print_map(self):
		self.dataframe.plot()
		plt.show()
	
	def interactive_map(self):
		self.dataframe.explore()

	def add_image(self, image_path):
		self.detector.detect(image_path)
		lat = random.randrange(-121.4916229248047,-121.4916229248147)
		lon = random.randrange(38.58091586687018,38.58091586688000)
		df.loc[len(df)]=[]


	def __read(self, file_path=None):
		if file_path:
			self.dataframe = geopandas.read_file(file_path)
		else:
			self.dataframe = geopandas.read_file(self.file_path)

	def __write(self):
		self.dataframe.to_file(self.file_path, driver="GeoJSON")
