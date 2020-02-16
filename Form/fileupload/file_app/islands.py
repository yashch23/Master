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
from .houghapp import HoughApp

sys.setrecursionlimit(10**6)


def DFS( i, j, visited, graph, row, col):
    rowNbr = [-1, -1, -1, 0, 0, 1, 1, 1];
    colNbr = [-1, 0, 1, -1, 1, -1, 0, 1];
    visited[i][j] = True
    for k in range(8):
        if isSafe(i + rowNbr[k], j + colNbr[k], visited, graph, row, col):
            DFS(i + rowNbr[k], j + colNbr[k], visited, graph, row, col)
    graph[i][j] = 0


def isSafe(i, j, visited, graph, row, col):
    return (i >= 0 and i < row and
            j >= 0 and j < col and
            not visited[i][j] and graph[i][j])


class Islands:

    def deleteIslands(l,graph,col,row,roi):
        visited = [[False for j in range(col)]for i in range(row)]
        for i in range(roi[l][1],roi[l][3]):
            for j in range(roi[l][0],roi[l][2]):
                if visited[i][j] == False and graph[i][j] == 1:
                    DFS(i, j, visited, graph, row, col)

        return graph
