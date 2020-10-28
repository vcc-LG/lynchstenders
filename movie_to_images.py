import cv2
import os.path


def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success, image = vidcap.read()
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count*5000))    # added this line
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        cv2.imwrite(('./output/'+('frame%d' % count))+'.png', image)
        count = count + 1


extractImages('twin_peaks.mkv', 'output')
