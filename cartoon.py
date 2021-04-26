import cv2
import easygui
import numpy as np 
import imageio
import sys 
import matplotlib.pyplot as plt
import os 
import tkinter as tk
from tkinter import filedialog 
from tkinter import *
from PIL import ImageTk, Image 

def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    #read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)
    #print(image)  # image is stored in form of numbers
    # confirm that image is chosen
    if originalmage is None:
        print("Can not find any image. Choose appropriate file")
        sys.exit()
    
    Resized1 = cv2.resize(originalmage, (960, 540))
    
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    Resized2 = cv2.resize(grayScaleImage, (960, 540))
    
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    Resized3 = cv2.resize(grayScaleImage, (960, 540))
    
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    Resized4 = cv2.resize(getEdge, (960, 540))
    
    colorImage = cv2.bilateralFilter(originalmage, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960, 540))
    
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask = getEdge)
    Resized6 = cv2.resize(cartoonImage, (960, 540))
    
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw = dict(hspace = 0.1, wspace = 0.1))
    
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap = 'gray')
        
    plt.show()

def save(Resized6, ImagePath):
    newName = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath) [1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.COLOR_RGB2BGR)
    I = "Image saved by the name "+ newName + "at " + path
    tk.messagebox.showinfo(title = None, message = I)

top = tk.Tk()
top.geometry('400x400')
top.title("Cartoonify your Image!")
top.configure(background="white")
label = Label(top, background="#CDCDCD", font=('calibri', 20, 'bold'))

upload = Button(top, text="Cartoonify an Image", command = upload, padx = 10, pady = 5)
upload.configure(background = "#364156", foreground = "white", font=('calibri', 10, 'bold'))
upload.pack(side = TOP, pady = 50)

save1 = Button(top, text = "Save Cartoon Image", command = lambda: save(ImagePath, Resized6), padx = 30, pady = 5)
save1.configure(background = "#364156", foreground = "white", font=('calibri', 10, 'bold'))
save1.pack(side = TOP, pady = 50)

top.mainloop()