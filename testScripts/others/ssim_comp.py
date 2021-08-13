from skimage.measure import compare_ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys


if len(sys.argv) < 3:
	print('imgs not provided')
	exit(0)

img_a_fn = sys.argv[1]   #"img_a.jpeg"
img_b_fn = sys.argv[2]   #"img_b.jpeg"

# mean squared error
def mse(img_a, img_b):
	err = np.sum((img_a.astype("float") - img_b.astype("float")) ** 2)
	err/= float(img_a.shape[0] * img_b.shape[1])

	return err

#structure similarity index
def compare_imgs(img_a, img_b):
        return compare_ssim(img_a, img_b)

#peak signal-to-noise-ratio

def plt_imgs(img_a, img_b):
	fig = plt.figure("")

	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(img_a, cmap = plt.cm.gray)
	plt.axis("off")

	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(img_b, cmap = plt.cm.gray)
	plt.axis("off")

	plt.show()


img_a = cv2.imread(img_a_fn)
img_b = cv2.imread(img_b_fn)

img_a_grey = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)
img_b_grey = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)

print(compare_imgs(img_a_grey, img_b_grey))
