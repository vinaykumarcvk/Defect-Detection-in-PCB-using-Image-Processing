from tkinter import *
import tkinter as tk
import cv2
import numpy as np
import statistics
from PIL import ImageTk,Image
import tkinter.filedialog
root = Tk()
    
def pcb():
    path = tk.filedialog.askopenfilenames(parent=root,title='choose template and test images')
    lst=list(path)
    print(lst)
    img3=cv2.imread(lst[1])
    img=cv2.imread(lst[0],0)
    image=cv2.imread(lst[1],0)
    #cv2.imshow('template_image',img)
    #cv2.imshow('defected_image',image)
    ret,thresh1 = cv2.threshold(img,120,255,cv2.THRESH_BINARY_INV)
    ret,thresh2 = cv2.threshold(image,120,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('original',thresh1)
    #cv2.imshow('defected',thresh2)
    image1=thresh2-thresh1
    image11=thresh1-thresh2
    #cv2.imshow('subtracted_image1',image11)
    ##cv2.imshow('subtracted_image',image1)
    kernel = np.ones((2,3),np.uint8)
    opening1 = cv2.morphologyEx(image1, cv2.MORPH_OPEN, kernel)
    ##cv2.imshow('subtracted_image21',opening1)
    #kernel = np.ones((2,3),np.uint8)
    opening = cv2.morphologyEx(image11, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('subtracted_image12',opening)
    ret,thresh3 = cv2.threshold(opening1,120,255,cv2.THRESH_BINARY_INV)
    ret,thresh4 = cv2.threshold(opening,120,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('image1',thresh3)
    #cv2.imshow('image2',thresh4)'''
    _,contours,_ = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    _,contours1,_ = cv2.findContours(thresh4,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print(len(contours))
    print(len(contours1))
    #img_contours = np.ones(img.shape)
    #cv2.drawContours(img_contours, contours, -1, (0,255,0), 3)
    #cv2.imshow('pavan',img_contours)
    #cv2.imwrite('saved.png',opening1)
    #im2,contours1, hierarchy = cv2.findContours(opening,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    list1=[]
    for c in contours:
        perimeter=cv2.arcLength(c,True)
        list1.append(perimeter)
    mean1=statistics.mean(list1)
    print(mean1)
    for c in contours:
        perimeter=cv2.arcLength(c,True)
        if(perimeter<(mean1/2)):
            cv2.drawContours(img3,[c],-1,(0,255,0),2)
        else:
            cv2.drawContours(img3,[c],-1,(255,0,0),2)

    list2=[]
    for c in contours1:
        perimeter=cv2.arcLength(c,True)
        list2.append(perimeter)
    mean2=statistics.mean(list2)
    print(mean2)
    for c in contours1:
        perimeter=cv2.arcLength(c,True)
        if(perimeter<(mean2/2)):
            cv2.drawContours(img3,[c],-1,(0,0,255),2)
        else:
            cv2.drawContours(img3,[c],-1,(255,255,0),2)
           

    #cont=cv2.drawContours(img3, contours, -1, (0,255,0), 2)
    #cont1=cv2.drawContours(img3, contours1, -1, (255,0,0), 2)
    #cv2.imshow('contour',img3)

    namer = cv2.circle(img3,(50,50), 12, (255,0,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img3,'SHORT CIRCUIT',(70,50), font, 0.5,(255,0,0),2,cv2.LINE_AA)

    nameb = cv2.circle(namer,(50,75), 12, (0,0,255), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(nameb,'PIN HOLE',(70,75), font, 0.5,(0,0,255),2,cv2.LINE_AA)

    nameg = cv2.circle(nameb,(50,100), 12, (0,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(nameg,'SPUR',(70,100), font, 0.5,(0,255,0),2,cv2.LINE_AA)

    name = cv2.circle(nameg,(50,125), 12, (255,255,0), -1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(name,'OPEN CIRCUIT',(70,125), font, 0.5,(255,255,0),2,cv2.LINE_AA)
    #cv2.imshow('original',img)
    #cv2.imshow('cn1',cont)
    cv2.imshow('final',name)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

frame = tk.Frame(root)
frame.pack()
pathimg = 'pcb2.jpg'
img = ImageTk.PhotoImage(Image.open(pathimg))
panel = tk.Label(root, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
b =Button(root,text="select template & test images",command=pcb,fg='blue',bg='white')
b.pack(side="bottom",fill= "both", expand="yes", padx="25", pady="25")

root.title('DEFECTS DETECTION IN A PCB ')
root.iconbitmap('srkricon.ico')
root.mainloop()
