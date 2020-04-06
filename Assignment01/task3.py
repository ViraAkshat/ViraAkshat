import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image
from scipy.cluster.vq import kmeans2

def K_Clustering(img, k) :
# Input an image
#img = plt.imread('image01.jpeg')

# converting to float
    imgf = img.astype(float)
    print(imgf)

# Converting to 2d
    nr, nc, c = img.shape
    print(nr, nc, c)
    imgf = imgf.reshape((nr*nc, 3))
    print(imgf.shape)

#K Clustering
    centroid, label = kmeans2(imgf, k, minit = '++')
    imgf = centroid[label]
    imgf = imgf.reshape((nr, nc, c))
    imgOut = imgf.astype(np.uint8)

    return imgOut

path = plt.imread(input("Enter image path: "))
#path = plt.imread('image01.jpeg')
k = int(input("Enter K value: "))
pathOut = input("Enter the path for Output Image: ")

kImg = K_Clustering(path, k) #function call
# Plotting & Saving an image
plt.figure()
plt.imshow(kImg, cmap = 'hot', interpolation = 'nearest')
plt.axis('off')
plt.title('k = ' + k)
plt.show()
image.imsave(pathOut, kImg)