import PIL
from PIL import Image, ImageTk
from tkinter import *
import numpy as np
import tkinter as tk
from tkinter import ttk
from eqCores import equalizaCores




class eqWindow(tk.Tk):

    image = PIL.Image.new("RGB", (800, 1280), (255, 255, 255))
    img2 = image

    def __init__(self, caminho):
        super().__init__()
        global dados_f
        #self.image = PIL.Image.open(caminho)
        self.image = PIL.Image.fromarray( np.uint8( dados_f.I * 255 ) ).convert( "RGB" )
        self.img2 = self.image
        self.title('Equilíbrio de Cores')
        #self.resizable(0, 0)

        self.create_widgets(dados_f.caminho)

    def create_widgets(self, caminho):
        imgArray = np.asarray(self.image)

        #Imagem
        photo = ImageTk.PhotoImage(self.image)
        img_label = tk.Label(self, image=photo)
        img_label.image = photo
        
        img_label.pack(side=LEFT)

        #Define o tamanho da dela baseado na largura da imagem
        s = str(self.image.width + 300) + "x600"
        self.geometry(s)


        #Sliders
        def saturation():
            self.img2 = equalizaCores(imgArray, crSlider.get(), mgSlider.get(), ybSlider.get())
            photo = ImageTk.PhotoImage(self.img2)
            img_label.configure(image=photo)
            img_label.image = photo


        def salvar():
            #self.img2.save("NovaImagem.png", "png")
            dados_f.I = np.array( self.img2 ) / 255
            


        rightSideFrame = tk.Frame(self, width=200, height=300,)
        rightSideFrame.pack(anchor=CENTER,side= RIGHT)
        rightSideFrame.pack_propagate(0)

        space = tk.Frame(rightSideFrame, width=140, height=50, )
        space.pack(anchor=W,side= BOTTOM)
        space.pack_propagate(0)

        ybFrame = tk.Frame(rightSideFrame, width=200, height=100)
        ybFrame.pack(anchor=W,side= BOTTOM)
        ybFrame.pack_propagate(0)

        ybLabel = Label(ybFrame, text="  Y - B        ")
        ybLabel.pack(side=RIGHT)
        applALL = Button(ybFrame, text="Aplicar", command=saturation)
        applALL.pack(anchor=CENTER, side=BOTTOM, pady=10, expand=1)
        ybSlider = Scale(ybFrame, from_=-255, to=255, orient=HORIZONTAL)
        ybSlider.set(0)
        ybSlider.pack(side=BOTTOM)
        
        mgFrame = tk.Frame(rightSideFrame, width=200, height=50)
        mgFrame.pack(anchor=W,side= BOTTOM)
        mgFrame.pack_propagate(0)

        mgLabel = Label(mgFrame, text="  M - G        ")
        mgLabel.pack(side=RIGHT)
        mgSlider = Scale(mgFrame, from_=-255, to=255, orient=HORIZONTAL)
        mgSlider.set(0)
        mgSlider.pack(side=BOTTOM)

        crFrame = tk.Frame(rightSideFrame, width=200, height=50)
        crFrame.pack(anchor=W,side= BOTTOM)
        crFrame.pack_propagate(0)

        crLabel = Label(crFrame, text="  C - R        ")
        crLabel.pack(side=RIGHT)
        crSlider = Scale(crFrame, from_=-255, to=255, orient=HORIZONTAL)
        crSlider.set(0)
        crSlider.pack(side=BOTTOM)


        salvar = Button(space, text=" Salvar ", command=salvar)
        salvar.pack(anchor= CENTER, side=BOTTOM, expand=1)

dados_f = None

def janelaEq( dados ):
    print("Confira a janela de edição")

    global dados_f
    dados_f = dados

    root = eqWindow(dados.caminho)
    root.mainloop()

