#USAGE 
# python yolo_vehicle.py -i [IMAGE PATH]
#OUTPUT: Detected Image + Cluster diagram

# import the necessary packages
import numpy as np
import argparse
import time
import cv2
import os
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from sklearn.cluster import KMeans

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-y", "--yolo", type=str, default='yolo-coco',
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applying non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
LABELS = open(labelsPath).read().strip().split("\n")

# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")

# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

# load our YOLO object detector trained on COCO dataset (80 classes)
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
image = cv2.imread(args["image"])
image = cv2.resize(image,(950,700), interpolation = cv2.INTER_AREA) #Resizing all images to 950x700 pixels
image_1 = image.copy()
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

# show timing information on YOLO
print("[INFO] YOLO took {:.6f} seconds".format(end - start))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]
		if classID not in [2,3,4,5,6,7]: #Restricting to vehicle classes only
			continue

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence > args["confidence"]:
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))

			if width > 500: #
				continue

			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],args["threshold"])

#create an empty list of x,y centroid coordinates
cpoints = []

# ensure at least one detection exists
if len(idxs) > 0:
	# loop over the indexes we are keeping
	for i in idxs.flatten():
		# extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		# draw a bounding box rectangle and label on the image
		color = [int(c) for c in COLORS[classIDs[i]]]
		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		
		#cv2.circle(image, (cx,cy), 4, (0,0,255), -1)#Radius 4, red, solid fill for circles
		#Unhash to activate centroids in the object detected
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)

		cx = int((x+w+x)/2)
		cy = int((y+y+h)/2)2
		point = [cx,cy]
		cpoints.append(point) #Collating all detected centroids in the image

while True:
	cv2.imshow("Image", image)
	ch = cv2.waitKey(0)
	key = ch & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

#CHANGE dest_path to the appropriate destination in your PC

dest_path = r'CHANGE THIS'
cv2.imwrite(dest_path, image) 

df = pd.DataFrame(cpoints, columns = ['X', 'Y'])  #Generating a dataframe to prepare scatter plot
    
#Optimal number of Clusters
if len(cpoints) >=5:
	K_clusters = range(1,10)
	kmeans = [KMeans(n_clusters=i) for i in K_clusters]
	Y_axis = df[['Y']]
	X_axis = df[['X']]
	score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]

	# Visualize the elbow curve
	plt.plot(K_clusters, score)
	plt.xlabel('Number of Clusters')
	plt.ylabel('Score')
	plt.title('Elbow Curve')
	plt.show()

	num_clust = len(cpoints)//5 #Ensuring most clusters are at least 5 detections
else:
	num_clust = 1

#Create Clustering Model using KMeans
kmeans = KMeans(n_clusters = num_clust)
# Fit the Clustering Model on the Data
kmeans.fit(df)

# Print the Cluster Centers
print("Features", "\tX", "\tY")
print()

centers = kmeans.cluster_centers_

for i, center in enumerate(centers):
    print("Cluster", i, end=":\t")
    for coord in center:
        print(round(coord, 2), end="\t")
    print()

# Predict the Cluster Labels
labels = kmeans.predict(df)
# Append Labels to the Data
df_labeled = df.copy()
df_labeled["Cluster"] = pd.Categorical(labels)

# larger figure size for subplots
fig = plt.figure(figsize = [15,5])
#Cluster countplot
plt.subplot(1, 2, 1) # 1 row, 2 cols, subplot 1
sb.countplot(df_labeled["Cluster"])
#Visualise Clusters
plt.subplot(1, 2, 2) # 1 row, 2 cols, subplot 2
plt.scatter(x = "X", y = "Y", c = "Cluster", cmap='gist_rainbow', data = df_labeled)
plt.title('Distribution of vehicles', fontsize=10)
plt.xlabel('Total number of detections = {}'.format(len(cpoints)), fontsize=16)
plt.gca().invert_yaxis()
implot = plt.imshow(image_1)
plt.show()

fig_name = '{}_graph.png'.format(args['image'])#Saving the image in the directory

fig.savefig(fig_name)
graph_image = Image.open(fig_name)
new_image = graph_image.resize((1900, 700)) #Concatenated cluster diagram 
new_image.save(fig_name)

cv2.destroyAllWindows()

