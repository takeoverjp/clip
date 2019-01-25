#!/usr/bin/python

import sys
import cv2
import numpy as np

DEBUG_CLIP=False
OUTPUT_SIZE = (28, 28)
MARGIN = 60

def clip(im):
  gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
  ret, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
  # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,\
  #                                cv2.THRESH_BINARY,11,2)
  neg = cv2.bitwise_not(thresh)
  kernel = np.ones((3,3),np.uint8)
  morph = cv2.morphologyEx(neg, cv2.MORPH_OPEN, kernel)
  kernel = np.ones((7,7),np.uint8)
  dilate = cv2.dilate(morph, kernel, iterations=2)
  x,y,w,h = cv2.boundingRect(dilate)

  x = x - MARGIN
  w = w + MARGIN * 2
  y = y - MARGIN
  h = h + MARGIN * 2

  if w > h:
    y = y - (w-h)/2
    h = w
  elif w < h:
    x = x - (h-w)/2
    w = h
  clip = dilate[y:y+h, x:x+w]
  result = cv2.resize(clip, OUTPUT_SIZE)

  if DEBUG_CLIP:
    cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('orig', im)
    cv2.imshow('gray', gray)
    cv2.imshow('thresh', thresh)
    cv2.imshow('morph', morph)
    cv2.imshow('dilate', dilate)
    cv2.imshow('result', result)
    cv2.waitKey()
    cv2.destroyAllWindows()

  return result

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('[USAGE] ' + sys.argv[0] + ' INFILE OUTFILE')
    exit(1)

  infile = sys.argv[1]
  outfile = sys.argv[2]

  im = cv2.imread(infile)

  clipped = clip(im)

  clipped.tofile(outfile)

  f = np.fromfile(outfile,
                  dtype=np.uint8,
                  count=OUTPUT_SIZE[0]*OUTPUT_SIZE[1])
  result = f.reshape(OUTPUT_SIZE)
  cv2.imshow('input', im)
  cv2.imshow('result', result)
  cv2.waitKey()
  cv2.destroyAllWindows()
