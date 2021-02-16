import base64
from os import urandom
import pygame
from playback import midiToBase64, play_music
import cv2
import numpy as np

def messageToBinary(message):
  if type(message) == str:
    return ''.join([ format(ord(i), "08b") for i in message ])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [ format(i, "08b") for i in message ]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, "08b")
  else:
    raise TypeError("Input type not supported")

def hideData(image, secret_message):

  # Calcula a quantidade máxima de bytes
  n_bytes = image.shape[0] * image.shape[1] * 3 // 8
  print("Maximum bytes to encode:", n_bytes)

  #Confere se a quantidade de bytes a ser codificados excede o valor máximo.
  if len(secret_message) > n_bytes:
      raise ValueError("Impossível de esteganografar na imagem :(")
  
  secret_message += "#####" 

  data_index = 0
  binary_secret_msg = messageToBinary(secret_message)

  data_len = len(binary_secret_msg) #Calcula o tamanho dos dados a ser escondidos
  for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel)
          if data_index < data_len:
              pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index < data_len:
              pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
              data_index += 1
          if data_index >= data_len:
              break

  return image
  
def consumir_dados(image):

  binary_data = ""
  for values in image:
      for pixel in values:
          r, g, b = messageToBinary(pixel)
          binary_data += r[-1] 
          binary_data += g[-1] 
          binary_data += b[-1]
  # divide em 8-bits
  all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
  decoded_data = ""
  for byte in all_bytes:
      decoded_data += chr(int(byte, 2))
      if decoded_data[-5:] == "#####": 
          break
  return decoded_data[:-5] 

def codificar_dados(image_name): 
  image = cv2.imread(image_name) 
  
  print("The shape of the image is: ",image.shape)
  
  midis = ["bwv-773.mid", "lune-op46"]
  music_file = "midis/" + midis[urandom.randint(0,len(midis)-1)]
  data = midiToBase64(music_file).decode('utf-8')
  
  if (len(data) == 0): 
    raise ValueError('Está vazio! >:(')
  
  filename = input("Insira o nome da imagem de saída: ")
  encoded_image = hideData(image, data)
  cv2.imwrite(filename, encoded_image)

def decodificar_dados(image_name):
  image = cv2.imread(image_name)
  dados = consumir_dados(image)

  fish = base64.b64decode(dados.encode("utf-8"))
  fout = open("audio.mid","wb")
  fout.write(fish)
  fout.close()

  #freq, bitsize, channels, buffer
  pygame.mixer.init(44100, -16, 2, 1024)
    
  try:
    play_music('audio.mid')
  except KeyboardInterrupt:

    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit

  return dados
