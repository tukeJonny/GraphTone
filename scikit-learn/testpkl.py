# -*- coding: utf-8 -*-

import os
from PIL import Image
from PIL import ImageOps
import numpy as np
import pylab as pl
import pandas as pd
from sklearn.decomposition import RandomizedPCA
from sklearn.externals import joblib
from sklearn.svm import LinearSVC
from sklearn import datasets
from sklearn.externals import joblib

STANDARD_SIZE = (300, 167)
def img_to_matrix(filename, verbose=False):
	"""
	take a filename and turns it into a numpy array of RGB pixels
	array([[255,255,255],
		   [255,255,250],
		   [250,250,250],
		   ...,])
	"""
	print "Opening " + str(filename) + "..."
	img = Image.open(filename)
	#img = ImageOps.grayscale(img)
	if verbose == True:
		print "changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE))
	img = img.resize(STANDARD_SIZE)
	imgArray = np.asarray(img)
	return(imgArray)

def flatten_image(img):
	"""
	takes in an (m, n) numpy array and flattens it
	into an array of shape (1, m*n)
	"""
	s = img.shape[0] * img.shape[1] * img.shape[2]
	img_wide = img.reshape(1, s)
	return img_wide[0]

img_dir = "tests/"

images = [img_dir + r for r in os.listdir(img_dir)]
labels = ['Quadratic_function' if 'Quadratic' in f.split('/')[-1] else 'Linear_function' for f in images]
print labels

data = []
for image in images:
	print "Transforming " + str(image) + "..."
	image = img_to_matrix(image)
	image = flatten_image(image)
	data.append(image)
data = np.array(data)


y = np.where(np.array(labels) == 'Quadratic_function', 1, 0)
print "y is " + str(y)

is_train = np.random.uniform(0, 1, len(data)) <= -1
print "is_train is " + str(is_train)

test_x, test_y = data[is_train == False], y[is_train == False]

svm = joblib.load('model.pkl')
print test_x

pca = RandomizedPCA(n_components=5)


test_x = pca.fit(test_x).transform(test_x)
pred = svm.predict(test_x)
print pd.crosstab(test_y, pred, rownames=['Actual'],colnames=['Predicted'])

