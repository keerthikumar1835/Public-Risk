#run
import cv2
import os
import numpy as np
#import matplotlib.pyplot as plt

class Video(object):

    def __init__(self, filename, isAnomaly, width=320, height=240):
        if filename is None:
            raise ValueError("invalid filename argument")
        self.isAnomaly=isAnomaly
        self.filename = filename
        self.frames=[]
        self.frameCount = 0
        self.width = width
        self.height = height
        self.__setFrames()


    def __split(self):
        print(self.filename)
        if os.path.exists(self.filename) is False:
            raise ValueError("Video File Not Found. Could not find: %s" % ('data/'+self.filename))
        videoSource = cv2.VideoCapture(self.filename)
        success,image = videoSource.read() #success is true if file exist, and loads first frame in image
        count = 0
        dir = os.path.splitext(self.filename)[0] 
        if os.path.isdir(dir) is False:
            os.makedirs(dir)
        while success:
            resize_image = cv2.resize(image,(self.width, self.height))
            cv2.imwrite(dir+"/frame%d.jpg" %count,resize_image)
            success, image = videoSource.read()
            count+=1
        #print("Read %d Frames" %count)
        return count


    def __setFrames(self):

        dir = os.path.splitext(self.filename)[0]
        if os.path.isdir(dir) is False:
            self.__split()

        count = len(os.listdir(dir))

        imageArr=[]
        for i in range(count):
            image = cv2.imread(dir+"/frame%d.jpg"%i)
            if image is not None: 
                imageArr.append(image)

        self.frames=imageArr
        self.frameCount = len(imageArr)

    def getFrames(self):
        return np.array(self.frames)

    def getAnomaly(self):
        return self.isAnomaly

    def getFilename(self):
        return self.filename

    def getFrameCount(self):
        return self.frameCount

    def resize(self, new_width, new_height):
        self.frames = [cv2.resize(frame, (new_width, new_height)) for frame in self.frames]

    def getSegments(self):
        count = self.getFrameCount()
        print("Getting segments:", count, " total frames.")
        frames = np.array(self.getFrames())
        print("FRAMES SHAPE: %s" % (str(frames.shape)))
        if count % 16 != 0:
            print("REMOVING FRAMES: %d" % (count%16))
            frames = frames[:-(count%16)]

        segments = frames.reshape([-1, 16, 112, 112, 3])
        
        print("SEGMENT SHAPE: %s" % (str(segments.shape)))
        return segments

    def __str__(self):
        return "You are print video object, use one of my methods, My filename is "+self.filename

