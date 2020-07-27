'''
Apply trained machine learning model to an entire image scene using
a sliding window.

USAGE: python detect_plane.py "ARG(1)" "ARG(2)"

ARGUMENTS: (1) "models/model.tfl" (2) "imagePath"

OUTPUT: Detected image + Cluster Diagram 
''' 

import sys
import os
import numpy as np
from PIL import Image
from scipy import ndimage
from model import model

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sb
from skimage.measure import EllipseModel
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
import cv2
from sklearn.cluster import KMeans

def detector(model_fname, in_fname):
    """ Perform a sliding window detector on an image.

    Args:
        model_fname (str): Path to Tensorflow model file (.tfl)
        in_fname (str): Path to input image file
        out_fname (str): Path to output image file. Default of None.

    """

    # Load trained model
    model.load(model_fname)

    # Read input image data
    im = Image.open(in_fname)
    im = im.resize((950, 700))
    im.save(in_fname)

    arr = np.array(im)[:,:,0:3]
    shape = arr.shape

    # Set output fname
    out_fname = os.path.splitext(in_fname)[0] + '_output.jpg'

    # Create detection variables
    detections = np.zeros((shape[0], shape[1]), dtype='uint8')
    output = np.copy(arr)

    # Sliding window parameters
    step = 2
    win = 20

    # Loop through pixel positions
    print('Processing...')
    for i in range(0, shape[0]-win, step):
        print('row %1.0f of %1.0f' % (i, (shape[0]-win-1)))

        for j in range(0, shape[1]-win, step):

            # Extract sub chip
            chip = arr[i:i+win,j:j+win,:] 
            
            # Predict chip label
            prediction = model.predict_label([chip / 255.])[0][0]

            # Record positive detections
            if prediction == 1:
                detections[i+int(win/2), j+int(win/2)] = 1
    # Process detection locations
    dilation = ndimage.binary_dilation(detections, structure=np.ones((3,3)))
    labels, n_labels = ndimage.label(dilation)
    center_mass = ndimage.center_of_mass(dilation, labels, np.arange(n_labels)+1)
    # Loop through detection locations
    if type(center_mass) == tuple: center_mass = [center_mass]
    for i, j in center_mass:
        i = int(i - win/2)
        j = int(j - win/2)
        
        # Draw bounding boxes in output array
        output[i:i+win, j:j+2, 0:3] = [255,0,0]
        output[i:i+win, j+win-2:j+win, 0:3] = [255,0,0]
        output[i:i+2, j:j+win, 0:3] = [255,0,0]
        output[i+win-2:i+win, j:j+win, 0:3] = [255,0,0]
    # Save output image
    outIm = Image.fromarray(output)
    outIm.save(out_fname)

    #Cluster plot
    im = Image.open(in_fname)
    cpoints = [[j,i] for i,j in center_mass if center_mass] #All the detection centroids
    df = pd.DataFrame(cpoints, columns = ['X', 'Y'])  #To collect data for scatter plot

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

        num_clust = len(cpoints)//10 #Keeping most clusters at least 10 detections
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
    plt.title('Distribution of planes', fontsize=10)
    plt.xlabel('Total number of detections = {}'.format(len(cpoints)), fontsize=16)
    plt.gca().invert_yaxis()
    implot = plt.imshow(im)
    plt.show()

    fig_name = '{}_graph.png'.format(os.path.splitext(in_fname)[0])
    fig.savefig(fig_name)

    graph_image = Image.open(fig_name)
    new_image = graph_image.resize((1900, 700)) #Saving the cluster diagram
    new_image.save(fig_name)

    cv2.destroyAllWindows()


# Main function
if __name__ == "__main__":

    # Run detection function with command line inputs
    detector(sys.argv[1], sys.argv[2])



