# for making frames of star trails as they move across the sky

from cgitb import grey
import skimage.filters
import skimage.color
import skimage.util
import skimage.io
import matplotlib.pyplot as plt
import numpy as np
import glob

out_dir = "e/"  # output dir prefix

raws = glob.glob("*.jpg")
raws.sort()

# use the first image as the starting point
lastimage = skimage.io.imread(raws[0])

skip = 3
skipCounter = 0

for raw in raws:
    image = skimage.io.imread(raw)  # open image
    gray_image = skimage.color.rgb2gray(image)  # turn grayscale
    gray_image = skimage.filters.gaussian(gray_image, sigma=1.0)
    binary_mask = gray_image > 0.02  # threshhold
    image[~binary_mask] = 0  # shine image through bright areas

    image += lastimage
    # add image to last image and don't overflow
    image[image < lastimage] = 255
    if(skipCounter >= skip):
        skimage.io.imsave(out_dir+raw, image)
        skipCounter = -1
    skipCounter += 1

    lastimage = image
    print(raw)
