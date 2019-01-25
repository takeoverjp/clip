#!/usr/bin/python

import cv2
import numpy as np

DEBUG_CLIP=False
OUTPUT_SIZE = (28, 28)
MARGIN = 30

def clip(im):
  gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
  ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
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
  im = cv2.imread("data/001.jpg")
  height = int(round(im.shape[0]/8))
  width  = int(round(im.shape[1]/8))
  resize = cv2.resize(im, (width, height))

  clipped = clip(resize)

  clipped.tofile("data/001_clipped.raw")

  f = np.fromfile('data/001_clipped.raw',
                  dtype=np.uint8,
                  count=OUTPUT_SIZE[0]*OUTPUT_SIZE[1])
  result = f.reshape(OUTPUT_SIZE)
  cv2.imshow('input', resize)
  cv2.imshow('result', result)
  cv2.waitKey()
  cv2.destroyAllWindows()
