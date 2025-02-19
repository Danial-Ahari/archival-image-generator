# Get Tkinter and file and process stuff
from tkinter import *
from tkinter import messagebox
import os
import subprocess

# Make our window
root = Tk()
root.geometry("800x450")
frame = Frame(root)
frame.pack()
clicked = StringVar()
clicked.set("TIFF")

# Make all our GUI objects, named appropriately
L_title = Label(frame, text = "This is the digitization assistant. WARNING: This program will overwrite files. Make sure this is the only program generating the target file.")
L_title.pack()
L_ph = Label(frame)
L_ph.pack()
L_im = Label(frame, text = "Directory with image magick.")
L_im.pack()
T_im = Text(frame, height = 1)
T_im.pack()
L_in = Label(frame, text = "Directory with TIFF or JPG inputs.")
L_in.pack()
T_in = Text(frame, height = 1)
T_in.pack()
pt = IntVar()
C_patt = Checkbutton(frame, text="The above is a file pattern.", variable=pt)
C_patt.pack()
L_it = Label(frame, text = "Input type")
L_it.pack()
D_it = OptionMenu(frame, clicked, *["TIFF", "JPEG"])
D_it.pack()
L_dpi = Label(frame, text = "Output DPI for web copy")
L_dpi.pack()
T_dpi = Text(frame, height = 1)
T_dpi.pack()
L_size = Label(frame, text = "Output Longest Side in Pixels (for example, 150 dpi * 10 inches = 1500 pixels) for web copy")
L_size.pack()
T_size = Text(frame, height = 1)
T_size.pack()
L_pdf = Label(frame, text = "PDF file name:")
L_pdf.pack()
T_pdf = Text(frame, height = 1)
T_pdf.pack()
jp = IntVar()
w = IntVar()
p = IntVar()
C_jpeg = Checkbutton(frame, text="Generate 'altered' JPEGs.", variable=jp)
C_jpeg.pack()
C_web = Checkbutton(frame, text="Generate 'web' JPEGs.", variable=w)
C_web.pack()
C_pdf = Checkbutton(frame, text="Generate PDF (no OCR).", variable=p)
C_pdf.pack()
B_runner = Button(frame, text="Generate files")
B_runner.pack()

# This function makes a jpeg by calling imagemagick on an input TIFF or JPEG and outputting a 100% quality jpeg
def make_jpeg(file, im_dir, in_dir):
	process = subprocess.Popen(im_dir + "magick.exe -quality 100 \"" + in_dir + file + ".tif\" \"" + in_dir + "altered\\" + file + ".jpg\"", shell=TRUE, stdout=subprocess.PIPE)
	process.wait()

# This function makes a web copy from the full DPI JPEG, by using imagemagick to scale it to size pixels at dpi DPI
def make_web(file, im_dir, in_dir, dpi, size):
	process = subprocess.Popen(im_dir + "magick.exe \"" + in_dir + "altered\\" + file + ".jpg\"" + " -density " + dpi + "x" + dpi + " \"" + in_dir + "altered\\" + file + "_web.jpg\"", shell=TRUE, stdout=subprocess.PIPE)
	process.wait()
	width = subprocess.check_output(im_dir + "identify.exe -ping -format %w \"" + in_dir + "altered\\" + file + "_web.jpg\"")
	height = subprocess.check_output(im_dir + "identify.exe -ping -format %h \"" + in_dir + "altered\\" + file + "_web.jpg\"")
	new_width = int(0)
	new_height = int(0)
	if width > height:
		new_width = int(size)
		ratio = new_width/int(width)
		new_height = int(height)*ratio
	else:
		new_height = int(size)
		ratio = new_height/int(height)
		new_width = int(width)*ratio
	process2 = subprocess.Popen(im_dir + "magick.exe \"" + in_dir + "altered\\" + file + "_web.jpg\"" + " -quality 100 -resize " + str(int(new_width)) + "x" + str(int(new_height)) + "! " +  in_dir + "altered\\" + file + "_web.jpg\"", shell=TRUE, stdout=subprocess.PIPE)
	process2.wait()

