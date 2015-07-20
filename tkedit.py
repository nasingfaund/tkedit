#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
tkedit - https://github/lizardfoot/tkedit

'''
import sys, os
from Tkinter import *
import tkMessageBox
import ScrolledText
from tkFileDialog import askopenfilename, asksaveasfilename

def callback():
	tkMessageBox.showinfo("Callback", "Callback")

APPTITLE = "TK Edit"
APPVERSION = "1.0"

class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def set(self, format, *args):
        self.label.config(text=format % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()

class MainWindow:
	
	currentFilename = None

	def __init__(self, master):
		## root options and config
		master.geometry("640x480+100+100")
		master.option_add('*tearOff', FALSE)
		master.title(APPTITLE)
		self.mainwin = master
		## configure menu
		self.buildMenu(master)

		# configure open file dialog options
		self.dialog_options = {}
		self.dialog_options['defaultextension'] = '.txt'
		self.dialog_options['filetypes'] = [('text files', '.txt'),('all files', '.*') ]
		#self.dialog_options['initialdir'] = ''
		#self.dialog_options['initialfile'] = ''
		self.dialog_options['parent'] = master
		self.dialog_options['title'] = APPTITLE

		self.panel = PanedWindow(orient=VERTICAL)
		self.panel.pack(fill=BOTH, expand=1)

		self.textfield = ScrolledText.ScrolledText(master, wrap=WORD,font=("Courier New",10))
		self.panel.add(self.textfield)

		self.status = StatusBar(master)
		self.status.pack(side=BOTTOM, fill=X)


	def buildMenu(self, win):
		# configure menu
		menu = Menu(win)
		win.config(menu=menu)
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.doFileNew)
		filemenu.add_command(label="Open file...", command=self.doFileOpen)
		filemenu.add_command(label="Save file...", command=self.doFileSaveAs)
		filemenu.add_command(label="Save", command=self.doFileSave)
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=win.quit)
		helpmenu = Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About...", command=self.doHelpAbout)


	# callbacks
	def doFileNew(self):
		tkMessageBox.showinfo(APPTITLE, "doFileNew()")

	def doFileOpen(self):
		filename = askopenfilename(**self.dialog_options) 
		if filename:
			self.currentFilename = filename
			self.fileLoad(self.currentFilename)

	def doFileSave(self):
		if self.currentFilename:
			self.fileSave(self.currentFilename)
		else:
			self.doFileSaveAs()

	def doFileSaveAs(self):
		filename = asksaveasfilename(**self.dialog_options) 
		if filename:
			self.currentFilename = filename
			self.fileSave(self.currentFilename)

	def doHelpAbout(self):
		message = "{0} v{1}\nA simple text editor in less than\n200 lines of python code.\nCopyright gtimlin © 2015".format(APPTITLE, APPVERSION)
		tkMessageBox.showinfo(APPTITLE, message)		

	# file handling routines
	def fileLoad(self, filename):		
		self.status.set(filename)
		fi = open(filename, 'r')
		contents = fi.read()
		fi.close()
		self.textfield.delete("0.0", END)
		self.textfield.insert(INSERT,contents)

	def fileSave(self, filename):
		self.status.set(filename)
		fi = open(filename, 'w')
		contents = self.textfield.get(1.0, END)
		fi.write(contents)
		fi.close()
		self.status.set("{0} saved...".format(filename))


def main():
  
	try:	
		root = Tk()
		# icons MUST be in GIF format for this to work
		img = PhotoImage(file='favicon.gif')
		root.tk.call('wm', 'iconphoto', root._w, img)		

		app = MainWindow(root)
		root.mainloop()
	except:
		#print "Can't find icon file."
		print "Error: {0} {1}".format(sys.exc_info()[1], sys.exc_info()[2])

if __name__ == '__main__':
    main()  
