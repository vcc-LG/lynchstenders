import os
import random
from os import listdir
from os.path import isfile, join

import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def view_image(image_path):
    img = mpimg.imread(image_path)
    imgplot = plt.imshow(img)
    plt.show()


def add_text_to_image(image_path, text_string, count):
    base = Image.open(image_path).convert("RGBA")
    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    fnt = ImageFont.truetype("LucidaGrande.ttf", 40)
    d = ImageDraw.Draw(txt)
    d.text((random.randint(0, round(base.size[0]/2)), random.randint(0, base.size[1])), text_string, font=fnt, fill=(255, 255, 255, 255))
    out = Image.alpha_composite(base, txt)
    out.save('overlays/image_'+str(count)+'.png')
    # out.show()


all_text = open('script_sentences.txt', 'r')

sentence_array = [line.split(',') for line in all_text.readlines()]

image_files = [f for f in listdir('screens') if isfile(join('screens', f))]
random.shuffle(image_files)

count = 0
for path in image_files:
    count = count + 1
    add_text_to_image(os.path.join('screens', path), " ".join(
        random.choice(sentence_array)).strip('\n'), count)
