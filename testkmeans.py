from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans  
from sklearn import datasets , svm , metrics
from PIL import Image , ImageDraw , ImageFilter
import numpy as np

image=Image.open('test.jpg')
#image=image.rotate(180)
crope=(30,10,155,80)
image=image.crop(crope)
image=image.filter(ImageFilter.GaussianBlur())

img_arr=np.asarray(image,dtype='int32')
cnt=0
Data= {'x':[],'y':[]}
for y in range(len(img_arr)):
    for x in range(len(img_arr[0])):
        if img_arr[y][x]<=220:
            Data['x'].append(x)
            Data['y'].append(y)
            cnt+=1

df = DataFrame(Data,columns=['x','y'])
cluster=4
cluster2=4
var=1
kmeans = KMeans(n_clusters=cluster).fit(df)
centroids=kmeans.cluster_centers_
while var==1:
    for x1 in range(0,cluster):
        for x2 in range(x1+1,cluster):
            if (abs(centroids[x1][0]-centroids[x2][0])<=15):
                cluster2=3
                break
    if cluster2==cluster:
        break
    else:
        cluster=cluster2
        kmeans = KMeans(n_clusters=cluster2).fit(df)
        centroids=kmeans.cluster_centers_
        break

#print(len(centroids),centroids[2][0],centroids[2][1])

centroids=sorted(centroids,key = lambda x: x[0])
print(centroids)

imageofnumber=[]
for point in centroids:
    imageofnumber.append(image.crop((point[0]-15,point[1]-20,point[0]+15,point[1]+23)))

#digits = datasets.load_digits()
#print(digits.target[0])


#images_and_labels = list(zip(digits.images, digits.target))
#print(len(images_and_labels),images_and_labels[5])
#for index, (image2, label) in enumerate(images_and_labels[:4]):
#    plt.subplot(2, 4, index + 1)
#    plt.axis('off')
#    plt.imshow(image2, cmap=plt.cm.gray_r, interpolation='nearest')
#    plt.title('Training: %i' % label)


#n_samples = len(digits.images)

#print(n_samples)
#data = digits.images.reshape((n_samples, -1))
################custom train
dataimage=[]
target=[]
for j in range(10):
    for i in range(1,10):
        try:
            img=Image.open('train/'+str(i)+str(j)+'.jpg')
            data_img=np.asarray(img,dtype="int32")
            data_img=np.concatenate(data_img,axis=0)
            dataimage.append(data_img)
            target.append(i)
        except IOError:
            pass 
############################
print(type(dataimage))
# Create a classifier: a support vector classifier
classifier = svm.SVC(gamma=0.000001 , C=100.)

# We learn the digits on the first half of the digits
#classifier.fit(data[:n_samples // 2], digits.target[:n_samples // 2])
classifier.fit(dataimage, target)

# Now predict the value of the digit on the second half:
#expected = digits.target[n_samples // 2:]
print("---------------")
print(len(dataimage[0]))
print("---------------")

dataimage=[]
for im in imageofnumber:
    #im.show()
    data_image=np.asarray( im,dtype="int32")
    data_image=np.concatenate(data_image,axis=0)
    dataimage.append(data_image)
    #dataimage['target']+=[1];
#dfimg = DataFrame(dataimage,columns=['images','target'])
#dataofimage=dfimg.images
#dataofimage=np.concatenate(dataofimage)
#dataofimage
print("-->",len(dataimage))
print("---------------")
predicted = classifier.predict(dataimage) #data[n_samples // 2:])

#print("Classification report for classifier %s:\n%s\n"
#      % (classifier, metrics.classification_report(expected, predicted)))
#print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
print("predict type: ",predicted)
numbers=''
for i in predicted:
    numbers+=str(i)
print(numbers)
#images_and_predictions = list(zip(digits.images[n_samples // 2:], predicted))
#for index, (image2, prediction) in enumerate(images_and_predictions[:4]):
#    plt.subplot(2, 4, index + 5)
#    plt.axis('off')
#    plt.imshow(image2, cmap=plt.cm.gray_r, interpolation='nearest')
#    plt.title('Prediction: %i' % prediction)

#plt.show()


imagefinal=ImageDraw.Draw(image)
for point in centroids:
    imagefinal.rectangle(((point[0]-15,point[1]-20),(point[0]+15,point[1]+23)),outline="black")
image.show()


