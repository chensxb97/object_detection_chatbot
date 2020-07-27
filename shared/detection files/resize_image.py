from PIL import Image
import argparse
import os 
import glob
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to image")
args = vars(ap.parse_args())

filename = args['image']

if os.path.isfile(filename):
	image = Image.open(filename)
	new_image = image.resize((950, 700))
	new_image.save(args['image'])
else:
	for file in glob.iglob(filename+ '\*'):
		if file.endswith('jpg') or file.endswith('png'):
			image = Image.open(file)
			new_image = image.resize((950, 700))
			new_image.save(file)