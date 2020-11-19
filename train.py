import cv2
import numpy as np
import face_recognition
import os
import sqlite3
import io

class Train:
	def initialize(self):
		def adapt_array(arr):
		    out = io.BytesIO()
		    np.save(out, arr)
		    out.seek(0)
		    return sqlite3.Binary(out.read())

		sqlite3.register_adapter(np.ndarray, adapt_array)

		self.conn = sqlite3.connect('database.sqlite',detect_types=sqlite3.PARSE_DECLTYPES)
		self.cur = self.conn.cursor()

	def findEncodings(self,image):
	    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	    encode=face_recognition.face_encodings(image)[0]
	    return encode


	def insertIntoDatabase(self,studentDetails):
		name=studentDetails['name']
		roll_no=studentDetails['roll_no']
		dob=studentDetails['dob']
		image=cv2.imread(studentDetails['image'])
		face=self.findEncodings(image)
		self.cur.execute('INSERT INTO Class (name,roll_no,dob,encode) VALUES (?,?,?,?)',(name,roll_no,dob,face))
		print("encode complete")
		self.conn.commit()

	def getImage(self,name):
		cap=cv2.VideoCapture(0)
		count=1
		img_name=""
		while count:
			success,img=cap.read()
			if not success:
				print("Can't get frame")
				break

			cv2.imshow('Webcam',img)
			k=cv2.waitKey(1)
			if k%256==32:
				img_name="images/"+name+".jpg"
				cv2.imwrite(img_name,img)
				print("saved")
				count-=1
				cv2.waitKey(250)
				cv2.destroyAllWindows()
		return img_name


	def deleteFromDatabase(self,studentDetails):
		name=studentDetails['name']
		roll_no=studentDetails['roll_no']
		dob=studentDetails['dob']
		self.cur.execute('DELETE FROM Class WHERE (name=? AND roll_no=? AND dob=?)',(name,roll_no,dob))
		self.conn.commit()
		print("DELETED")

	def closeDatabase(self):
		self.cur.close()