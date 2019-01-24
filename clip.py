#!/usr/bin/python

import cv2
import numpy as np

if __name__ == '__main__':
  fd = open('data/001.raw', 'rb')
  rows = 28
  cols = 28
  f = np.fromfile(fd, dtype=np.uint8,count=rows*cols)
  im = f.reshape((rows, cols))
  fd.close()

  dst = im[10:20, 10:20]
  cv2.imwrite('clip.bmp',dst)

  cv2.imshow('original', im)
  cv2.imshow('clipped', dst)
  cv2.waitKey()
  cv2.destroyAllWindows()