# This function creates a PDF from all files in our list that end in _web.jpg
def make_pdf(im_dir, in_dir, filename):
	if filename == "":
		process = subprocess.Popen(im_dir + "magick.exe -quality 100 \"" + in_dir + "altered\\" + "*_web.jpg\"" + " \"" + in_dir + "upload\\" + T_pdf.get(1.0, "end-1c") + ".pdf\"", shell=TRUE, stdout=subprocess.PIPE)
		process.wait()
	else:
		process = subprocess.Popen(im_dir + "magick.exe -quality 100 \"" + in_dir + "altered\\" + filename + "*_web.jpg\"" + " \"" + in_dir + "upload\\" + T_pdf.get(1.0, "end-1c") + ".pdf\"", shell=TRUE, stdout=subprocess.PIPE)
		process.wait()

# The main function
def generate(event):
	# Grab imagemagick, and initialize filename
	im_dir = T_im.get(1.0, "end-1c")
	filename = ""
	# Actually get the in_dir and if necesarry, the filename (for file patterns)
	if pt.get() == 0:
		in_dir = T_in.get(1.0, "end-1c")
	else:
		in_dir = os.path.dirname(T_in.get(1.0, "end-1c")) + "\\"
		filename = os.path.basename(T_in.get(1.0, "end-1c"))
	# Get the remainder of our input data.
	dpi = T_dpi.get(1.0, "end-1c")
	size = T_size.get(1.0, "end-1c")
	do_jpeg = jp.get()
	do_web = w.get()
	do_pdf = p.get()
	format = clicked.get()
	# Initialize and generate a files list appropriately
	files = []
	fin_files = []
	if format == "TIFF": # Here, we are using TIFF masters, the nominal way to run this program.
		files = os.listdir(in_dir + "master\\")
		for file in files:
			if pt.get() == 0:
				if file[-4:] == ".tif":
					fin_files.append(file)
			else:
				if file[-4:] == ".tif":
					if file[:len(filename)] == filename:
						fin_files.append(file)
	else:
		if do_jpeg == 0: # Here, we are using JPEGs to generate further images.
			files = os.listdir(in_dir + "altered\\")
			for file in files:
				if pt.get() == 0:
					if file[-4:] == ".jpg" and file[-8:] != "_web.jpg":
						fin_files.append(file)
				else:
					if file[-4:] == ".jpg" and file[-8:] != "_web.jpg":
						if file[:len(filename)] == filename:
							fin_files.append(file)
		else: # Here, we are using JPEG, but we do not have altered files, assume master JPEG files.
			files = os.listdir(in_dir + "master\\")
			for file in files:
				if pt.get() == 0:
					if file[-4:] == ".jpg":
						fin_files.append(file)
				else:
					if file[-4:] == ".jpg":
						if file[:len(filename)] == filename:
							fin_files.append(file)
	# Conditionally perform the actual image generation, after creating folders for the outputs.
	if(do_jpeg == 1): # Make altered directory.
		try:
			os.mkdir(in_dir + "altered\\")
		except FileExistsError:
			print("Altered directory already exists.")
	for file in fin_files: # Get the basename and do JPEG and file web file creation
		basename = file[:-4]
		if(do_jpeg == 1):
			make_jpeg(basename, im_dir, in_dir)
		if(do_web == 1):
			make_web(basename, im_dir, in_dir, dpi, size)
	if(do_pdf == 1): # Do PDF creation
		try:
			os.mkdir(in_dir + "upload\\")
		except FileExistsError:
			print("Upload directory already exists.")
		make_pdf(im_dir, in_dir, filename)
	# We're done.
	messagebox.showinfo("showinfo", "Done!")

# Bind our button to the generate function.
B_runner.bind('<Button-1>', generate)

# Start the window
root.title("Digitization File Generator Assistant")
root.mainloop()
