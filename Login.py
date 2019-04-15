from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from subprocess import call

with sqlite3.connect('quit.db') as db:
	c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL ,password TEX NOT NULL);')
db.commit()
db.close()

# main Class


class main:
	def __init__(self, master):
		# Window
		self.master = master
		# Some Usefull variables
		self.username = StringVar()
		self.password = StringVar()
		self.n_username = StringVar()
		self.n_password = StringVar()
		# Create Widgets
		self.widgets()

	# Login Function
	def login(self):
		# Establish Connection
		with sqlite3.connect('quit.db') as db:
			c = db.cursor()

		#Find user If there is any take proper action
		find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
		c.execute(find_user,[(self.username.get()),(self.password.get())])
		result = c.fetchall()
		if result:
			root.destroy()
			call(["python", "GUI.py"])

		else:
			ms.showerror('Oops!', 'Username Not Found.')

	def new_user(self):
		# Establish Connection
		with sqlite3.connect('quit.db') as db:
			c = db.cursor()

		# Find Existing username if any take proper action
		find_user = ('SELECT * FROM user WHERE username = ?')
		c.execute(find_user, [(self.username.get())])
		if c.fetchall():
			ms.showerror('Error!', 'Username Taken Try a Diffrent One.')
		else:
			ms.showinfo('Success!', 'Account Created!')
			self.log()
		# Create New Account
		insert = 'INSERT INTO user(username,password) VALUES(?,?)'
		c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
		db.commit()

	# Frame Packing Methords
	def log(self):
		self.username.set('')
		self.password.set('')
		self.crf.pack_forget()
		self.head['text'] = 'LOGIN'
		self.logf.pack()

	def cr(self):
		self.n_username.set('')
		self.n_password.set('')
		self.logf.pack_forget()
		self.head['text'] = 'Create Account'
		self.crf.pack()



	# Draw Widgets
	def widgets(self):
		def on_e1_click(event):
			if e1.get() == 'Enter your Username':
				e1.delete(0, "end")
				# delete all the text in the e1
				e1.insert(0, '')
				# Insert blank for user input
				e1.config(fg='black')

		def on_focusout(event):
			if e1.get() == '':
				e1.insert(0, 'Enter your Username')
				e1.config(fg='grey')

		def on_focusout_e2(event):
			if e2.get() == '':
				e2.insert(0, '*****')
				e2.config(fg='grey')

		def on_e2_click(event):
			if e2.get() == '*****':
				e2.delete(0, "end") # delete all the text in the e1
				e2.insert(0, '') #Insert blank for user input
				e2.config(fg='black')

		self.head = Label(self.master, text = 'LOGIN', font = ('', 35), pady = 10)
		self.head.pack()
		self.logf = Frame(self.master, padx =10, pady = 10)
		Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
		e1 = Entry(self.logf, textvariable = self.username, bd = 5, font = ('',15))
		e1.grid(row=0, column=1)
		e1.insert(0, "Enter your Username")
		e1.config(fg='grey')
		e1.bind('<FocusIn>', on_e1_click)
		e1.bind('<FocusOut>', on_focusout)
		Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
		e2 = Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15), show = '*')
		e2.grid(row=1,column=1)
		e2.insert(0, "*****")
		e2.config(fg='grey')
		e2.bind('<FocusIn>', on_e2_click)
		e2.bind('<FocusOut>', on_focusout_e2)
		Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid(row = 2, column = 1)
		Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=2)
		self.logf.pack()
		self.crf = Frame(self.master,padx =10,pady = 10)
		Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
		Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
		Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
		Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
		Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
		Button(self.crf,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=2,column=1)

# create window and application object


root = Tk()
#root.state('zoomed')
root.title("Login")
main(root)
root.mainloop()
