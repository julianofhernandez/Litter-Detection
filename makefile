train: train_trash.py
	# TODO: Replace with command to train model on trash
	python $< arg1

simpletest: 
	python .\trash_detection.py detect --image .\datasets\gsv.png -m something
