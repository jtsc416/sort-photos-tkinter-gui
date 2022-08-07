from tkinter import *
import tkinter.messagebox as box
import tkinter.filedialog as file
from sortphotos import *
inputfolder= ""
outputfolder= ""

window = Tk()
window.title('SortPhotos.py')
inputframe = Frame(window)
outputframe = Frame(window)
sortframe = Frame(window)
recursiontoggle = IntVar()
recursionvar = False

#the config file has to be created before and configured already, could be for next update

with open ('config.txt', 'r') as f:
    oldlines = f.readlines()
    for line in oldlines:
        if line.startswith('inputfolder'):
            inputfolder = line[14:-2]
        elif line.startswith('outputfolder'):
            outputfolder = line[15:-2]
        elif line.startswith('recursion'):
            recursionvar = line[12:-2]
    if recursionvar == "True":
        recursiontoggle.set(1)

#opens and re-writes config.txt every time a stored variable changes
def storevariable(opening, variable):
    newlines = []
    with open ('config.txt' , 'r') as f:
        oldlines = f.readlines()
        i = 0
        for line in oldlines:
            if line.startswith(opening):
                line = opening + '= \"' + variable + '\"\n'
            i += 1
            newlines.append(line)
    with open ('config.txt' , 'w') as f:
        for line in newlines:
            f.write(line)

def selectinput():
    selected = file.askdirectory(title="Select Input Directory")
    if selected != "":
        global inputfolder
        inputfolder = selected
        inputlabel.config(text='Your input folder is ' + inputfolder)
        storevariable('inputfolder', inputfolder)

def selectoutput():
    selected = file.askdirectory(title="Select Output Directory")
    if selected != "":
        global outputfolder
        outputfolder = selected
        outputlabel.config(text='Your output folder is ' + outputfolder)
        storevariable('outputfolder', outputfolder)

#so far, only recursion option is configurable via gui, other options for future updates
def togglerecursion():
    global recursionvar
    if recursiontoggle.get():
        recursionvar = True
        storevariable('recursion',str(recursionvar))
    elif not recursiontoggle.get():
        recursionvar = False
        storevariable('recursion',str(recursionvar))

def confirmsort():
    if inputfolder == "":
        box.showwarning('No input folder selected','Please select input folder')
    elif outputfolder == "":
        box.showwarning('No output folder selected','Please select output folder')
    elif inputfolder == outputfolder:
        box.showwarning('Recursion Warning','Same folder selected for both input and output')
    elif inputfolder != "" and outputfolder != "":
        print(recursiontoggle.get())
        print(recursionvar)
        var = box.askyesno('Confirm Sort' , 'Sort photos from\n'+inputfolder+'\nto\n'+outputfolder+'?')
        if var == 1:
            box.showinfo('Confirmed','Sorting...')
            sortPhotos(src_dir = inputfolder , dest_dir = outputfolder , sort_format = '%Y/%m-%b' , rename_format = None , recursive = recursionvar, additional_groups_to_ignore=[])
            sortlabel.config(text='Files are sorted!')
        else:
            box.showinfo('Cancelled','Going back...' )

#designing and placing the tkinter graphical elements
inputbtn=Button( inputframe , text = 'Select Input Folder' , command=selectinput)
if inputfolder == "\"\"" :
    inputlabel =Label( inputframe , text= '')
elif inputfolder != "\"\"" :
    inputlabel =Label( inputframe , text= 'Your input folder is ' + inputfolder)
outputbtn=Button( outputframe , text = 'Select Output Folder' , command=selectoutput)
if outputfolder == "\"\"" :
    outputlabel =Label( outputframe , text= '')
elif outputfolder != "\"\"" :
    outputlabel =Label( outputframe , text= 'Your output folder is ' + outputfolder)
sortbtn=Button( sortframe , text = 'Sort Photos' , command=confirmsort)
recursioncheckbtn = Checkbutton(sortframe , text='Sort With Recursion?',variable=recursiontoggle, onvalue= 1, offvalue= 0, command=togglerecursion)
sortlabel=Label( sortframe , text = '')

window.minsize(325, 255)
inputframe.pack()
inputbtn.pack(side=TOP,padx=10,pady=(30,5))
inputlabel.pack(side=TOP, padx=10, pady=5)
outputframe.pack()
outputbtn.pack(side=TOP,padx=10,pady=5)
outputlabel.pack(side=TOP,padx=10,pady=5)
sortframe.pack()
sortbtn.pack(side=TOP,padx=10,pady=5)
recursioncheckbtn.pack(side=TOP,padx=10,pady=5)
sortlabel.pack(side=BOTTOM,padx=10,pady=(5,30))

window.mainloop()