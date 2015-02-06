import numpy as np
import cv2
import sys
resize_w = 8
resize_h = 8

#Source: http://www.hackerfactor.com/blog/?/archives/432-Looks-Like-It.html

# We define all redeable files
accepted = ['jpg','jpeg', 'png', 'tif','tiff', 'bmp']

def average2D(table2D):
	n = 0
	s = 0
	for i in table2D:
		s += len(i)
		for j in i:
			n += j
	return (n*1.0/s)

def hashTableA(table2D, averageHash):
	for i in xrange(0, len(table2D)):
		for j in xrange(0, len(table2D[i])):
			if (table2D[i][j] > averageHash):
				table2D[i][j] = '1'
			else:
				table2D[i][j] = '0'
	return (table2D)

def hashTableD(table2D):
	for i in xrange(0, len(table2D)):
		for j in xrange(0, len(table2D[i])-1):
			if (table2D[i][j] > table2D[i][j+1]):
				table2D[i][j] = 1
			else:
				table2D[i][j] = 0
	table2D = np.delete(table2D,np.s_[-1:],1)
	return (table2D)

def concatenation(table2D):
	table2D = [ y for x in table2D for y in x]
	table2D = ''.join(str(int(i)) for i in table2D)
	table2D = int(table2D, 2)
	table2D = hex(table2D)
	return table2D[2:-1]

def match(hash1, hash2):
	hex1 = int(hash1, 16)
	hex2 = int(hash2, 16)

	size = len(hash1) if hash1 <= hash2 else len(hash2)
	size *= 4
	similitude = (hex1 ^ hex2)
	similitude = bin(similitude)[2:]
	similitude = similitude.count('0') + size-len(similitude)
	
	percentage = similitude*100.0/size
	return percentage

def aHash(path1,path2):
	# Import images
	img1 = cv2.imread(path1)
	img2 = cv2.imread(path2)

	# Resize them to 8x8
	img1resize = cv2.resize(img1, (resize_w, resize_h)) 
	img2resize = cv2.resize(img2, (resize_w, resize_h)) 

	# Change color to black and white	
	img1resize = cv2.cvtColor( img1resize, cv2.COLOR_BGR2GRAY );
	img2resize = cv2.cvtColor( img2resize, cv2.COLOR_BGR2GRAY );

	# Calculate average color value
	img1average = average2D(img1resize)
	img2average = average2D(img2resize)

	# Hash the image with the average color value
	img1hashed = hashTableA(img1resize, img1average)
	img2hashed = hashTableA(img2resize, img2average)

	# Generage the hash Value
	img1value = concatenation(img1hashed)
	img2value = concatenation(img2hashed)

	# Calculate the match between the two hash (in % )
	matching = match(img1value, img2value)
	print("Method A: " + str(round(matching, 2)) + "% match")


def pHash(path1,path2):
	# Import images
	img1 = cv2.imread(path1)
	img2 = cv2.imread(path2)

	# Resize them to 8x8
	img1resize = cv2.resize(img1, (resize_w, resize_h)) 
	img2resize = cv2.resize(img2, (resize_w, resize_h)) 

	# Change color to black and white	
	img1resize = cv2.cvtColor( img1resize, cv2.COLOR_BGR2GRAY );
	img2resize = cv2.cvtColor( img2resize, cv2.COLOR_BGR2GRAY );

	# Calculate the DCT
	img1dct = cv2.dct(np.float32(img1resize)/255.0)
	img2dct = cv2.dct(np.float32(img2resize)/255.0)

	#Calculate average DCT
	img1avdct = average2D(img1dct)
	img2avdct = average2D(img1dct)

	#Hash the DCT
	img1dcthash = hashTableA(img1dct, img1avdct)
	img2dcthash = hashTableA(img2dct, img2avdct)

	# Generage the hash Value
	img1value = concatenation(img1dcthash)
	img2value = concatenation(img2dcthash)

	# Calculate the match between the two hash (in % )
	matching = match(img1value, img2value)
	print("Method P: " + str(round(matching, 2)) + "% match")
	
	
def dHash(path1,path2):
	# Import images
	img1 = cv2.imread(path1)
	img2 = cv2.imread(path2)

	# Resize them to 9x8
	img1resize = cv2.resize(img1, (resize_w+1, resize_h)) 
	img2resize = cv2.resize(img2, (resize_w+1, resize_h)) 

	# Change color to black and white	
	img1resize = cv2.cvtColor( img1resize, cv2.COLOR_BGR2GRAY );
	img2resize = cv2.cvtColor( img2resize, cv2.COLOR_BGR2GRAY );

	# Hash the image with the average next color value (8x8)
	img1hashed = hashTableD(img1resize)
	img2hashed = hashTableD(img2resize)

	# Generage the hash Value
	img1value = concatenation(img1hashed)
	img2value = concatenation(img2hashed)

	# Calculate the match between the two hash (in % )
	matching = match(img1value, img2value)
	print("Method D: " + str(round(matching, 2)) + "% match")


def errorInput():
	print("Pleaser enter argument as follow : image1, image2, algorithm")
	print('For the algorithm, you may use:')
	print("# 'a', Using the Average Hash algorithm (ahash)")
	print("# 'p' Using the Average Hash Perceptive (phash)")
	print("# 'd' Using the Difference Hash algorithm (dhash)")
	print("# 'all' for using all of the above")
	print("The images format accepted are 'jpg','jpeg', 'png', 'tif','tiff', 'bmp' ")


def main():
	if len(sys.argv) < 3:
		errorInput()
		return

	elif len(sys.argv) == 3:
		arg3 = 'all' # hash algorithm

	elif len(sys.argv) == 4:
		arg3 = sys.argv[3] # hash algorithm

	else:
		errorInput()
		return

	arg1 = sys.argv[1] # Picture 1
	arg2 = sys.argv[2] # Picture 2

	if arg3 == 'a':
		aHash(arg1, arg2)
	elif arg3 == 'p':
		pHash(arg1, arg2)
	elif arg3 == 'd':
		dHash(arg1, arg2)
	elif arg3 == 'all':
		aHash(arg1, arg2)
		pHash(arg1, arg2)
		dHash(arg1, arg2)
	else:
		print "Error in input algorithm argument !"
		errorInput()
		return
	print ("Done !")

main()