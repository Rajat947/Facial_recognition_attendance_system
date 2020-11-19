from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
from os import system
import sqlite3
import io
from train import Train
from recognize import Recognize

class Application():
	def __init__(self):
		#initialize root window with size
		self.root = Tk()
		self.root.title("Facial Attendance System")
		self.root.maxsize(width=990,height=600)
		self.root.minsize(width=990,height=600)

		# Defining and placing background image on root
		pic=ImageTk.PhotoImage(Image.open("face_recognition.png"))
		self.welcome_pic=Label(self.root,image= pic)
		self.welcome_pic.place(x=0,y=0,relwidth=1,relheight=1)

		# setting time to load another window
		self.root.after(100,lambda: self.mainWindow())

		#mainloop of prgram
		self.root.mainloop()

	def viewAttendenceSheet(self):

		#Destroying existng frame and widgets
		self.container.destroy()
		self.mainContent()
		self.background_image.grid_forget()

		#Frame to display attendees
		frame1=Frame(self.container,padx=20,pady=20,bg="#9AB4DE")
		frame1.pack()

		#Heading
		Label(frame1,text="Attendees",font=("Source code variable",20),bg="#9AB4DE").grid(row=0,column=0,columnspan=3)
		
		#row counter
		rowCounter=1
		with open('Attendance.csv','r+') as f:
			filePointer=f.readlines()
			for line in filePointer:
				Detials=line.split(',')
				name=Detials[0].upper()
				roll_no=Detials[1].upper()
				time=Detials[2].upper()
				Label(frame1,text=name,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=0)
				Label(frame1,text=roll_no,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=1)
				Label(frame1,text=time,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=2)
				rowCounter=rowCounter+1
			
			# Displaying label after all attendees
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=0)
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=1)
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=2)


	def insertFunction(self):
		studentDetails=dict()
		
		def  getValue():
			print(studentDetails['image'])
			t1.insertIntoDatabase(studentDetails)
		

		def uploadImage():
			studentDetails['name']=name.get().lower()
			studentDetails['roll_no']=roll_no.get().lower()
			studentDetails['dob']=dob.get().lower()
			studentDetails['image']=filedialog.askopenfilename(title="Upload Image",filetypes=(("png","*.png"),("jpeg","*.jpeg"),("jpg","*.jpg")) )

		def webCamImage():
			studentDetails['name']=name.get().lower()
			studentDetails['roll_no']=roll_no.get().lower()
			studentDetails['dob']=dob.get().lower()
			studentDetails['image']=t1.getImage(studentDetails['name'])
		

		#Destroying existng frame and widgets
		self.container.destroy()
		self.mainContent()
		self.background_image.grid_forget()

		#Heading
		Label(self.container,text="Student Detials",bg="#9AB4DE",width=50,font=("Source code variable",20)).pack()
		
		#Frame for Detials
		frame1=Frame(self.container,padx=20,pady=20,bg="#9AB4DE")
		frame1.pack()

		# Label and entry widget for name
		Label(frame1,text="Name :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=0,column=0)
		name=Entry(frame1,width=20,font=("Source code variable",15))
		name.grid(row=0,column=2)

		# Label and entry widget for Roll no
		Label(frame1,text="Roll no. :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=1,column=0)
		roll_no=Entry(frame1,width=20,font=("Source code variable",15))
		roll_no.grid(row=1,column=2)

		# Label and entry widget for DOB
		Label(frame1,text="DOB :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=2,column=0)
		dob=Entry(frame1,width=20,font=("Source code variable",15))
		dob.grid(row=2,column=2)
		Label(frame1,text="dd/mm/yyyy",padx=10,font=("Source code variable",10),bg="#9AB4DE").grid(row=2,column=3)

		# Label, entry, uplaod button, webcam button widget for Image
		Label(frame1,text="Image :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=3,column=0)
		upload=PhotoImage(file='upload.png')
		uploadBtn=Button(frame1,image=upload,borderwidth=0,bg="#9AB4DE",activebackground="#9AB4DE",highlightbackground="#9AB4DE",command=uploadImage)
		uploadBtn.image=upload
		uploadBtn.grid(row=3,column=2)
		
		Label(frame1,text="OR",font=("Source code variable",15),bg="#9AB4DE").grid(row=4,column=2)

		webCam=PhotoImage(file='web_cam.png')
		webCamBtn=Button(frame1,image=webCam,borderwidth=0,bg="#9AB4DE",activebackground="#9AB4DE",highlightbackground="#9AB4DE",command=webCamImage)
		webCamBtn.image=webCam
		webCamBtn.grid(row=5,column=2)

		#Submit button
		submit=PhotoImage(file='submit.png')
		submitBtn=Button(frame1,image=submit,command=getValue,borderwidth=0,bg="#9AB4DE",activebackground="#9AB4DE",highlightbackground="#9AB4DE")
		submitBtn.image=submit
		submitBtn.grid(row=7,column=1)
	

	def deleteFunction(self):
		studentDetails=dict()
		
		def  getValue():
			studentDetails['name']=name.get().lower()
			studentDetails['roll_no']=roll_no.get().lower()
			studentDetails['dob']=dob.get().lower()
			t1.deleteFromDatabase(studentDetails)
		

		#Destroying existng frame and widgets
		self.container.destroy()
		self.mainContent()
		self.background_image.grid_forget()

		#Heading
		Label(self.container,text="Student Detials",bg="#9AB4DE",width=50,font=("Source code variable",20)).pack()

		#Frame for Detials
		frame1=Frame(self.container,padx=20,pady=20,bg="#9AB4DE")
		frame1.pack()


		# Label and entry widget for name
		Label(frame1,text="Name :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=0,column=0)
		name=Entry(frame1,width=20,font=("Source code variable",15))
		name.grid(row=0,column=2)


		# Label and entry widget for Roll no
		Label(frame1,text="Roll no. :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=1,column=0)
		roll_no=Entry(frame1,width=20,font=("Source code variable",15))
		roll_no.grid(row=1,column=2)
		

		# Label and entry widget for DOB
		Label(frame1,text="DOB :",pady=20,padx=10,font=("Source code variable",15),bg="#9AB4DE").grid(row=2,column=0)
		dob=Entry(frame1,width=20,font=("Source code variable",15))
		dob.grid(row=2,column=2)
		Label(frame1,text="dd/mm/yyyy",padx=10,font=("Source code variable",10),bg="#9AB4DE").grid(row=2,column=3)
		
		# Delete Button
		delete=PhotoImage(file='delete_1.png')
		deleteBtn=Button(frame1,image=delete,command=getValue,borderwidth=0,bg="#9AB4DE",activebackground="#9AB4DE",highlightbackground="#9AB4DE")
		deleteBtn.image=delete
		deleteBtn.grid(row=6,column=1)
	


	def sideMenu(self):
		self.side_menu = Frame(self.root,padx=10,bg="#E6E6E5")
		self.side_menu.pack(side=LEFT,fill=Y)

		def markAttendaneFunction():
			r1.getData()
			r1.markAttendance()

		def viewDbFunction():
			#Destroying existng frame and widgets
			self.container.destroy()
			self.mainContent()
			self.background_image.grid_forget()

			#Frame for content of databases
			frame1=Frame(self.container,padx=20,pady=20,bg="#9AB4DE")
			frame1.pack()
			Label(frame1,text="Students Detials",font=("Source code variable",20),bg="#9AB4DE").grid(row=0,column=0,columnspan=3)
			
			#row counter for content of database
			rowCounter=1

			#Connect with database and read data
			conn = sqlite3.connect('database.sqlite',detect_types=sqlite3.PARSE_DECLTYPES)
			cur =conn.cursor()
			cur.execute('SELECT name,roll_no,dob FROM Class')

			#Display data in frame
			for name,roll_no,dob in cur.fetchall():
				Label(frame1,text=name,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=0)
				Label(frame1,text=dob,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=1)
				Label(frame1,text=roll_no,width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=2)
				rowCounter=rowCounter+1
			
			# Displaying label after data
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=0)
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=1)
			Label(frame1,text=" ",width=23,font=("Source code variable",13),bg="#9AB4DE").grid(row=rowCounter,column=2)
		

		def showSelection(event):
			selection = selected.get().strip()
			selected.set("Update Database")
			if(selection=="Insert"):
				self.insertFunction()
			else:
				self.deleteFunction()

		
		options=["              Insert              ","              Delete              "]
		selected=StringVar()
		selected.set("Update Database")
		updateDbBtn=OptionMenu(self.side_menu,selected,*options,command=showSelection)
		updateDbBtn["borderwidth"]=0
		updateDbBtn.config(bg="black",fg="white",width=20,height=2,indicatoron=0)
		updateDbBtn['menu'].config(bg="grey",font=("Consolas",10))
		updateDbBtn.grid(row=0,column=0,pady=30)

		viewDbBtn = Button(self.side_menu,text="View Database",bg="black",fg="white",width=20,height=2,command=viewDbFunction)
		viewDbBtn.grid(row=1,column=0,pady=30)

		markAttendaneBtn = Button(self.side_menu,text="Mark Attendance",bg="black",fg="white",width=20,height=2,command=markAttendaneFunction)
		markAttendaneBtn.grid(row=2,column=0,pady=30)

		viewSheetBtn = Button(self.side_menu,text="View Attendance Sheet",bg="black",fg="white",width=20,height=2,command=self.viewAttendenceSheet)
		viewSheetBtn.grid(row=3,column=0,pady=30)
	
	def mainContent(self):
		self.container=Frame(self.root,bg="#9AB4DE")
		self.container.pack(side=LEFT,fill='both')
		pic=ImageTk.PhotoImage(Image.open("home_page.png"))
		self.background_image=Label(self.container,image=pic)
		self.background_image.image = pic
		self.background_image.grid(column=0,row=0)
	
	def mainWindow(self):
		# Destroying background image and button to place new things
		self.welcome_pic.place_forget()

		#Adding top bar to mainWindow
		self.top_bar = Frame(self.root,bg="#3A83C4")
		self.top_bar.pack(side=TOP,fill=X)
		Label(self.top_bar,text="FACIAL RECOGNITION ATTENDANCE SYSTEM",fg="#9AB4DE",bg="#3A83C4",font=("Consolas",30)).pack()

		#Adding side menu to mainWindow
		self.sideMenu()
		
		#Addind center content
		self.mainContent()

t1=Train()
t1.initialize()
r1=Recognize()
r1.initialize()
app = Application()