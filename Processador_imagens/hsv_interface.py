from gerais import salvar_imagem
import PIL
from PIL import Image, ImageTk
from tkinter import *
import numpy as np
import tkinter as tk
from tkinter import ttk
from rgbHsv import ajustarValor, hsvArray, ajustarSat, ajustarMatiz
import rgbHsv




class HsvWindow(tk.Tk):

    image = PIL.Image.new("RGB", (800, 1280), (255, 255, 255))
    img2 = image

    def __init__(self, dados):
        super().__init__()
        
        global dados_f
        #self.dados = dados
        self.image = PIL.Image.fromarray( np.uint8( dados.I * 255 ) ).convert( "RGB" ) #PIL.Image.open(caminho)
        self.img2 = self.image
        self.title('Matiz, saturação e brilho')
        #self.resizable(0, 0)

        self.create_widgets( dados.caminho )

    def create_widgets(self, caminho):
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
            dados_f.I = rgbHsv.rgbArray( hsv ) / 255
            

        def valor():
            img2 = ajustarValor(hsv, valSlider.get())
            photo = ImageTk.PhotoImage(img2)
            img_label.configure(image=photo)
            img_label.image = photo

        rightSideFrame = tk.Frame(self, width=200, height=400,)
        rightSideFrame.pack(anchor=CENTER,side= RIGHT)
        rightSideFrame.pack_propagate(0)

        space = tk.Frame(rightSideFrame, width=140, height=50, )
        space.pack(anchor=W,side= BOTTOM)
        space.pack_propagate(0)

        valFrame = tk.Frame(rightSideFrame, width=200, height=100)
        valFrame.pack(anchor=W,side= BOTTOM)
        valFrame.pack_propagate(0)

        valLabel = Label(valFrame, text="Brilho          ")
        valLabel.pack(side=RIGHT)
        applVal = Button(valFrame, text="Aplicar", command=valor)
        applVal.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        valSlider = Scale(valFrame, from_=-100, to=100, orient=HORIZONTAL)
        valSlider.set(0)
        valSlider.pack(side=BOTTOM)
        
        satFrame = tk.Frame(rightSideFrame, width=200, height=100)
        satFrame.pack(anchor=W,side= BOTTOM)
        satFrame.pack_propagate(0)

        satLabel = Label(satFrame, text="Saturação   ")
        satLabel.pack(side=RIGHT)
        applSat = Button(satFrame, text="Aplicar", command=saturation)
        applSat.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        satSlider = Scale(satFrame, from_=-100, to=100, orient=HORIZONTAL)
        satSlider.set(0)
        satSlider.pack(side=BOTTOM)

        mtzFrame = tk.Frame(rightSideFrame, width=200, height=100)
        mtzFrame.pack(anchor=W,side= BOTTOM)
        mtzFrame.pack_propagate(0)

        mtzLabel = Label(mtzFrame, text="  Matiz        ")
        mtzLabel.pack(side=RIGHT)
        applMatiz = Button(mtzFrame, text="Aplicar", command=hue)
        applMatiz.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        mtzSlider = Scale(mtzFrame, from_=-360, to=360, orient=HORIZONTAL)
        mtzSlider.set(0)
        mtzSlider.pack(side=BOTTOM)


        salvar = Button(space, text=" Salvar ", command=salvar)
        salvar.pack(anchor= CENTER, side=BOTTOM, expand=1)

dados_f = None

def janelaHsv( dados ):
    print("Confira a janela de edição")

    global dados_f

    dados_f = dados
    root = HsvWindow( dados )
    root.mainloop()
