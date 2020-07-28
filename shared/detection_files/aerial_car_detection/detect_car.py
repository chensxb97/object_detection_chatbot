#USAGE 
#python detect_car.py -i [IMAGE PATH] 

#OUTPUT: Detected image + Cluster Diagram 

from imageai.Detection.Custom import CustomObjectDetection
import argparse
import numpy as np
import time
import cv2
import os
import keras 
from keras_applications import vgg16
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to image")
args = vars(ap.parse_args())

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath("detection_model-ex-046--loss-8.848.h5")
detector.setJsonPath("detection_config.json")
detector.loadModel()

image = cv2.imread(args["image"])
image = cv2.resize(image,(950,700), interpolation = cv2.INTER_AREA)
cv2.imwrite(args['image'],image)

LABELS = ['car']

detections = detector.detectObjectsFromImage(input_image=args['image'], output_image_path="{}_output.jpg".format(args['image']))
for detection in detections:
    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])

cpoints = []
classes= []
# ensure at least one detection exists
if len(detections) > 0:
	# loop over the indexes we are keeping
	for detection in detections:
		# extract the bounding box coordinates
		(x, y) = (detection['box_points'][0],detection['box_points'][1])
		(x2, y2) = (detection['box_points'][2],detection['box_points'][3])
		cx = int((x+x2)/2)
		cy = int((y+y2)/2)
		point = [cx,cy]
		cpoints.append(point) #Collating all centroids
		classes.append(LABELS.index(detection['name']))

num_car= classes.count(0)
print('Number of cars: {}'.format(num_car))

image = cv2.imread(args["image"])
image_raw = image.copy()
output_image_name="{}_output.jpg".format(args['image'])
output_image = cv2.imread(output_image_name) #Saving the output image

df = pd.DataFrame(cpoints, columns = ['X', 'Y'])  #To collect data for the scatter plot
    
#Finding the optimal number of clusters
print(df['X'])

#Optimal number of Clusters
if len(cpoints) >=10:
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

	num_clust = len(cpoints)//10 #Ensuring most clusters have at least 10 detections
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
implot = plt.imshow(image_raw)
plt.show()

fig_name = '{}_graph.png'.format(args['image'])
fig.savefig(fig_name)

graph_image = Image.open(fig_name)
new_image = graph_image.resize((1900, 700)) #To generate the cluster diagram
new_image.save(fig_name)

cv2.destroyAllWindows()





