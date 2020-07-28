#USAGE
# python social_distance.py -i [VIDEO PATH] -o [OUTPUT PATH]
# OUTPUT: Social distancing video analysis + Count/Violations & Avg Distance Diagrams

# import the necessary packages
from pyimagesearch import social_distancing_config as config
from pyimagesearch.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import math
import cv2
import os
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from PIL import Image
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
	help="path to (optional) input video file")
ap.add_argument("-o", "--output", type=str, default="social_distancing",
	help="path to (optional) output video file")
ap.add_argument("-d", "--display", type=int, default=1,
	help="whether or not output frame should be displayed")
ap.add_argument("-l", "--label", type=bool, default=True,
	help="whether or not title should be displayed")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# check if we are going to use GPU
if config.USE_GPU:
	# set CUDA as the preferable backend and target
	print("[INFO] setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream and pointer to output video file
print("[INFO] accessing video stream...")
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)
writer = None

df = pd.DataFrame(columns=('count', 'violations')) #To collect data on count and violations
column_names = ['Average distance in pixels']
df2 = pd.DataFrame(columns=column_names) #To collect data on average distance between detections
# loop over the frames from the video stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break

	# resize the frame and then detect people (and only people) in it
	frame = cv2.resize(frame, (950,700), interpolation = cv2.INTER_AREA) #950 x 700 pixels
	height, width = frame.shape[:2]
	results = detect_people(frame, net, ln,
		personIdx=LABELS.index("person")) 
	# initialize the set of indexes that violate the minimum social
	# distance
	violate = set()
	omitted = 0
	distances = []
	#Separate black window for analytical visualisation
	blank_img = np.zeros((height, width, 3), np.uint8)
	#Original Bounding Boxes
	# ensure there are *at least* two people detections (required in
	# order to compute our pairwise distance maps)
	if len(results) >= 2:
		# extract all centroids from the results and compute the
		# Euclidean distances between all pairs of the centroids
		centroids = np.array([r[2] for r in results])
		D = dist.cdist(centroids, centroids, metric="euclidean") 
		widths = np.array([r[1][2]-r[1][0] for r in results])
		avg_width = int(sum(widths)/len(widths)) #Average width of the bounding boxes for the specific frame

		# loop over the upper triangular of the distance matrix
		for i in range(0, D.shape[0]):
			for j in range(i + 1, D.shape[1]):
				# check to see if the distance between any two
				# centroid pairs is less than the configured number
				# of pixels
				if D[i, j] < avg_width*2.5: #2.5 * avg_width is approximately 1m
					# update our violation set with the indexes of
					# the centroid pairs
					violate.add(i)
					violate.add(j)
				distances.append(D[i,j]) #Create distances list for the specific frame

	# loop over the results
	for (i, (prob, bbox, centroid)) in enumerate(results):
		# extract the bounding box and centroid coordinates, then
		# initialize the color of the annotation
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		# if the index pair exists within the violation set, then
		# update the c
		if i in violate:
			color = (0, 0, 255)
		
		if endX-startX > 500: #Fixing the large bounding box problem
			omitted+=1
			continue

		# draw (1) a bounding box around the person and (2) the
		# centroid coordinates of the person,
		cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2) #Raw view
		cv2.circle(frame, (cX, cY), 5, color, 1)
		cv2.circle(blank_img,(cX,cY), int(avg_width*2.5/2), color, 3) #Analytical view
		cv2.circle(blank_img, (cX,cY), 5, color,-1)

	# draw the total number of social distancing violations on the
	# output frame

	#CAN REMOVE THIS TO REMOVE TEXT
	text = "Social Distancing Violations: {}".format(len(violate)-omitted)
	cv2.putText(frame, text, (10, frame.shape[0] - 25),
		cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 2)

	violations = len(list(violate))-omitted #Number of violations
	count = len(results) - omitted #Number of count
	avg_d = sum(distances)/len(distances) #Average distance between detections
	df = df.append({'count': count, 'violations':violations}, ignore_index=True)
	df2=df2.append({'Average distance in pixels':avg_d}, ignore_index=True)
	# check to see if the output frame should be displayed to our
	# screen
	if args["display"] > 0:
		# show the output frame
		both = np.concatenate((frame, blank_img), axis=1)
		cv2.imshow("Comparison", both)
		#cv2.imshow("Transformed", blank_img)
		#cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
	# if an output video file path has been supplied and the video
	# writer has not been initialized, do so now
	if args["output"] != "" and writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"]+ '.avi', fourcc, 25,
			(both.shape[1], both.shape[0]), True)

	# if the video writer is not None, write the frame to the output
	# video file
	if writer is not None:
		writer.write(both)

df['time']=df.index #Add a column time
df['time']=df['time']/(27) #Change column time to seconds
df1 = df[::27] #Fiter every 27 rows
ax = df1.plot(x='time') #Plot columns vs time
ax.set_xlabel("Time in seconds") #Label
fig_name = '{}_summary.png'.format(args['output'])
plt.savefig(fig_name) #Save Count/Violations Diagram

graph_image = Image.open(fig_name)
image_resized = graph_image.resize((950, 700)) #Resizing
image_resized.save(fig_name)

df2['time']=df2.index #Add a column time
df2['time']=df2['time']/(27) #Change column time to seconds
df3 = df2[::27] #Fiter every 27 rows
ax1 = df3.plot(x='time') #Plot columns vs time
ax1.set_xlabel("Time in seconds") #Label
fig2_name = '{}_analysis.png'.format(args['output'])
plt.savefig(fig2_name) #Save Avg_distance Diagram

graph2_image = Image.open(fig2_name)
image2_resized = graph2_image.resize((950, 700)) #Resizing
image2_resized.save(fig2_name)

im1 = cv2.imread(fig_name)
im2 = cv2.imread(fig2_name)
im_h = cv2.hconcat([im1, im2])
cv2.imwrite('{}_summary.png'.format(args['output']), im_h) #Concatenating the two diagrams