import PIL
from PIL import Image, ImageTk
from tkinter import *
import numpy as np
import tkinter as tk
from tkinter import ttk
from rgbHsv import hsvArray, ajustarSat, ajustarMatiz, ajustarValor




class HsvWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title('Matiz, saturação e valor')
        #self.resizable(0, 0)

        self.create_widgets()

    def create_widgets(self):
         #Imagem
        image = PIL.Image.open("pikachu.png")
        photo = ImageTk.PhotoImage(image)
        img_label = tk.Label(self, image=photo)
        img_label.image = photo
        hsv = hsvArray(np.asarray(image))
        
        img_label.pack(side=LEFT)

        #Sliders
        def saturation():
            img2 = ajustarSat(hsv, satSlider.get())
            photo = ImageTk.PhotoImage(img2)
            img_label.configure(image=photo)
            img_label.image = photo

        def hue():
            img2 = ajustarMatiz(hsv, mtzSlider.get())
            photo = ImageTk.PhotoImage(img2)
            img_label.configure(image=photo)
            img_label.image = photo

        def valor():
            img2 = ajustarMatiz(hsv, mtzSlider.get())
            photo = ImageTk.PhotoImage(img2)
            img_label.configure(image=photo)
            img_label.image = photo

        rightFrame = tk.Frame(self, width=200, height=500)
        rightFrame.pack(anchor=CENTER,side= RIGHT)
        rightFrame.pack_propagate(0)
        
        satFrame = tk.Frame(rightFrame, width=200, height=100)
        satFrame.pack(anchor=CENTER,side= BOTTOM)
        satFrame.pack_propagate(0)

        satLabel = Label(satFrame, text="Saturação")
        satLabel.pack(side=RIGHT)
        applSat = Button(satFrame, text="Aplicar", command=saturation)
        applSat.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        satSlider = Scale(satFrame, from_=-100, to=100, orient=HORIZONTAL)
        satSlider.set(0)
        satSlider.pack(side=BOTTOM)

        mtzFrame = tk.Frame(rightFrame, width=200, height=100)
        mtzFrame.pack(anchor=CENTER,side= BOTTOM)
        mtzFrame.pack_propagate(0)

        mtzLabel = Label(mtzFrame, text="Matiz")
        mtzLabel.pack(side=RIGHT)
        applMatiz = Button(mtzFrame, text="Aplicar", command=hue)
        applMatiz.pack(anchor=CENTER, side=BOTTOM, pady=10,  expand=1)
        mtzSlider = Scale(mtzFrame, from_=-360, to=360, orient=HORIZONTAL)
        mtzSlider.set(0)
        mtzSlider.pack(side=BOTTOM)
        





        


root = HsvWindow()
root.mainloop()