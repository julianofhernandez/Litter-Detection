import os
import argparse

from numpy import mask_indices

from WasteMap import WasteMap
# from detectors.YoloV3 import YOLOv3
from detectors.MaskRCNN import MaskRCNN
from data_sources.Mapillary import Mapillary


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')

	detect = subparser.add_parser('detect')
	# Required
	detect.add_argument('-i', '--images', dest='images', type=str, required=True, 
						help='The path to the image directory that you want to process images from')
	detect.add_argument('-m', '--model_dir', dest='model_dir', type=str, 
						help='Points to a model directory (they all require their own files)')
	detect.add_argument('-g', '--geojson', type=str, 
						help='Results are saved in a geoJSON file')
	# Optional
	detect.add_argument('-v', '--verbose', type=bool, required=False, default=True,
						help='Will save processed images to verbose and print debug information')
	detect.add_argument('-c', '--confidence', type=float, default=0.7, 
						help='Confidence of detections to count as true')

	# Used for debugging and checking models against a single image
	check = subparser.add_parser('check')
	check.add_argument('-i', '--image', dest='image', type=str, required=True, 
						help='The image to check')
	check.add_argument('-m', '--model_dir', dest='model_dir', type=str, 
						help='Points to a model directory (they all require their own files)')
	check.add_argument('-c', '--confidence', type=float, default=0.7, 
						help='Confidence of detections to count as true')

	map = subparser.add_parser('map')
	map.add_argument('-g', '--geojson', type=str, help='Path to a geojson file for saving results')

	download = subparser.add_parser('download')
	#!Needs to choose a location
	download.add_argument('-d', '--download', type=str, help='mapillary|google_street_view')

	args = parser.parse_args()

	if args.command == 'detect':
		map = WasteMap(args.geojson, args.model_dir)
		map.add_images(args.images)
		map.write()
	
	if args.command == 'check':
		# detector = YOLOv3(args.model_dir, confidence=args.confidence)
		detector = MaskRCNN(args.model_dir, confidence=args.confidence)
		detector.detect(args.image, args.image + '_processed.jpg')

	if args.command == 'map':
		map = WasteMap(args.geojson)
		map.print_map()

	if args.command == 'download':
		data_source = Mapillary()
		# data_source.download_images_in_bbox(13,55.599,13.001,55.600)
		data_source.download_images_in_bbox(-121.435,38.55,-121.415, 38.57)