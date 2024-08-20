import tkinter as tk
from tkinter import PhotoImage
from tkinter import *
from tkinter import messagebox, filedialog 
from tkinter import ttk

from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk

import shutil 

import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch

import os
import subprocess


def hell():
   model_path = 'models/RRDB_PSNR_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
   device = torch.device('cuda')  
   # device = torch.device('cpu')

   test_img_folder = 'LR/*'

   model = arch.RRDBNet(3, 3, 64, 23, gc=32)
   model.load_state_dict(torch.load(model_path), strict=False)
   model.eval()
   model = model.to(device)

   print('Model path {:s}. \nTesting...'.format(model_path))

   idx = 0
   for path in glob.glob(test_img_folder):
      idx += 1
      base = osp.splitext(osp.basename(path))[0]
      print(idx, base)
      # read images
      img = cv2.imread(path, cv2.IMREAD_COLOR)
      img = img * 1.0 / 255
      img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
      img_LR = img.unsqueeze(0)
      img_LR = img_LR.to(device)

      with torch.no_grad():
         output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
      output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
      output = (output * 255.0).round()
      cv2.imwrite('results/{:s}_rlt.png'.format(base), output)




win= tk.Tk()
win.title("Image Upscaller")
win.geometry("800x550")
win.resizable(False, False)
browsebt = PhotoImage(file="new.png")
startbt = PhotoImage(file="start.png")
resultbt = PhotoImage(file="result.png")
bg_title = PhotoImage(file="titleh (1).png")

def CreateWidgets(): 
    
    bgtitle = tk.Label(win, image=bg_title)
    bgtitle.place(x=230, y=20,width=352,height=80)    


    Browse=tk.Button(win, image =browsebt, border =0)
    #Browse.place(x=285, y=40)
    #Browse["bg"] = "#f0f0f0"
    #ft = tkFont.Font(family='Times',size=10)
    #Browse["font"] = ft
    #Browse["fg"] = "#000000"
    Browse["justify"] = "center"
    Browse["text"] = "Browse"
    Browse.place(x=300,y=110,width=197,height=59)
    Browse["command"] = SourceBrowse
	
    win.sourceText = Entry(win, width = 50, 
						textvariable = sourceLocation) 

    win.destinationText = Entry(win, width = 50, 
                textvariable = destinationLocation) 
    
    
	
    Start=tk.Button(win, image =startbt, border =0)
    Start["bg"] = "#f0f0f0"
    #ft = tkFont.Font(family='Times',size=10)
    #Start["font"] = ft
    Start["fg"] = "#000000"
    Start["justify"] = "center"
    Start["text"] = "Start"
    Start.place(x=320,y=350,width=120,height=35)
    Start["command"] = CopyFile

    Results=tk.Button(win, image = resultbt, border =0)
    Results["bg"] = "#f0f0f0"
    #ft = tkFont.Font(family='Times',size=10)
    #Results["font"] = ft
    Results["fg"] = "#000000"
    Results["justify"] = "center"
    Results["text"] = "Results"
    Results.place(x=320,y=400,width=120,height=35)
    Results["command"] = browseFiles
	

def SourceBrowse(): 
    win.files_list = list(filedialog.askopenfilenames(initialdir ="C:/Users/AKASH / Desktop / Lockdown Certificate / Geek For Geek")) 
    win.sourceText.insert('1', win.files_list)

    col = 0
    row = 1
    x_offset = 10
    y_offset = 10
    for f in win.files_list:
        img = Image.open(f)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)
        e1 = tk.Label(win, image=img)
        e1.image = img
        e1.place(x=col * 110 + x_offset, y=row * 170 + y_offset)
        col += 1
        if col == 7:
            col = 0
            row += 1

    DestinationBrowse() 
	
def DestinationBrowse():  
    destinationdirectory = ("LR")
    win.destinationText.insert('1', destinationdirectory) 
	


def CopyFile(): 
    files_list = win.files_list 
    destination_location = destinationLocation.get() 
    for f in files_list:  
        shutil.copy(f, destination_location) 
    hell() 

def browseFiles():
    subprocess.Popen(f'explorer "results"')



image_path = PhotoImage(file="iron.png")
bg_image = tk.Label(win, image=image_path)
bg_image.place(x=0, y=0, relwidth=1, relheight=1)

	
sourceLocation = StringVar() 
destinationLocation = StringVar() 
	
CreateWidgets() 

win.mainloop()