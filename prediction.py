#from ucsd_dataset import ucsd_dataset
from models.c3d_model import C3DModel
from models.bc_model import BCModel
import numpy as np
import cv2
from videos import Video
import os
from flask import Flask, flash
import requests
import datetime

def sms(pesttext):
    url = 'https://www.smsgateway.center/SMSApi/rest/send'
    f = '%Y-%m-%d %H:%M:%S.%f%z'
    from datetime import datetime, timedelta
    t = datetime.now() + timedelta(seconds=19830)
    out = t.strftime("%Y-%m-%d %H:%M:%S")
    print(out)
    querystring = {
        'userId': 'mitron',
        'password': 'Mitron@123',
        'senderId': 'MiHelp',
        'sendMethod': 'simpleMsg',
        'msgType': 'text',
        'mobile': '9945393093',
        'msg': pesttext,
        'duplicateCheck': 'true',
        'format': 'json',
        'scheduleTime': out,
        }
    headers = {'cache-control': 'no-cache'}
    response = requests.request('GET', url, headers=headers,
                                params=querystring)
    print(response.text)

def main():
    # Load in one of the videos from the dataset
    #folder = "/home/sunil/Documents/2020-2021/public_risk/webapp/data/"#chaange location
    folder = "data/"
    selected_video = Video(folder, 1)
    selected_video.resize(112,112)
    selected_video = selected_video.getSegments()

    c3d = C3DModel()
    features, elapsed_time = c3d.predict(selected_video)
    print("c3d",features)
    print(features.shape)
    print("Extracting features...")
    print("Elapsed time: %fs" % (elapsed_time))
    bc = BCModel()
    bc.load_model("checkpoint/model")
    scores, elapsed_time = bc.predict(features)
    #print("bc",scores)
    #print(scores.shape)

    #url = '/home/sunil/Documents/2020-2021/public_risk/webapp/data/'#change location
    url = 'data/'
    img = []
    predictions = []
    #dir = os.path.splitext("/home/sunil/Documents/2020-2021/public_risk/webapp/data/")[0]#change Location
    dir = os.path.splitext("data/")[0]
    frames = len(os.listdir(dir))
    imageArr=[]
    for i in range(frames):
        image = cv2.imread(dir+"/frame%d.jpg"%i)
        if image is not None:
             imageArr.append(image)
    print("Images loaded!!!")        

    # Collect all the images into a Python list
    print("Gathering images...")
   # for k in range(0, frames+1):
   #     print("Progress: %2.1f" % (float(k) / frames))
   #     img.append(cv2.imread(url + '/frame' + str(k) + '.jpg'))

    height, width, layers = imageArr[0].shape

    print("Predicting scores...")
    print("Elapsed time: %fs" % (elapsed_time))

    # Iterate through and print out each 16-frame anomaly score and
    cou = 0
    for i in range(len(scores)):
        w = i*16
        # Ask use for the name of the video and how many frames to use

        if scores[i] > 0.5:
          for w in range((i*16),(i+1)*16):
              font = cv2.FONT_HERSHEY_SIMPLEX 
              #cv2.rectangle(img[w],(384,0),(240,240),(0,255,0),3)
              print("Printing Text...")
              cv2.putText(imageArr[w],'Risk Detected',(100,100), font, 0.8, (0,0,255), 2, cv2.LINE_AA)
              if cou == 0:
                 sms("Crime/Anomaly Detected ,Kindly click the location  https://goo.gl/maps/Vmk6UpgfW2aSPVrX6 --MitronTech")
                 #print("Risk Detected ,Kindly click the location https://goo.gl/maps/Vmk6UpgfW2aSPVrX6  --MitronTech")
                 cou = cou +1

        print("Frames (%4d to %4d)\tScore: %f\t%s" % (i*16,(i+1)*16,scores[i], "Risk detected!" if scores[i] > .4 else ""))
        predictions.append(scores[i])



    # Convert the list of images to a video and saves it to the working directory
    print("Creating video writer...")
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter('static/Risk.mp4', fourcc, 30.0, (width, height))
    print("Video writer created!")

    print("Total Frames: %d" % (len(img)))

    # Writes each image to the video
    print("Writing Frames...")
    try:
        for j in range(0, frames):
            print("Progress: %2.1f" % (float(j)/frames))
            video.write(imageArr[j])
    except (ValueError,IndexError):
        print("index out of range")

    # Finalization
    print("Finalizing...")
    cv2.destroyAllWindows()
    video.release()
    print("Finished!!!")
    results = ""
    predd = predictions
    if max(predd) >= 0.5:
        results = "Risk is detected in uploaded Video. Video is sent to Mail"
        #flash("Risk is detected in uploaded Video. Video is sent to Mail")
    else:
        results = "Risk is not detected in uploaded Video. Please re-upload or upload new video. You can refer in mail"
        #flash("Risk is not detected in uploaded Video. Please re-upload or upload new video. You can refer in mail")

    return results