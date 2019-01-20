#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author  :   Goodwillie
@Software:   PyCharm
@File    :   capcha.py
@Time    :   2019/1/16 23:41
@Desc    :
'''
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import random
import string
import os
pwd = os.path.abspath(__file__)
font_file = os.path.join(pwd,'ariblk.ttf')
font = ImageFont.truetype(font_file, 36)

# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:
def rndColor():
    return (random.randint(164, 255), random.randint(164, 255), random.randint(164, 255)) # 数值调大点,不然看不清

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def getcapcha(num=5,size=(90,68)):
    cap_text = ''.join(random.sample(string.ascii_uppercase + string.digits, num))

    width = size[0] * num
    height = size[1]
    image = Image.new('RGB', (width, height), color=rndColor())
    # 创建Font对象:

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    # # 填充每个像素:
    # for x in range(width):
    #     for y in range(height):
    #         draw.point((x, y), fill=rndColor())
    # 输出文字:
    for t in range(num):
        draw.text((size[0] * t + 20, 15), cap_text[t], font=font, fill=rndColor2())
    # 模糊:
    image = image.filter(ImageFilter.BLUR)

    f = io.BytesIO()
    image.save(f, 'png')
    return f.getvalue(),cap_text

if __name__=='__main__':
    import time
    t1 = time.time()
    for i in range(1000):
        getcapcha() # 平均3.5毫秒
    t2 = time.time()
    print(t2-t1)
