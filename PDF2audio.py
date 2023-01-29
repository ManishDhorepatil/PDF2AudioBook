from multiprocessing.sharedctypes import Value
from click import progressbar
from matplotlib.pyplot import text
from pdf2image import convert_from_path
import pytesseract
import cv2
from gtts import gTTS
import os
from pdf2image import convert_from_path
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import time
from tkinter import ttk
from tkinter.filedialog import FileDialog, asksaveasfile
from tkinter import messagebox
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# To  Create a window

root=Tk()
root.title('PDF to AudioBook')
root.geometry("670x500+100+200")
root.config(bg="white")



## Backgroung image

img = PhotoImage(file="thor2.png")
label = Label(root,image=img)
label.place(x=-530, y=-750,)

# processbar
processbar = ttk.Progressbar(root, orient=HORIZONTAL, length=500, mode='determinate')
downloadbar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')

# Function for Open the PDF file

def openfile():
    filepath=filedialog.askopenfilename(initialdir="C:/",title="Select PDF",filetype=(("pdf file","*.pdf"),))


    label_file.configure(text=filepath)
    
    try:
        filetxt='alltext.txt'
        os.remove(filetxt)
        
    except:
        pass    
    


        
    print(filepath)
    return filepath


# this function convert pdf to Audio 

def convert():
    processbar['value'] = 0
    start = time.time()
    filepath = openfile()
    
    
    images = convert_from_path(filepath,500,poppler_path=r'C:\Program Files\poppler-22.01.0\Library\bin')

    #Extraction of images from PDF
    
    for i in range(len(images)):
        root.update_idletasks()
        processbar['value'] += 16
        time.sleep(1)
        
        
        # Save pages as images from the pdf
        images[i].save('page'+ str(i) +'.jpg', 'JPEG') 
        print("image extraction.........")
        print("No of Pages is -",i)

        
        
        
        
    
    # TEXT Extraction Phase
    
    for x in range(i+1):

        print("Working page No -",x)
        root.update_idletasks()
        processbar['value'] += 16
        time.sleep(1)

        #Selected image convert RGB to Grey
        
        image = cv2.imread('page'+ str(x) +'.jpg')
        ret,thresh1 = cv2.threshold(image,120,255,cv2.THRESH_BINARY)
    
        # Extracted text save in text.txt file 
        text= str(pytesseract.image_to_string(thresh1, config='--psm 6'))
        txtfile = open("alltext.txt","a")
        txtfile.writelines(text)
        txtfile.close()

        
        
        
    print("text file created")
    processbar['value'] = 100
    end = time.time()
    print(("total time is first"), end-start)
    messagebox.showinfo("Information","File ready for Download")



# Now Conert TEXT into AUDIO and Download function

def save():
    
    try:
        downloadbar['value'] = 0
        root.update_idletasks()
        downloadbar['value'] += 16
        time.sleep(1)

        #Convert text to Audio and temp audio save
        print("text to audio start") 
        txtfile = open("alltext.txt","r+")
        print("TExt file is ",type(txtfile))
        finaltext=txtfile.read()
        
        
        root.update_idletasks()
        downloadbar['value'] += 16
        time.sleep(1)
        
        
        language = 'en'
        print("text to audio start 2") 
        audio= gTTS(text=finaltext, lang=language, slow=False)
        ttxt=audio.save("tempAudio1.mp3")


        root.update_idletasks()
        downloadbar['value'] += 16
        time.sleep(1)

        # saving to new Destination
        main_file =  open("tempAudio1.mp3", "rb").read()

        root.update_idletasks()
        downloadbar['value'] += 12
        time.sleep(1)

        dest_file = open('D:/Audiobook.mp3','wb+')

        root.update_idletasks()
        downloadbar['value'] += 20
        time.sleep(1)

        dest_file.write(main_file)
        dest_file.close()
        
        downloadbar['value'] = 100
        print("Download 2 way try ")

        # filetxt= 'alltext.txt'
        file = 'tempAudio1.mp3'
        os.remove(file)
        
        


        # os.remove(filetxt)
        messagebox.showinfo("Information","File Saved at D:/")
    except:
        messagebox.showerror('Download Error', 'Error: Download problem!')  
        #  



    


# Creating Butoons,labels with thir Dimention

label_file = Label(root, text = "Select File....", width = 100, height = 4,fg = "blue")
Headline = Label(root, text = "Convert PDF to AudioBook",height= 3, width=25,)
Headline.config(font =("Courier", 14))
audio = Button(text="Select PDF",height= 2, width=10,command=convert)
download = Button(root, text = 'Download',height= 3, width=25, command = lambda : save())
exit = Button(root, text="Exit",height= 2, width=15,command=root.destroy)


# Displaying the Buttons and Label With thir Position

Headline.grid(column = 2, row = 3,)
label_file.grid(column = 1, row = 3)
processbar.grid(column = 1, row = 8)
downloadbar.grid(column = 1, row = 10)
audio.grid(column = 1,row = 12)
download.grid(column = 1,row = 22)
exit.grid(column = 1,row = 27)


Headline.place(x=200, y=10)
audio.place(x=300, y=140)
label_file.place(x=0, y=180)
processbar.place(x=90, y=250)
download.place(x=250, y=290)
downloadbar.place(x=140, y=350)
exit.place(x=290, y=380)


root.mainloop()



# 1.for pytessreact u need to download binary file and install .exe and mention his path in code
#  EX.pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# to Download it..https://github.com/UB-Mannheim/tesseract/wiki

# 2.for image from pdf2image import convert_from_path this module u need to download propler
#   And save any where n mention path till bin in code 
#   EX.images = convert_from_path(filepath,500,poppler_path=r'C:\Program Files\poppler-22.01.0\Library\bin')

