import numpy as np
import matplotlib.pyplot as plt
import cv2

# read image
im = cv2.imread('test.jpg')
# calculate mean value from RGB channels and flatten to 1D array
vals = im.mean(axis=2).flatten()
print(len(vals))
# calculate histogram
counts, bins = np.histogram(vals, range(256))
# plot histogram centered on values 0..255
#plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
#plt.xlim([-0.5, 255.5])
histr = cv2.calcHist([im],[0],None,[256],[0,256])
plt.hist(im.ravel(),256,[0,256])
plt.show()
