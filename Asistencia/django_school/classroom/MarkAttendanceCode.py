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
import traceback
"""-----------------------------------------"""

#globalVals

#set Raspi IP
raspiIP = "192.168.0.6"

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

def updateInDB(classToMarkAttendance, prof, finalSet):
    cursor = sqlConn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    SubId = subjectCodeOfClass(classToMarkAttendance, prof, cursor)
    print("------")
    try:
        #Update in Cumulative Total table
        try:
            print(str(1))
            data = (classToMarkAttendance, SubId, 1)
            cursor.execute("insert into classroom_cumulativeattendancetotal(ClassId, SubId, Total) values(%s, %s, %s)", data)
            
        except:
            print(str(2))
            data = (classToMarkAttendance, SubId)
            cursor.execute("update classroom_cumulativeattendancetotal set Total=Total+1 where ClassId=%s and SubId=%s", data)
            
        #Update in Daily Total table
        try:
            print(str(3))
            data = (classToMarkAttendance, today, SubId, 1)
            cursor.execute("insert into classroom_dailyattendancetotal(ClassId, Date_c, SubId, Total) values(%s, %s, %s, %s)", data)
            
        except:
            print(str(4))
            data = (classToMarkAttendance, SubId, today)
            cursor.execute("update classroom_dailyattendancetotal set Total=Total+1 where ClassId=%s and SubId=%s and Date_c=%s", data)
            
        #Update Cumulative table
        for roll in finalSet:
            try:
                print(str(5))
                data = (roll, SubId, 1)
                cursor.execute("insert into classroom_cumulativeattendance(RollNo, SubId, Attended) values(%s, %s, %s)", data)
                
            except:
                print(str(6))
                data = (roll, SubId)
                cursor.execute("update classroom_cumulativeattendance set Attended=Attended+1 where RollNo=%s and SubId=%s", data)
                
        #Update Daily table
        for roll in finalSet:
            try:
                print(str(7))
                data = (roll, today, SubId, 1)
                cursor.execute("insert into classroom_dailyattendance(RollNo, Date_c, SubId, Attended) values(%s, %s, %s, %s)", data)
                
            except:
                print(str(8))
                data = (roll, SubId, today)
                cursor.execute("update classroom_dailyattendance set Attended=Attended+1 where RollNo=%s and SubId=%s and Date_c=%s", data)
                
        sqlConn.commit()
        print("Marked in DB successfully!")
    except Exception as e:
        print(e)
        traceback.print_exc()
        sqlConn.rollback()
        print("An Error occured and insertion was not possible, please try again!")

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

