#-*- coding: utf-8 -*-
#setup a standard image size; this will distort some images but will get everything into the same shape

import os
from PIL import Image
from PIL import ImageOps
import numpy as np
import pylab as pl
import pandas as pd
from sklearn.decomposition import RandomizedPCA
from sklearn.externals import joblib
from sklearn.svm import LinearSVC


STANDARD_SIZE = (300, 167)
def img_to_matrix(filename, verbose=False):
	"""
	take a filename and turns it into a numpy array of RGB pixels
	array([[255,255,255],
		   [255,255,250],
		   [250,250,250],
		   ...,])
	"""
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

#-*- main -*-

img_dir = "images/"
images = [img_dir + r for r in os.listdir(img_dir)]
labels = ['Quadratic_function' if 'Quadratic' in f.split('/')[-1] else 'Linear_function' for f in images]

data = []
for image in images:
	if 'DS_Store' in image:
		continue
	print image
	img = img_to_matrix(image) #行列化
	img = flatten_image(img)   #平坦化
	data.append(img)           #追加

data = np.array(data)
print "data: " + str(data)

is_train = np.random.uniform(0, 1, len(data)) <= 0.7
y = np.where(np.array(labels) == 'Quadratic_function', 1, 0)
print "y is " + str(y)

train_x, train_y = data[is_train], y[is_train]

#２次元プロット
pca = RandomizedPCA(n_components=2)
X = pca.fit_transform(data)
df = pd.DataFrame({"x": X[:, 0], "y": X[: ,1], "label": np.where(y==1, 'Quadratic_function','Linear_function')})
colors = ['red', 'yellow']
for label, color in zip(df['label'].unique(), colors):
	mask = df['label'] == label
	pl.scatter(df[mask]['x'], df[mask]['y'], c=color, label=label)

pl.legend()
pl.savefig('pca_feature.png')

#クラス分類訓練
pca = RandomizedPCA(n_components=5) # => 最初は5だったんだけど、２でもいいんじゃないかと思って変えてみた
print "train_x: " + str(train_x)
train_x = pca.fit_transform(train_x)

svm = LinearSVC(C=1.0)
svm.fit(train_x, train_y)
joblib.dump(svm, 'model.pkl')

#モデル評価
test_x, test_y = data[is_train == False], y[is_train == False]
print "data[is_train == false]: " + str(data[is_train == False])
print "y[is_train == False]: " + str(y[is_train == False])
print "before: " + str(test_x)
print "after:  " + str(pca.transform(test_x))
test_x = pca.transform(test_x)
print pd.crosstab(test_y, svm.predict(test_x),rownames=['Actual'],colnames=['Predicted'])



