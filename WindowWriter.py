import ml
from PIL import Image
import _thread
import tkinter as tk  # Python 3
from tkinter import TclError
from PIL import Image, ImageFont, ImageDraw, ImageTk
import time


class WindowWriter:
    def _text_image(self, text):
        name = 'tmp/text_image_tmp.png'
        image = Image.new('RGB', (1920, 1080), color=(255, 0, 0))
        draw = ImageDraw.Draw(image)
        # specified font size

        font = ImageFont.truetype(r'fonts\SIMYOU.TTF', self.text_size)
        # font = ImageFont.truetype('fonts/STHUPO.TTF', 40)
        # drawing text size
        draw.text((0, 0), text, font=font, align="left", fill=(254, 0, 0, 255), stroke_fill=(254, 0, 0, 255),
                  stroke_width=1)
        image.save(name)
        return name

    def _window_thread(self, x, y, offset=1.0):
        ml.ensure_dir('tmp')
        root = tk.Tk()
        self.text_size = 30
        # The image must be stored to Tk or it will be garbage collected.
        root.image = tk.PhotoImage(file=self._text_image('hello world'))
        label = tk.Label(root, image=root.image, bg='red')
        self.root = root
        self.label = label
        root.overrideredirect(True)
        root.geometry(f"+{int(x * offset)}+{int(y * offset)}")  # real index is bigger for 1/4
        root.lift()
        root.wm_attributes("-topmost", True)
        root.wm_attributes("-disabled", True)
        root.wm_attributes("-transparentcolor", "red")
        label.pack()
        label.mainloop()

    # offset 1.0 or 0.8
    def __init__(self, x, y, offset=1.0):
        ml.ensure_dir('tmp')
        _thread.start_new_thread(self._window_thread, (x, y, offset,))

    def set_text(self, text):
        img2 = ImageTk.PhotoImage(Image.open(self._text_image(text)))
        self.label.configure(image=img2)
        self.label.image = img2
        self.root.update_idletasks()

    def set_text_size(self, size):
        self.text_size = size


if __name__ == '__main__':
    w = WindowWriter(1625, 584, 4 / 5)
    counter = 1000
    while True:
        time.sleep(1)
        w.set_text(str(counter))
        counter += 1
    pass
    # while True:
    #     t.set_text(''+str(i))
    #     i+=1
    #     time.sleep(2)
    # time.sleep(5)

    # s = ml.read_string(
    #     r'C:\Users\1\Downloads\(auto)SAPIENS_ A BRIEF HISTORY OF HUMANKIND _ ANIMATED BOOK SUMMARY - YouTube.srt')
    # # print(s)
    # l = s.split('\n')
    # print(l)
    # ind = 2
    # r = ''
    # for ind in range(2, len(l), 4):
    #     print(l[ind])
    #     r += l[ind]+' '
    # ml.write_string('tmp.txt',r)
    from tkinter import Tk  # or(from Tkinter import Tk) on Python 2.x
