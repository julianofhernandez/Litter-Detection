from tqdm import tqdm
import os
from exif import Image

class ExifData:
	def get_coordinates(self, imagePath):
		img_path = imagePath
		with open(img_path, 'rb') as src:
			img = Image(src)
			if img.has_exif:
				try:
					lon = self.decimal_coords(img.gps_longitude, img.gps_longitude_ref)
					lat = self.decimal_coords(img.gps_latitude, img.gps_latitude_ref)
					return (lon,lat)
				except:
					print(imagePath + " doesn't contain coordinate data")
					return None
			else:
				print(imagePath + " doesn't contain coordinate data")
				return None

	def decimal_coords(self, coords, ref):
		decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
		if ref == "S" or ref == "W":
			decimal_degrees = -decimal_degrees
		return decimal_degrees

	def metersToDegrees(meters):
		return meters/1582