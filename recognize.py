import cv2
import numpy as np
import face_recognition
import os
import sqlite3
import io
from datetime import datetime

class Recognize:

	def initialize(self):
		def convert_array(text):
		    out = io.BytesIO(text)
		    out.seek(0)
		    return np.load(out)


		sqlite3.register_converter("array", convert_array)

		self.conn = sqlite3.connect('database.sqlite',detect_types=sqlite3.PARSE_DECLTYPES)
		self.cur = self.conn.cursor()
	

	def getData(self):
		self.knownPerson=[]
		self.class_name=[]
		self.roll_no=[]
		self.cur.execute('SELECT encode,name,roll_no FROM Class')
		for encode,name,roll_no in self.cur.fetchall():
			self.knownPerson.append(encode)
			self.class_name.append(name)
			self.roll_no.append(roll_no)
		self.cur.close()

	def makeEntryInFile(self,name,roll_no):
		with open('Attendance.csv','r+') as f:
			filePointer=f.readlines()
			namesInList=[]
			for line in filePointer:
				names=line.split(',')[0]
				namesInList.append(names)
			if name not in namesInList:
				time=datetime.now().strftime('%H:%M')
				f.writelines("\n"+name+","+roll_no+","+time)  

	def markAttendance(self):
		cap=cv2.VideoCapture(0)

		while True:
		    success, img=cap.read()
		    imgSmall=cv2.resize(img,(0,0),None,0.25,0.25)
		    imgSmall=cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)
		    frameFaces=face_recognition.face_locations(imgSmall)
		    frameEncode=face_recognition.face_encodings(imgSmall,frameFaces)

		    for faces,encode in zip(frameFaces,frameEncode):
		        matches=face_recognition.compare_faces(self.knownPerson,encode)
		        faceDist=face_recognition.face_distance(self.knownPerson,encode)
		        matchIndex=np.argmin(faceDist)

		        if matches[matchIndex]:
		        	name=self.class_name[matchIndex].upper()
		        	y1,x2,y2,x1=faces
		        	y1,x2,y2,x1=4*y1,4*x2,4*y2,4*x1
		        	self.makeEntryInFile(name,self.roll_no[matchIndex])
		        	cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
		        	cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
		    cv2.imshow('Webcam',img)
		    k=cv2.waitKey(1)
		    if k%256==32:
		    	cv2.waitKey(250)
		    	cv2.destroyAllWindows()
		    	return 0