from PIL import ImageGrab, Image
import win32gui
import sys
import cv2
import pytesseract
import time
import numpy as np

from os import listdir, remove
from os.path import isfile, join

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_PATH = 'C:/Users/USUARIO/Desktop/gc-tracker/SRs/'
TEMP_IMAGE_PATH = 'temp_screenshot.png'

sr_dict = {
  'Sherlockao': 'Sherlockão',
  'DK.MARK3': 'DK-MARK3',
}

def print_unique_pixels(image):
  pixels = {}
  for line in image:
    for px in line:
      [b, g, r] = px
      key = f"{b},{g},{r}"
      if key not in pixels.keys():
        print(px)
        pixels[key] = px

def show_image(image):
  cv2.imshow('image', image)
  cv2.waitKey(0)

def enum_cb(hwnd, results):
  winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

def get_sr_name_from_image(path):
  image = cv2.imread(TEMP_IMAGE_PATH)

  lower_blue = np.array([151, 197, 1])
  upper_blue = np.array([183, 255, 10])

  mask = cv2.inRange(image, lower_blue, upper_blue)

  sr_name = pytesseract.image_to_string(mask)[:-1]

  if sr_name in sr_dict.keys():
    return sr_dict[sr_name]

  return sr_name

def take_screenshot():
  win32gui.SetForegroundWindow(hwnd)
  bbox = win32gui.GetWindowRect(hwnd)
  return ImageGrab.grab(bbox)

def crop_to_focus_area(image):
  return img.crop((384, 231, 829, 718))

def get_path(char_name, sr_name):
  return f"{BASE_PATH}{char_name}/{sr_name}.png"

def save_image(img, path):
  img.save(path)
  output_path = "file://C:/Users/USUARIO/" + path
  print('Image saved to ' + output_path)

if len(sys.argv) >= 2:
  char_name = sys.argv[1]
  toplist, winlist = [], []

  win32gui.EnumWindows(enum_cb, toplist)

  for hwnd, title in winlist:
    if 'grandchase' in title.lower():
      img = take_screenshot()
      img.save(TEMP_IMAGE_PATH)
      sr_name = get_sr_name_from_image(TEMP_IMAGE_PATH)
      image_path = get_path(char_name, sr_name)
      cropped_img = crop_to_focus_area(img)
      save_image(cropped_img, image_path)

      break
else:
  print('Utilize o comando da seguinte forma:')
  print(sys.argv[0] + ' [char_name]')

# for char_folder in listdir(BASE_PATH):
#   char_folder_path = BASE_PATH + char_folder
#   images = [img for img in listdir(BASE_PATH + char_folder)]
#   for img_file in images:
#     image_path = char_folder_path + '/' + img_file
#     img = Image.open(image_path)
#     width, height = img.size
#     path, extension = image_path.split('.')

#     if width > 450 and height > 490:
#       print('cortei')
#       cropped_img = crop_to_focus_area(img)

#       new_path = path + '_crop.' + extension
#       cropped_img.save(image_path)

#     if extension == 'jpg':
#       print(image_path)
#       img.save(path + '.png')
#       remove(image_path)