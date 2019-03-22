#call(["espeak", "Hello Asistencia"])
from classroom.forms import PostForm
import os
from shutil import rmtree
import subprocess
import face_recognition
import pickle
import cv2
from matplotlib import pyplot as plt
import mysql.connector as sql
from datetime import datetime
"""-----------------------------------------"""

#globalVals

#set Raspi IP
raspiIP = "192.168.0.5"

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

#sqlPath
sqlConn = sql.connect(user="root", database="asistencia", host="localhost", password="toor")
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
    cursor.execute("select distinct SubId from classroom_proftosubmapping where Prof=%s and ClassId=%s", (prof,classToMarkAttendance))
    subId = cursor.fetchall()
    if(len(subId) <= 0):
        raise Exception("The professor doesnt teach this class!")
    elif(len(subId) > 1):
        raise Exception("One professor cannot teach more than one subject for a class")
    print(subId)
    return subId[0][0]

def updateInDB(classToMarkAttendance, prof, subCode, finalSet):
    cursor = sqlConn.cursor()
    today = datetime.date(datetime.now())

def takeAttendance(classToMarkAttendance, prof):
    """try:
        rmtree(tmpDirLocal)
    except:
        pass
    os.mkdir(tmpDirLocal)"""
    commandStartSystem = 'sshpass -p ' + '"' + raspiPass + '" ' + "ssh " + raspiUser + "@" + raspiIP + " python3.5 /home/pi/Assistentia/RaspberryPiCode/main.py"
    commandGetImgs = 'sshpass -p ' + '"' + raspiPass + '" ' + "scp " + raspiUser + "@" + raspiIP + ":" + tmpDirRpi + "* " + tmpDirLocal
    process = subprocess.Popen(commandStartSystem, shell=True, stdout=subprocess.PIPE)
    process.wait()
    #if(process.returncode) not successful then alert user that raspi not booted up
    print(process.returncode)
    process = subprocess.Popen(commandGetImgs, shell=True, stdout=subprocess.PIPE)
    process.wait()
    print(process.returncode)
    print("[INFO] loading encodings...")
    data = pickle.loads(open(os.path.join(os.path.join(classDir,classToMarkAttendance), pickleName), "rb").read())
    finalResult = set()
    for i in os.listdir(tmpDirLocal):
        #print(i + " Results: " )
        result = recognizePeople(data, tmpDirLocal+i)
        finalResult.update(set(result))
        #print(result)
    # call update in db
    conn = sqlConn
    cursor = conn.cursor()
    subId = subjectCodeOfClass(classToMarkAttendance, prof, cursor)
    dataToGetStudentList = (classToMarkAttendance, prof, subId)
    cursor.execute("select distinct RollNo from classroom_proftosubmapping where ClassId=%s and Prof=%s and SubId=%s", dataToGetStudentList)
    studentsOfThisClass = cursor.fetchall()
    cursor.close()
    studentsOfThisClass = set([i[0] for i in studentsOfThisClass])
    finalResult = finalResult - (finalResult - studentsOfThisClass)
    print("The following are present")
    print(finalResult)
    #print(prof, subId)
    #code to return absentees list
    absentees = studentsOfThisClass - finalResult
    print("abseentees are",absentees)
    return [absentees, list(finalResult)]

