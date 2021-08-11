from PIL import Image
import cv2
import os
import pathlib
import numpy
import os
import sys
import paddlehub as hub
import numpy as np


class ImageProcess:
    def __init__(self, path):
        assert os.path.exists(path)
        self.img = Image.open(path).convert("RGB")
        self.w, self.h = self.img.size

    def resize(self, w, h, bGColor=(255, 255, 255), ratio=False) -> Image:
        background = Image.new("RGB", size=(max(self.w, self.h), max(self.w, self.h)), color=bGColor)
        length = abs(self.w - self.h) // 2
        box = (length, 0) if self.w < self.h else (0, length)
        background.paste(self.img, box)
        background.show()
        img = background.resize((min(w, h), min(w, h)), resample=Image.LANCZOS, reducing_gap=3)
        img.show("img")
        print(bGColor)
        res = Image.new("RGB", (w, h), bGColor)
        res.show("res")
        length = abs(w - h) // 2
        box = (length, 0) if w > h else (0, length)
        res.paste(img, box)

        return res

    def resizeFree(self, w, h, retio=False) -> Image:
        if retio is True:
            return self.img.resize((self.w * w, self.h * h))
        return self.img.resize((w, h))

    def getPeopel(self, img):
        humanseg = hub.Module(name="deeplabv3p_xception65_humanseg")
        files = [img]
        results = humanseg.segmentation(data={"image": files})
        img = np.array(Image.open(img).convert("RGB"))
        mask = results[0]['data']
        # mask = np.stack((mask, mask, mask), axis=-1)
        w, h = mask.shape
        for ww in range(w):
            for hh in range(h):
                if mask[ww, hh]==False:
                    img[ww, hh, :] = 255
        res = Image.fromarray(img)
        res.show()
        res.save("res.jpg")





if __name__ == '__main__':
    img = '../res.jpg'

    iP = ImageProcess(img)
    test = 'test.jpg'
    # iP.resize(512, 512).save("img.jpg")
    iP.getPeopel(test)
    # iP.resizeFree(8, 6, True).show()