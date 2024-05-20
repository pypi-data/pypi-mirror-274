def idp():

    print("""
    
    ## Libraries
import matplotlib.pyplot as plt
import numpy as np
import cv2
%matplotlib inline


##
# use matplotlib to show opencv pic
def matshow(title='image',image=None,gray=False):
 	if isinstance(image,np.ndarray):
 		if len(image.shape) ==2:
 			pass
 		elif gray == True:
 			# transfer color space to gray in opencv
 			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 		else:
		# transfer color space to RGB in openc
 		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
 	plt.figure()
 	plt.imshow(image,cmap='gray')

 	plt.axis('off') 
 	plt.title(title) # title
 	plt.show()

## Image reading and display
im = cv2.imread(r"lena.png",1)
matshow("test",im)
 
# Image storage
cv2.imwrite('lena.jpg', im)

## Color space conversion
img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

## Translation
def translate(img, x, y):
 	# Obtain the image size.
 	(h, w) = img.shape[:2]

 	# Define the translation matrix.
 	M = np.float32([[1, 0, x], [0, 1, y]])

 	shifted = cv2.warpAffine(img, M, (w, h))

 	return shifted
shifted = translate(im, 0, 50)


# Define the rotate function.
def rotate(img, angle, center=None, scale=1.0):
	# Obtain the image size.
 	(h, w) = img.shape[:2]
 	# The missing value of the rotation center is the image center.
 	if center is None:
 		center = (w / 2, h / 2)
 	# Invoke the function of calculating the rotation matrix.
 	M = cv2.getRotationMatrix2D(center, angle, scale)
 	rotated = cv2.warpAffine(img, M, (w, h))
 	# Return the rotated image.
 	return rotated

rotated = rotate(im, 45)

## Mirrowing
im_flip0 = cv2.flip(im, 0)
im_flip1 = cv2.flip(im, 1)


# Zooming.
resized = cv2.resize(im, dst_size, interpolation = method)


## Gray Transformation

def linear_trans(img, k, b=0):
 	trans_list = [(np.float32(x)*k+b) for x in range(256)]
 	trans_table =np.array(trans_list)
 	trans_table[trans_table>255] = 255
 	trans_table[trans_table<0] = 0
 	trans_table = np.round(trans_table).astype(np.uint8)
 	return cv2.LUT(img, trans_table)

im_inversion = linear_trans(im, -1, 255) # Inversion.
im_stretch = linear_trans(im, 1.2) # Grayscale stretch.
im_compress = linear_trans(im, 0.8) # Grayscale compression.

def gamma_trans(img, gamma):
	gamma_list = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]
	gamma_table = np.round(np.array(gamma_list)).astype(np.uint8)
	return cv2.LUT(img, gamma_table)

im_gama05 = gamma_trans(im, 0.5)

## Histogram Plot
plt.hist(im.ravel(), 256, [0,256])

## Histogram Equalization
im_equ1 = cv2.equalizeHist(im)

## Filtering
im_medianblur = cv2.medianBlur(im, 5)

## Mean Filtering
im_meanblur1 = cv2.blur(im, (3, 3))
    
    """)