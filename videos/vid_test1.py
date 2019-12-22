# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 01:44:25 2018

@author: Dylan
"""

import cv2

vidFile = cv2.CaptureFromFile( 'Lecture-13.mp4' )

nFrames = int(  cv2.GetCaptureProperty( vidFile, cv2.CV_CAP_PROP_FRAME_COUNT ) )
fps = cv2.GetCaptureProperty( vidFile, cv2.CV_CAP_PROP_FPS )
waitPerFrameInMillisec = int( 1/fps * 1000/1 )

print('Num. Frames = ', nFrames)
print('Frame Rate = ', fps, ' frames per sec')

for f in xrange(nFrames):
  frameImg = cv2.QueryFrame( vidFile )
  cv2.ShowImage( "My Video Window",  frameImg )
  cv2.WaitKey( waitPerFrameInMillisec  )

# When playing is done, delete the window
#  NOTE: this step is not strictly necessary, 
#         when the script terminates it will close all windows it owns anyways
cv2.DestroyWindow( "My Video Window" )