train: train_trash.py
	# TODO: Replace with command to train model on trash
	python $< arg1

simpletest: 
	python .\trash_detection.py detect --image .\datasets\gsv.png -m something

download:
	python37 .\menu.py download

map:
	python37 .\menu.py map -g save_files/random.geojson

detect:
	python37 .\menu.py detect -i images/ -m models/yolov3_30000 -g save_files/random.geojson