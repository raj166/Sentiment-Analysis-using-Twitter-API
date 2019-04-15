from tkinter import *
import webbrowser as wb
import subprocess as sp
from subprocess import call

window = Tk()



def open_csv_in_excel():
	wb.open_new(r'tweet_sentiment.csv')

def open_history():
	#wb.open_new(r"history")
	programName = "notepad.exe"
	fileName = "history"
	sp.Popen([programName, fileName])


def open_pdf():
	wb.open_new(r"sentiment_histogram.pdf")
	wb.open_new(r"sentiment_barplot.pdf")
	wb.open_new(r"Wordcloud.pdf")
	wb.open_new(r"SentimentAnalysis.pdf")

def new_search():
	window.destroy()
	call(["python", "GUI.py"])

def quit():
	window.destroy()

B1  = Button(window, text="Open output in Excel", font=("Helvetica", 16), command=open_csv_in_excel ,width = 25)
B1.grid(columnspan= 12, rowspan = 12, padx = 10 , pady = 10)

B2  = Button(window, text="Open Search History", font=("Helvetica", 16), command=open_history ,width = 25 )
B2.grid(columnspan= 12, rowspan = 12, padx = 10 , pady = 10)

B3  = Button(window, text="Open Output Graphs", font=("Helvetica", 16), command=open_pdf ,width = 25 )
B3.grid(columnspan= 12, rowspan = 12, padx = 10 , pady = 10)

B4  = Button(window, text="Search Again", font=("Helvetica", 16), command=new_search ,width = 25 )
B4.grid(columnspan= 12, rowspan = 12, padx = 10 , pady = 10)

B  = Button(window, text="Exit", font=("Helvetica", 16), command=quit ,width = 25)
B.grid(columnspan= 12, rowspan = 12, padx = 10 , pady = 10)



window.title('Output')
window.mainloop()
