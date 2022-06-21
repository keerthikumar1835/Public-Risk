import cv2
import glob, os, os.path
def frame_extaction(filename):
  try:
    mydir = 'data/'
    filelist = glob.glob(os.path.join(mydir, "*.jpg"))
    for f in filelist:
      os.remove(f)
  except:
    print("no file found")
  vidcap = cv2.VideoCapture(filename)
  def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*100)
    hasFrames,image = vidcap.read()
    if hasFrames:
      cv2.imwrite("data/frame"+str(count)+".jpg", image)
    return hasFrames
  sec = 0
  frameRate = 0.5
  count=1
  success = getFrame(sec)
  while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)

