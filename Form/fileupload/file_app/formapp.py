import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import numpy as np
import matplotlib.image as mpimg
import cv2
import math
import imutils
import sys
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import find_peaks
import statistics
import threading
import json
import time
from multiprocessing import Process, Manager
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed
from .houghapp import HoughApp
from .islands import Islands
from .mapping import Mapping



#sending and receiving text OCR from azure
class FormApp:
    def __init__(self, data):
        self.data = data
        self.image_path = '../fileupload'+ data
        self.cntr = []
        self.wdth = []
        self.roi = []
        self.polygons = []
        self.analysis = {}
        self.closeMap = []

    def mainapp(self):

        def OCR():
            text_recognition_url = "https://southeastasia.api.cognitive.microsoft.com/" + "vision/v2.0/read/core/asyncBatchAnalyze"
            image_data = open(self.image_path, "rb").read()
            headers = {'Ocp-Apim-Subscription-Key': 'c1bb997019b04634a6324da15ce99d8f',
                      'Content-Type': 'application/octet-stream'}

            response = requests.post(text_recognition_url, headers=headers, data = image_data)
            response.raise_for_status()
            operation_url = response.headers["Operation-Location"]
            poll = True
            while (poll):
                response_final = requests.get(
                    response.headers["Operation-Location"], headers=headers)
                self.analysis = response_final.json()
                time.sleep(0.4)
                if ("recognitionResults" in self.analysis):
                    poll = False
                if ("status" in self.analysis and self.analysis['status'] == 'Failed'):
                    poll = False


        #The image presprocessing to remove the shadows



        def Remove_Shadows():
            self.img = cv2.imread(self.image_path, -1)
            dimensions = self.img.shape
            height = self.img.shape[0]
            width = self.img.shape[1]
            channels = self.img.shape[2]
            rgb_planes = cv2.split(self.img)
            result_planes = []
            result_norm_planes = []

            for plane in rgb_planes:
                dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
                bg_img = cv2.medianBlur(dilated_img, 21)
                diff_img = 255 - cv2.absdiff(plane, bg_img)
                norm_img = cv2.normalize(diff_img, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
                result_norm_planes.append(norm_img)

            result_norm = cv2.merge(result_norm_planes)
            gray = cv2.cvtColor(result_norm, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            rect,self.thresh = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            l,self.graph =cv2.threshold(self.thresh,0,1,cv2.THRESH_BINARY_INV)
            self.row = self.thresh.shape[0]
            self.col = self.thresh.shape[1]

        t1 = threading.Thread(target=OCR, name='t1')
        t2 = threading.Thread(target=Remove_Shadows, name='t2')
        t1.start()
        t2.start()
        t1.join()
        t2.join()


        if ("recognitionResults" in self.analysis):

            self.polygons = [(line["boundingBox"], line["text"])
                        for line in self.analysis["recognitionResults"][0]["lines"]]

        for polygon in self.polygons:
            self.cntr.append(((polygon[0][0]+polygon[0][2]+polygon[0][4]+polygon[0][6])/4,(polygon[0][1]+polygon[0][3]+polygon[0][5]+polygon[0][7])/4))
        for polygon in self.polygons:
            self.wdth.append(abs((polygon[0][2]+polygon[0][4])/2 - (polygon[0][0]+polygon[0][6])/2))
        for polygon in self.polygons:
            self.roi.append((min(polygon[0][0],polygon[0][6]),min(polygon[0][1],polygon[0][3]),max(polygon[0][2],polygon[0][4]),max(polygon[0][5],polygon[0][7])))


        #Connected Islands Algo
        for l in range(0,len(self.roi)):
            self.graph = Islands.deleteIslands(l,self.graph,self.col, self.row, self.roi)




        self.graph = self.graph*255
        contours = cv2.findContours(self.graph.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours = imutils.grab_contours(contours)

        x = []
        y = []
        w = []
        h = []

        for c in contours:
            cv2.drawContours(self.img, [c], -1, (0, 255, 0), 3)
            tempx = []
            tempy = []

            for l in c:
                for m in l:
                    tempx.append(m[0])
                    tempy.append(m[1])
            f = min(tempx)
            g = min(tempy)
            r = max(tempx)
            i = max(tempy)
            x.append(f)
            y.append(g)
            w.append(r)
            h.append(i)


        #more preprocessing



        closey = []
        closex = []
        count = 0
        for i in range(len(x)):

            #skips very small contours, KEEPS THE HORIZONTAL LINES, AND NOT VERTICAL LINES
            thresholdContour = 11
            if((w[i]-x[i]<thresholdContour and h[i]-y[i]<thresholdContour)):
                continue

            temp = []
            tempx = []
            temp.append((y[i],h[i]))
            tempx.append((x[i],w[i]))


            flag = 0
            for j in range(i+1,len(x)):
                if((h[j]>y[i] and y[j]<y[i]) or (y[j]>y[i] and h[j]<h[i]) or (y[j]< h[i] and h[j]>h[i])):

                    # Checking if one contour is inside another contour, then skip the one that lies inside. doesn't work for heirchy 2 levels contours
                    if(x[j]>x[i]-15 and w[j]<w[i]+15):
                        flag = 1
                    if(x[i]>x[j]-15 and w[i]<w[j]+15):
                        flag = 2
                    if(flag ==2):
                        temp.pop()
                        tempx.pop()
                        continue
                    if(flag == 1):
                        break
                    temp.append((y[j],h[j]))
                    tempx.append((x[j],w[j]))
            if(flag!=2):
                closey.append(temp)
                closex.append(tempx)


        #delete the single duplicates in closex and closey
        i = 0
        while(i<len(closex)):
            flag=0
            try:
                if(len(closex[i])==1):
                    for j in range(len(closex)):
                        if(len(closex[j])>1):
                            for k in closex[j]:
                                if (closex[i][0]==k):
                                    flag = 1
                                    break
                        if(flag==1):
                            del closex[i],closey[i]
                            break
                if(flag==1):
                    i-=1
            except:
                break
            i = i+1

        minc = []
        def Reverse(lst):
            lst.reverse()
            return lst

        closex = Reverse(closex)
        closey = Reverse(closey)

        value = []
        count = 0
        for i in range(len(closex)):
            for j in range(len(closex[i])):
                try:
                    cropImg = self.thresh[closey[i][j][0]-20:closey[i][j][1]+20,closex[i][j][0]-20:closex[i][j][1]+20]
                    value.append(cropImg)
                except:
                    cropImg = self.thresh[closey[i][j][0]:closey[i][j][1],closex[i][j][0]:closex[i][j][1]]
                    value.append(cropImg)
                count+=1
        result_assy = []
        with ProcessPoolExecutor(max_workers = len(value)) as executor:
            results = executor.map(HoughApp.houghfunc, value)
        for result in results:
            result_assy.append(result)



        #Algo for mapping

        self.closeMap,textonline = Mapping(self.roi,x,closex, closey).cmap()

        #if polygon is small

        def checksizeFunc(j):

            checksizeFlag = np.zeros(len(self.closeMap))
            for i in range(len(self.closeMap)):
                if(len(self.closeMap[i])==2):
                    sizeTextx = self.closeMap[i][0][2]-self.closeMap[i][0][0]
                    sizeTexty = self.closeMap[i][0][3]-self.closeMap[i][0][1]
                    if(self.closeMap[i][1][2]-self.closeMap[i][1][0]< 1.5*sizeTexty and self.closeMap[i][1][3]-self.closeMap[i][1][1] < 5*sizeTexty):
                        checksizeFlag[i]=1
            #one, if the size is small, hence check
            return(checksizeFlag[j])

        imgNum = len(textonline)
        def Crop(noImg):
            try:
                if(noImg<=imgNum):
                    cropImg = self.thresh[self.closeMap[noImg][1][1]-20:self.closeMap[noImg][1][3]+20,self.closeMap[noImg][1][0]-20:self.closeMap[noImg][1][2]+20]
                return cropImg
            except:
                cropImg = self.thresh[self.closeMap[noImg][1][2]:self.closeMap[noImg][1][3],self.closeMap[noImg][1][0]:self.closeMap[noImg][1][2]]
                return cropImg



        #checking heirchy of contours

        def hierarchy(i,j):
            imgCrop = Crop(j)
            contours,hierarchy = cv2.findContours(imgCrop, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
            return(contours, hierarchy)



        mainText = ''

        fieldMap = {}


        for i in range(len(self.cntr)):
            name = '';
            type = '';
            sub_type = '';

            count = 0
            for j in range(len(self.closeMap)):
                if(self.cntr[i][0]>self.closeMap[j][0][0] and self.cntr[i][0]<self.closeMap[j][0][2] and self.cntr[i][1]>self.closeMap[j][0][1] and self.cntr[i][1]<self.closeMap[j][0][3]):

                    asymmetricFlag=result_assy[j]
                    checksizeFlag = checksizeFunc(j)

                    #for radiobuttons
                    type = 'input'
                    if(asymmetricFlag==0 and int(checksizeFlag)==1):
                        sub_type = 'radio'
                        count = 1
                    #for checkboxes
                    if(asymmetricFlag==1 and int(checksizeFlag)==1):
                        sub_type = 'checkbox'
                        count = 1
                    #for text
                    if(asymmetricFlag==1 and int(checksizeFlag)==0):

                        if(len(hierarchy(i,j)[1][0])>3):
                            sub_type = 'date'
                        else:
                            sub_type = 'text'
                        count = 1

                    if(count == 1):
                        name = self.polygons[i][1]

            if(count==0):
                name = self.polygons[i][1]
                type = 'header';

            field = []
            field.append(name);
            field.append(type);
            field.append(sub_type);
            fieldMap[i] = field;

        print(json.dumps(fieldMap))

        return(fieldMap)
