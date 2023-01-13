#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
A simple text editor written in Python 
Geno Timlin 2015
nasingfaund 2023
'''
import sys, os
###import tkinter as tk
from tkinter import messagebox, Tk, Frame, Label, simpledialog, FALSE, Menu, PanedWindow, VERTICAL, BOTH, scrolledtext, WORD, SUNKEN, W, X, BOTTOM, LEFT, StringVar, OptionMenu, END, INSERT
###from tkinter import Tk
###import tkMessageBox

###from tkinter.Messagebox import Messagebox
###import ScrolledText
###from tkFileDialog import askopenfilename, asksaveasfilename
from tkinter.filedialog import askopenfilename, asksaveasfilename
###import tkSimpleDialog
import json
from os.path import expanduser

def callback():
	messagebox.showinfo("Callback", "Callback")

APPTITLE = "TK Editor"
APPVERSION = "1.0"

g_window_config = None


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

class WindowConfig:
	font = None
	font_size = None
	foreground = None
	background = None

	def __init__(self, font = "Courier New", font_size = 10, foreground = "Blue", background = "White"):
		#print "WindowConfig()"
		self.font = font
		self.font_size = font_size
		self.foreground = foreground
		self.background = background

	def __str__(self):
		return "{ font : '%s', font_size : %s, foreground : '%s', background : '%s' }" % (self.font, self.font_size, self.foreground, self.background)



class OptionsDialog(simpledialog.Dialog):
	parent = None	
	opt_font = None
	opt_font_size = None
	opt_foreground = None
	opt_background = None
	
	selected_font = None
	selected_font_size = None
	selected_foreground = None
	selected_background = None

	def __init(self, master, title):
		#print "OptionsDialog()"
		self.parent = master
		self.title(title)		


	def body(self, master):		
		global g_window_config
		# label and dropdown for Font
		Label(master, text="Font", justify=LEFT).grid(row=0)
		self.opt_font = StringVar(master)
		self.opt_font.set(g_window_config.font) # default value
		self.select_font = OptionMenu(master, self.opt_font, "Courier New", "Helvetica", "Sans Serif")
		self.select_font.grid(row=0, column=1)

		# label and dropdown for Font Size
		Label(master, text="Font", justify=LEFT).grid(row=1)
		self.opt_font_size = StringVar(master)
		self.opt_font_size.set(g_window_config.font_size) # default value
		self.select_font_size = OptionMenu(master, self.opt_font_size, 8, 9, 10, 11, 12)
		self.select_font_size.grid(row=1, column=1)

		# label and dropdown for Foreground color
		Label(master, text="Foreground", justify=LEFT).grid(row=2)
		self.opt_foreground = StringVar(master)
		self.opt_foreground.set(g_window_config.foreground) # default value
		self.select_foreground = OptionMenu(master, self.opt_foreground, "Black", "Blue", "Green", "Red","White", "Yellow")
		self.select_foreground.grid(row=2, column=1)

		# label and dropdown for Background color
		Label(master, text="Background", justify=LEFT).grid(row=3)
		self.opt_background = StringVar(master)
		self.opt_background.set(g_window_config.background) # default value
		self.select_background = OptionMenu(master, self.opt_background, "Black", "Blue", "Green", "Red","White", "Yellow")
		self.select_background.grid(row=3, column=1)


	def apply(self):
		global g_window_config
		g_window_config.font = self.opt_font.get()
		g_window_config.font_size = self.opt_font_size.get()
		g_window_config.foreground = self.opt_foreground.get()
		g_window_config.background = self.opt_background.get()
		#print "OptionsDialog\tconfig: %s" % (g_window_config)

	def get_font(self):
		return self.selected_font

	def get_font_size(self):
		return self.selected_font_size

	def get_foreground(self):
		return self.selected_foreground

	def get_background(self):
		return self.selected_foreground


class MainWindow:
	
	currentFilename = None
	mainwin = None
	config = None

	def __init__(self, master):
		global g_window_config
		## root options and config
		master.geometry("640x480+100+100")
		master.option_add('*tearOff', FALSE)
		master.title(APPTITLE)
		self.mainwin = master
		self.config = WindowConfig()
		#print "MainWindow - self.config.font: %s" % (g_window_config.font)

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

		self.textfield = scrolledtext.ScrolledText(master, wrap=WORD,
			 font=(g_window_config.font, g_window_config.font_size), 
			 fg = g_window_config.foreground, bg = g_window_config.background )
		self.panel.add(self.textfield)

		self.status = StatusBar(master)
		self.status.pack(side=BOTTOM, fill=X)

		#self.mainwin.bind('<Control-n>', self.doFileNew)  
		self.mainwin.bind('<Control-o>', self.keyEventFileOpen)  
		self.mainwin.bind('<Control-s>', self.keyEventFileSave)  

	def buildMenu(self, win):
		# configure menu
		menu = Menu(win)
		win.config(menu=menu)
		filemenu = Menu(menu)
		menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", command=self.doFileNew)
		filemenu.add_command(label="Open file...", command=self.doFileOpen, accelerator='Ctrl+o')
		filemenu.add_command(label="Save file...", command=self.doFileSaveAs)
		filemenu.add_command(label="Save", command=self.doFileSave, accelerator='Ctrl+s')
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command=win.quit)

		editmenu = Menu(menu)
		menu.add_cascade(label="Edit", menu=editmenu)
		editmenu.add_command(label="Preferences", command=self.doEditPreferences)

		helpmenu = Menu(menu)
		menu.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About...", command=self.doHelpAbout)


	# callbacks
	def doFileNew(self):
		messagebox.showinfo(APPTITLE, "doFileNew()")

	def doFileOpen(self):
		filename = askopenfilename(**self.dialog_options) 
		if filename:
			self.currentFilename = filename
			self.fileLoad(self.currentFilename)

	def keyEventFileOpen(self, event):
		self.doFileOpen()

	def doFileSave(self):
		self.fileSave(self.currentFilename)

	def keyEventFileSave(self, event):
		self.doFileSave()

	def doFileSaveAs(self):
		filename = asksaveasfilename(**self.dialog_options) 
		if filename:
			self.currentFilename = filename
			self.fileSave(self.currentFilename)
	
	def doEditPreferences(self):
		global g_window_config
		# show the dialog window
		dlg = OptionsDialog(self.mainwin, "Preferences")
		#print "MainWindow\tconfig: %s" % (g_window_config)
		# set the text options
		self.textfield.config(font=(g_window_config.font, g_window_config.font_size), 
			 fg = g_window_config.foreground, bg = g_window_config.background, 
			 insertbackground = g_window_config.foreground )


	def doHelpAbout(self):
		message = "{0} v{1}\nThis is a little program.\nCopyright © 2015".format(APPTITLE, APPVERSION)
		messagebox.showinfo(APPTITLE, message)		

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


def load_config():	
	global g_window_config
	g_window_config = WindowConfig()
	try:
		home_dir = expanduser("~")
		filename = "%s/.tkedit.cfg" % (home_dir)
		#print "load_config.filename: %s" % (filename)
		if os.path.isfile(filename):
			data = {}
			with open(filename) as config_file:
				for line in config_file:
					line.strip()
					tmp = line.strip().split("=")
					data[tmp[0]] = tmp[1]
			g_window_config.font = data['font']
			g_window_config.font_size = data['font_size']
			g_window_config.foreground = data['foreground']
			g_window_config.background = data['background']
			#print g_window_config

	except:
		print ("Error: {0} {1}".format(sys.exc_info()[1], sys.exc_info()[2]))

def save_config():
	global g_window_config
	try:
		home_dir = expanduser("~")
		filename = "%s/.tkedit.cfg" % (home_dir)
		#print "save_config.filename: %s" % (filename)
		with open(filename, 'w') as config_file:
			config_file.write("font=%s\n" % (g_window_config.font))
			config_file.write("font_size=%s\n" % (g_window_config.font_size))
			config_file.write("foreground=%s\n" % (g_window_config.foreground))
			config_file.write("background=%s\n" % (g_window_config.background))
			config_file.close()
	except:
		print ("Error: {0} {1}".format(sys.exc_info()[1], sys.exc_info()[2]))

def main():
    global g_window_config
    try:
        # load the window config
        load_config()
        root=Tk()
        # icons MUST be in GIF format for this to work
        ###img = PhotoImage(file='favicon.gif')
        ###root.tk.call('wm', 'iconphoto', root._w, img)
		# show the main window
        app = MainWindow(root)
        root.mainloop()
		# save the window config
        save_config()

    except:
        print ("Error: {0} {1}".format(sys.exc_info()[1], sys.exc_info()[2]))

if __name__ == '__main__':
    main() 
