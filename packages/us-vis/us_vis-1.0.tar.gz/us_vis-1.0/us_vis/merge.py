from PIL import Image
import math


def list_pics(pics):
    """
    Function adds .png extension to the list of names
    """
    pics = [x + ".png" for x in pics]
    return pics


def merge_pics(pics, columns, name):
    """
    Merges pictures specified in "pics" argument
    """
    for image in pics:
        rows = math.ceil(len(pics)/columns)
        width_max = max([Image.open(image).width for image in pics])
        height_max = max([Image.open(image).height for image in pics])
        background = Image.new('RGBA', (columns*(width_max+1),
                               rows*(height_max+1)), (255, 255, 255, 255))
        x = 0
        y = 0
        for i, image in enumerate(pics):
            img = Image.open(image)
            x_offset = int((width_max-img.width)/2)
            y_offset = int((height_max-img.height)/2)
            background.paste(img, (x+x_offset, y+y_offset))
            x += width_max
            if (i+1) % columns == 0:
                y += height_max
                x = 0
        background.save(name+".png")
