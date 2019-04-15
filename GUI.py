from subprocess import call
import webbrowser as wb
from tkinter import *
from tkinter import messagebox

import re

window = Tk()
#window.state('zoomed')

def change_dropdown(*args):
	if tkvar.get() == 'Select from drop down':
		messagebox.showinfo("Error", "Please Select your search criteria handle ")
	else:
		lable_text = "Enter your " + tkvar.get()
		lable1.config(text = lable_text )
		e1.delete(0, "end")
		e1.insert(0, lable_text)


def on_e1_click(event):
	if e1.get() == 'Enter your Search String' or e1.get()=='#enter your Select from drop down' or e1.get() == '#Enter your twitter handle' or e1.get() == 'Enter your Twitter Handle' or e1.get() == 'Enter your Hastag' or e1.get() == "#enter your":
		e1.delete(0, "end") # delete all the text in the e1
		e1.insert(0, '') #Insert blank for user input
		e1.config(fg='black')

def on_e2_click(event):
	if e2.get() == 'Description for the handle':
		e2.delete(0, "end") # delete all the text in the e1
		e2.insert(0, '') #Insert blank for user input
		e2.config(fg='black')

def on_focusout(event):
	if e1.get() == '':
		e1.insert(0, '#enter your ' + tkvar.get() )
		e1.config(fg='grey')

def on_focusout_e2(event):
	if e2.get() == '':
		e2.insert(0, 'Description for the handle')
		e2.config(fg='grey')

def on_e3_click(event):
	if e3.get() == '#Enter number of tweets to search for (less than 18000)':
		e3.delete(0, "end") # delete all the text in the e1
		e3.insert(0, '') #Insert blank for user input
		e3.config(fg='black')
def on_focusout_e3(event):
	if e3.get() == '':
		e3.insert(0, '#Enter number of tweets to search for (less than 18000)')
		e3.config(fg='grey')




def write_to_file():
	flag = "1"
	TSN = e3.get()
	input1 = e1.get()
	x = bool((re.search(' +', input1)))
	if input1 == "" or input1 ==  'Enter your Hastag' or input1=='Enter your Twitter Handle' or input1=='#enter your Select from drop down' or input1 == 'Enter your Search String' or input1 == '#Enter your twitter handle':
		messagebox.showinfo("Error", "Please re-enter tweeter handle ")
		e1.config(fg='red')
		flag = "0"
	else:
		flag = "1"
	if TSN == "#Enter number of tweets to search for" or bool(re.match('^[0-9]+$', TSN)) == False or int(TSN) > 18000:
		messagebox.showinfo("Error", "Number of tweets to search should be number and less than 18000")
		e3.config(fg='red')
		flag = "0"
	if flag == "1":
		d = {"Twitter_Handle": e1.get(), "Description": e2.get(), "Number of tweets": e3.get()}
		file = open("vals.txt", "w+")
		D1 = e1.get() + ',' + e3.get()
		file.write(D1)

		file1 = open("history", "a+")
		file1.write(str(d)+ "\n")
		file.close()
		file1.close()
		print("fetching your tweets plz wait...")
		



		call(["Rscript", "Authentication.R", "outcat", "script.Rout"])

		new_winF()

		i =1
		while i<1:
			wb.open_new(r'rplot.pdf')
			i -= 1


def new_winF():

	window.destroy()
	call(["python", "output.py"])



	e1.delete(0, "end")
	e1.insert(0, '#Enter your twitter handle')
	e1.config(fg='grey')

	e3.delete(0, "end")
	e3.insert(0, '#Enter number of tweets to search for (less than 18000)')
	e3.config(fg='grey')

	e2.delete(0, "end")
	e2.insert(0, 'Description for the handle')
	e2.config(fg='grey')

# lable 1
lable1 = Label(window, text="Twitter Handle:", font=("Helvetica", 16))
lable1.grid(row = 2, column=0)
e1 = Entry(window, bd=3, width=45, font=("Helvetica", 14))
e1.insert(0, '#Enter your twitter handle')
e1.grid(row = 2, column=1)
e1.bind('<FocusIn>', on_e1_click)
e1.bind('<FocusOut>', on_focusout)
e1.config(fg='grey')


# lable 3
lable3 = Label(window, text="Number of Tweets to scan:", font=("Helvetica", 16))
lable3.grid(row = 3, column=0)
e3 = Entry(window, bd=3, width=45, font=("Helvetica", 14))
e3.insert(0, '#Enter number of tweets to search for (less than 18000)')
e3.grid(row = 3, column=1)
e3.bind('<FocusIn>', on_e3_click)
e3.bind('<FocusOut>', on_focusout_e3)
e3.config(fg='grey')


# lable 3
lable2 = Label(window, text="Description:", font=("Helvetica", 16))
lable2.grid(row = 4, column=0)
e2 = Entry(window, bd=3, width=45, font=("Helvetica", 14))
e2.insert(0, 'Description for the handle')
e2.bind('<FocusIn>', on_e2_click)
e2.bind('<FocusOut>', on_focusout_e2)
e2.config(fg='grey')
e2.grid(row = 4, column=1)


# submit button
b1 = Button(window, text="Execute", font=("Helvetica", 16), command=write_to_file, width=10)
b1.grid(row = 5, column=1)



# Create a Tkinter variable
tkvar = StringVar(window)

# Dictionary with options
choices = {'Select from drop down', 'Twitter Handle', 'Hastag', 'Search String'}
tkvar.set('Select from drop down')

popupMenu = OptionMenu(window, tkvar, *choices)
choice1 = Label(window, text="Select search criteria" ,bd=3, width=25, font=("Helvetica", 16))
choice1.grid(row = 1, column = 0)
popupMenu.grid(row = 1, column =1)

tkvar.trace('w', change_dropdown)


window.title('Product And Market Sentiment Analysis')
window.mainloop()


