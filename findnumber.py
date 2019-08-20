from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn import datasets , svm , metrics
from PIL import Image , ImageDraw
import numpy as np

class findnumber:
    def __init__(self):
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
        
        self.classifier = svm.SVC(gamma=0.000001 , C=100.)
        self.classifier.fit(dataimage, target)

       
    def __read_image(self,image):

        #mage=Image.open('test.jpg')
        #image=image.rotate(180)
        crope=(30,10,155,80)
        image=image.crop(crope)
    
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
        #centroids.reverse();
        #print(centroids)
        self.imageofnumber=[]
        for point in centroids:
            self.imageofnumber.append(image.crop((point[0]-15,point[1]-20,point[0]+15,point[1]+23)))
        #imagefinal=ImageDraw.Draw(image)
        #for point in centroids:
            #imagefinal.rectangle(((point[0]-15,point[1]-20),(point[0]+15,point[1]+23)),outline="black")
        #image.show()
        dataimage=[]
        for im in self.imageofnumber:
            #im.show()
            data_image=np.asarray( im,dtype="int32")
            data_image=np.concatenate(data_image,axis=0)
            dataimage.append(data_image)
        predicted = self.classifier.predict(dataimage)
        self.number_string=''
        for i in predicted:
            self.number_string+=str(i)
        ############################

    def get_seperated_images_list(self,src_img):
        self.__read_image(src_img)
        return self.imageofnumber
    def get_numberstr_from_image(self,src_img):
        self.__read_image(src_img)
        return self.number_string
