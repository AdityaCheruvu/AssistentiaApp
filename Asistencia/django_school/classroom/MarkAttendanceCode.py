#call(["espeak", "Hello Asistencia"])
from classroom.forms import PostForm
import os
from shutil import rmtree
import subprocess
import face_recognition
import pickle
import cv2
from matplotlib import pyplot as plt
import sqlite3

"""-----------------------------------------"""

#globalVals

#set Raspi IP
raspiIP = "192.168.0.7"

#setTrainingParams

#Set other parameters
raspiPass = "aditya123*"
raspiUser = "pi"
tmpDirRpi="/home/pi/Assistentia/RaspberryPiCode/tmp/"
codeDirRpi="/home/pi/Assistentia/RaspberryPiCode/"
tmpDirLocal= os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp/")
serverPass = "aditya123*"
serverUser = "aditya"
classDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "classes/")
pickleName = "training.pickle"

#sqlitePath
sqlite3Path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3')
"""-----------------------------------------"""

def cropFaceData(pictureDat, locationOfFace):
    lof = locationOfFace
    print(locationOfFace)
    x, y, w, h = locationOfFace
    return pictureDat[y : y+w, x : x+h]

def recognizePeople(data, imgPath):
    image = cv2.imread(imgPath)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    print("[INFO] recognizing faces...")
    boxes = face_recognition.face_locations(rgb, model="hog")
    #blurriness = [(cv2.Laplacian(cropFaceData(image, box),cv2.CV_64F).var()) for box in boxes]
    encodings = face_recognition.face_encodings(rgb, boxes, 1)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["encodings"], encoding, 0.5)
        name = "Unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            name = max(counts, key=counts.get)
        #names[name] = blurryVal
        names.append(name)
    #return names, len(boxes), len(names.keys())
    return names

def subjectCodeOfClass(classToMarkAttendance, prof, cursor):
    subCode = cursor.execute("select SubjectId from classroom_proftosub_mapping where Professor=?", (prof,))
    subCode = subCode.fetchall()
    if(len(subCode) == 0):
        raise Exception("The professor doesnt teach this class!")

def updateInDB(classToMarkAttendance, prof, subCode, cursor):
    pass
    #subCode = cursor.execute("select ")
    #for roll in finalResult:

def takeAttendance(classToMarkAttendance, prof):
    try:
        rmtree(tmpDirLocal)
    except:
        pass
    os.mkdir(tmpDirLocal)
    commandStartSystem = 'sshpass -p ' + '"' + raspiPass + '" ' + "ssh " + raspiUser + "@" + raspiIP + " python3.5 /home/pi/Assistentia/RaspberryPiCode/main.py"
    commandGetImgs = 'sshpass -p ' + '"' + raspiPass + '" ' + "scp " + raspiUser + "@" + raspiIP + ":" + tmpDirRpi + "* " + tmpDirLocal
    process = subprocess.Popen(commandStartSystem, shell=True, stdout=subprocess.PIPE)
    process.wait()
    #if(process.returncode) not successful then alert user that raspi not booted up
    print(process.returncode)
    process = subprocess.Popen(commandGetImgs, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)

    classToMarkAttendance = classToMarkAttendance+"/"
    print("[INFO] loading encodings...")
    data = pickle.loads(open(classDir+classToMarkAttendance+pickleName, "rb").read())
    finalResult = set()
    for i in os.listdir(tmpDirLocal):
        #print(i + " Results: " )
        result = recognizePeople(data, tmpDirLocal+i)
        finalResult.update(set(result))
        #print(result)
    # call update in db
    conn = sqlite3.connect(sqlite3Path)
    cursor = conn.cursor()
    #subId = subjectCodeOfClass(classToMarkAttendance, prof, cursor)
    print("The following are present")
    print(finalResult)
    #print(prof, subId)

    """--------------------------------------------------------"""
    #code to return absentees list
    allStudents = {"15071A05I9", "15071A05N1", "15071A05L9", "15071A05L1", "15071A05I2", "15071A05I1", "15071A05J3"}
    absentees = allStudents - finalResult
    print("abseentees are",absentees)
    return (absentees, list(finalResult))

"""--------------------------------------------------------"""
