# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 01:40:58 2018

@author: Dylan
"""

import cv2
import numpy as np
 
cap = cv2.VideoCapture('Lecture-13.mp4')
'''
Make sure your_video is in the same dir, else mention the full path.
'''
while True:
    ret, frame = cap.read()
    #gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame',frame)
    #cv2.imshow('grayF',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
 
cap.release()
cv2.destroyAllWindows()