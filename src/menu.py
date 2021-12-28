import os
import argparse

from GeoDataFrameWrapper import GeoDataFrameWrapper

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')
	detect = subparser.add_parser('detect')

	detect.add_argument('-i', '--image', type=str, required=True, help='The path to the image you want to process')
	detect.add_argument('-m', '--model', type=str, help='Which bject detection model to use')
	args = parser.parse_args()

	while(quit!=True):
		print("Welcome to the gui application")

		option = ''
		
		while not os.path.isfile(option):
			option = input('Enter a path to a geojson file: ')
			print('Not a file')
		dataframe = GeoDataFrameWrapper(option)



		print("""
Options:
1: Print map
2: Interactive mode
3: Quit""")
		try:
			option = int(input('Enter your choice: '))
		except:
			print('Wrong input. Please enter a number ...')
		if option == 1:
			dataframe.print_map()
		elif option == 2:
			dataframe.interactive_map()
		elif option == 3:
			quit = True
		else:
			print('Invalid option. Please enter a number between 1 and 4.')

		

	# if (args.command == 'detect'):
	# 	detector = YoloPretrainedOnCoco()
	# 	detector.image_detect(args.image)
