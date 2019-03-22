from imutils import paths
from globalVals import *
import face_recognition
import argparse
import pickle
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to directory of dataset for a class")

ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="Detection method to find faces. hog is enough for single faces")
args = vars(ap.parse_args())
classDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classes/")
try:
	os.mkdir(os.path.join(classDir, os.path.basename(os.path.dirname(args["dataset"]))))
except:
	pass
imagePaths = list(paths.list_images(args["dataset"]))
targetDirForEncodings = os.path.join(classDir, os.path.basename(os.path.dirname(args["dataset"])))
encodingsFile = "training.pickle"
knownEncodings = []
knownNames = []

for (i, imagePath) in enumerate(imagePaths):
	print("[INFO] training on image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]
	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	boxes = face_recognition.face_locations(rgb, model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes, 2)

	for encoding in encodings:
		knownEncodings.append(encoding)
		knownNames.append(name)

print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(os.path.join(targetDirForEncodings, encodingsFile), "wb")
f.write(pickle.dumps(data))
f.close()
