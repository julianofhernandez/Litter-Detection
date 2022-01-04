import os
import argparse

from WasteMap import WasteMap
from data_sources.Mapillary import Mapillary

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')
	detect = subparser.add_parser('detect')

	detect.add_argument('-i', '--image', type=str, required=True, help='The path to the image you want to process')
	detect.add_argument('-m', '--model', type=str, help='Which bject detection model to use')
	args = parser.parse_args()

	option = ''
	
	# uncomment to skip setup
	map = WasteMap("save_files/random.geojson")
	mapillary = Mapillary()
	# print("Welcome to the cmd application")
	# option = input('Enter a path to a geojson file: ')
	# while (not os.path.isfile(option)):
	# 	print('Not a file')
	# 	option = input('Enter a path to a geojson file: ')
	# map = WasteMap(option)

	while(quit!=True):
		print("""
Options:
1: Print map
2: Print dataframe (debug)
3: Add images to geoJSON
4: Quit
5: Download images""")
		try:
			option = int(input('Enter your choice: '))
		except:
			print('Wrong input. Please enter a number ...')
		if option == 1:
			map.print_map()
		elif option == 2:
			print(map.dataframe)
		elif option == 3:
			map.add_images(input("Enter an image path to process:\n"))
		elif option == 4:
			map.write()
			quit = True
		elif option == 5:
			mapillary.download_images_in_bbox(13,55.599,13.001,55.600)
		else:
			print('Invalid option. Please enter a number between 1 and 4.')

		

	# if (args.command == 'detect'):
	# 	detector = YoloPretrainedOnCoco()
	# 	detector.image_detect(args.image)
