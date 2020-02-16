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




class HoughApp:
    def houghfunc(imgCrop):
            img_shape = imgCrop.shape
            x_max = img_shape[0]
            y_max = img_shape[1]
            theta_max = 1.0 * math.pi
            theta_min = 0.0
            r_min = 0.0
            r_max = math.hypot(x_max, y_max)
            r_dim = 2*math.ceil(r_max) - 1
            theta_dim = 180
            hough_space = np.zeros((r_dim,theta_dim))
            for x in range(x_max):
                for y in range(y_max):
                    if imgCrop[x][y] == 255: continue
                    for itheta in range(theta_dim):
                        theta =  (theta_max) - (1.0 * itheta * theta_max / theta_dim )
                        r = x * math.cos(theta) + y * math.sin(theta)
                        ir = r + math.ceil(r_max)
                        hough_space[round(ir),itheta] = hough_space[round(ir),itheta] + 1
            H = hough_space
            rho = r_dim
            theta = theta_dim
            #Finding the streaks peaks from Hough transform
            L2 = np.zeros((rho, theta))
            Y = np.zeros(rho)
            circ = np.zeros((rho, theta))

            for Q in range(theta):
                for S in range(rho):
                    Y[S] = H[S,Q]

                for P in range(rho - 3):
                    avgg = ((Y[P] + Y[P+1] + Y[P+2])/3)
                    if(avgg<1):
                        avgg=0
                    Y[P] = avgg
                    Y[P+1] = avgg
                    Y[P+2] = avgg

                circ[:,Q] = Y
                maxx = 0.2*max(Y);
                peaks, properties = find_peaks(Y, height=maxx, distance = 40, prominence=5)

                for W in range(len(peaks)):
                    L2[peaks[W]][Q]=Y[peaks[W]]
            #Finding if it's asymmetric
            temp = np.zeros(theta)
            for i in range(theta):
                for j in range(rho):
                    if(j<rho - 3 and circ[j,i]==0 and circ[j+1,i]!=0 and circ[j+2,i]!=0):
                        first = j
                    if(j>2 and circ[j,i]==0 and circ[j-1,i]!=0 and circ[j-2,i]!=0):
                        last = j

                temp[i] = last - first
            #Finding if the contour is circle or rect
            varianceTemp = statistics.variance(temp)
            varmin = min(temp)
            varmax = max(temp)

            asymmetricFlag = 0
            symmetricFlag = 0
            if((varmax/varmin)>1.2):
                asymmetricFlag = 1
            else:
                symmetricFlag = 1
                asymmetricFlag=0


            return asymmetricFlag
