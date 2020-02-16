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
import time
from multiprocessing import Process, Manager
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed




class Mapping:


        def __init__(self, roi, x, closex, closey):
            self.roi = roi
            self.x = x
            self.closex = closex
            self.closey = closey
            self.closeMap = []


        def cmap(self):
            textlist = self.roi
            textontop = np.zeros(len(textlist))
            checkleft = np.zeros(len(self.x))
            count = 0

            for i in range(len(self.closey)):
                textonleft = np.zeros(len(textlist))
                boxtextline = np.zeros(len(self.closex[i]))

                for j in range(len(self.closey[i])):
                    dist = []
                    textonline = np.zeros(len(textlist))

                    for textitr in range(len(textlist)):
                        if(textlist[textitr][3]<self.closey[i][j][0] and textontop[textitr]==0 ):
                            dist.append(self.closey[i][j][0]-textlist[textitr][3])
                        elif(textlist[textitr][1]<self.closey[i][j][1] and textontop[textitr]==0 ):
                            textonline[textitr]=1
                            dist.append(10000)
                        else:
                            dist.append(10000)


                    #When the box has a closest text on the top, and doesn't have any text on its line
                    minindex = np.argmin(dist)
                    if(textontop[minindex]==0 and textonline.any()!=1 and boxtextline[j]!=1):
                        dist1 = []

                        for n in range(0,len(self.closey[i])):
                            if(self.closex[i][n][1]>textlist[minindex][0]):
                                dist1.append(self.closex[i][n][1]-textlist[minindex][0])
                            else:
                                dist1.append(10000)

                        minindex1 = np.argmin(dist1)
                        self.closeMap.append((textlist[minindex],(self.closex[i][minindex1][0],self.closey[i][minindex1][0],self.closex[i][minindex1][1],self.closey[i][minindex1][1])))
                        textontop[minindex] = 1
                        boxtextline[minindex1]=1


                    #When the box has a closest text on the top, and also on the same line, we select the text on the same line on the left
                    elif(textontop[minindex]==0 and textonline.any()==1 and boxtextline[j]!=1):
                        dist3=[]
                        flagforboxleft = 0
                        flagtopright=0
                        boxfortopright = []
                        flagright = 0
                        listoftrueboxes = np.zeros(len(self.closex[i]))
                        listofboxright = np.zeros(len(self.closex[i]))

                        for y in range(len(self.closey[i])):
                            dist2 = []
                            for m in range(len(textonline)):

                                #if box is right of text, viola
                                if(int(textonline[m])==1 and textlist[m][2]<self.closex[i][y][1]):
                                    flagforboxleft = 1
                                    flagtopright = 1
                                    dist2.append(self.closex[i][y][1] - textlist[m][2])

                                else:
                                    dist2.append(10000)


                                #if box is left of textonline and right of the textontop
                                if(int(textonline[m])==1 and textlist[m][0]>self.closex[i][j][1] and textlist[minindex][0]<self.closex[i][j][1]):
                                    flagforboxleft = 1
                                    flagright = 1

                            if(flagtopright==0):
                                dist3.append(textlist[self.closex[i][y][1]-minindex][0])
                                listoftrueboxes[y]=1
                            else:
                                dist3.append(10000)

                            if((flagtopright==1 and flagright==1) or flagright==0):
                                minindex2 = np.argmin(dist2)
                                self.closeMap.append((textlist[minindex2],(self.closex[i][y][0],self.closey[i][y][0],self.closex[i][y][1],self.closey[i][y][1])))
                                boxtextline[y] = 1
                                textontop[minindex] = 1


                        #to assign the text on top for the box being left but the textontop right
                        if(flagtopright==0):
                            minindex3 = np.argmin(dist3)
                            self.closeMap.append((textlist[minindex],(self.closex[i][minindex3][0],self.closey[i][minindex3][0],self.closex[i][minindex3][1],self.closey[i][minindex3][1])))
                            boxtextline[minindex3] = 1
                            textontop[minindex]=1


                        #for the box to be exclusively left of everything
                        if(flagforboxleft==0):
                            self.closeMap.append((0,(self.closex[i][j][0],self.closey[i][j][0],self.closex[i][j][1],self.closey[i][j][1])))
                            boxtextline[j]=1
                            flagtopright = 1

            return self.closeMap,textonline
