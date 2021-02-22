from gerais import salvar_imagem
import PIL
from PIL import Image, ImageTk
from tkinter import *
import numpy as np
import tkinter as tk
from tkinter import ttk
from rgbHsv import hsvArray, ajustarSat, ajustarMatiz




class HsvWindow(tk.Tk):
    image = PIL.Image.open("pikachu.png")
    img2 = image

    def __init__(self):
        super().__init__()

        self.title('Matiz, saturação e valor')
        #self.resizable(0, 0)

        self.create_widgets()

    def create_widgets(self):
        #Imagem
        hsv = hsvArray(np.asarray(self.image))
        photo = ImageTk.PhotoImage(self.image)
        img_label = tk.Label(self, image=photo)
        img_label.image = photo
        
        img_label.pack(side=LEFT)

        #Define o tamanho da dela baseado na largura da imagem
        s = str(self.image.width + 300) + "x600"
        self.geometry(s)


        #Sliders
        def saturation():
            self.img2 = ajustarSat(hsv, satSlider.get())
            photo = ImageTk.PhotoImage(self.img2)
            img_label.configure(image=photo)
            img_label.image = photo

        def hue():
            self.img2 = ajustarMatiz(hsv, mtzSlider.get())
            photo = ImageTk.PhotoImage(self.img2)
            img_label.configure(image=photo)
            img_label.image = photo

        def salvar():
            self.img2.save("NovaImagem.png", "png")
            

        def valor():
            img2 = ajustarMatiz(hsv, mtzSlider.get())
            photo = ImageTk.PhotoImage(img2)
            img_label.configure(image=photo)
            img_label.image = photo

        rightSideFrame = tk.Frame(self, width=200, height=300,)
        rightSideFrame.pack(anchor=CENTER,side= RIGHT)
        rightSideFrame.pack_propagate(0)

        space = tk.Frame(rightSideFrame, width=140, height=50, )
        space.pack(anchor=W,side= BOTTOM)
        space.pack_propagate(0)
        
        satFrame = tk.Frame(rightSideFrame, width=200, height=100)
        satFrame.pack(anchor=W,side= BOTTOM)
        satFrame.pack_propagate(0)

        satLabel = Label(satFrame, text="Saturação")
        satLabel.pack(side=RIGHT)
        applSat = Button(satFrame, text="Aplicar", command=saturation)
        applSat.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        satSlider = Scale(satFrame, from_=-100, to=100, orient=HORIZONTAL)
        satSlider.set(0)
        satSlider.pack(side=BOTTOM)

        mtzFrame = tk.Frame(rightSideFrame, width=200, height=100)
        mtzFrame.pack(anchor=W,side= BOTTOM)
        mtzFrame.pack_propagate(0)

        mtzLabel = Label(mtzFrame, text="  Matiz     ")
        mtzLabel.pack(side=RIGHT)
        applMatiz = Button(mtzFrame, text="Aplicar", command=hue)
        applMatiz.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        mtzSlider = Scale(mtzFrame, from_=-360, to=360, orient=HORIZONTAL)
        mtzSlider.set(0)
        mtzSlider.pack(side=BOTTOM)


        salvar = Button(space, text=" Salvar ", command=salvar)
        salvar.pack(anchor= CENTER, side=BOTTOM, expand=1)
        





        


root = HsvWindow()
root.mainloop()