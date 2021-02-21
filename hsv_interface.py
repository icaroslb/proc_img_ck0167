from PIL import Image, ImageTk
from tkinter import *
import numpy as np
from rgbHsv import hsvArray, ajustarSat, ajustarMatiz, ajustarValor


root = Tk()
root.title('Codemy.com Image Viewer')
root.geometry("499x499")

def slide():
    newSat = Label(root, text=satSlider.get())

satLabel = Label(root, text="Saturação").pack()
satSlider = Scale(root, from_=-100, to=100, orient=HORIZONTAL)
satSlider.set(0)
satSlider.pack()
applSat = Button(root, text="Aplicar", command=slide).pack()

valLabel = Label(root, text="Valor").pack()
valSlider = Scale(root, from_=-100, to=100, orient=HORIZONTAL)
valSlider.set(0)
valSlider.pack()
applVal = Button(root, text="Aplicar", command=slide).pack()

img = Image.open('sonora.png')
imgArray = np.asarray(img)

hsvArray = hsvArray(imgArray)
ajustarSat(hsvArray)
root.mainloop()