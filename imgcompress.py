import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy
import sys

img = plt.imread(sys.argv[1])

width = img.shape[0]
height = img.shape[1]
count = img.shape[2]

img = img.reshape(width*height,count)

kmeans = KMeans(n_clusters=int(sys.argv[3])).fit(img)

labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_
img2 = numpy.zeros_like(img)

# img2 = numpy.zeros((width,height,count), dtype=numpy.uint8)
# count = 0
# for i in range(width):
# 	for j in range(height):
# 		img2[i][j] = clusters[labels[count]]
# 		count+=1

for i in range(len(img2)):
	img2[i] = clusters[labels[i]]
img2 = img2.reshape(width,height,count)

plt.imshow(img2)
plt.savefig(sys.argv[2])
plt.show()
