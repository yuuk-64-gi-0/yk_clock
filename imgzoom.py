import cv2
import sys
import os

inimgpath = sys.argv[sys.argv.index("-i") + 1]
outimgpath = sys.argv[sys.argv.index("-o") + 1]
afterheight = int(sys.argv[sys.argv.index("-h") + 1])

inimg = cv2.imread(inimgpath,-1)
insize = inimg.shape[:2]
outsize = (int(0.5 * insize[1] * afterheight / insize[0]) * 2,afterheight)
outimg = cv2.resize(inimg,outsize)
os.chdir(os.path.dirname(outimgpath))
cv2.imwrite(os.path.basename(outimgpath),outimg)