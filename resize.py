from PIL import Image
import os
import threading
from queue import Queue
import time

FILEPATH = "../Dataset_Palace_Museum"
OUT = "./Dataset_Palace_Museum"


class Producer(threading.Thread):
    def __init__(self, queue_dynastry, queue_image):
        threading.Thread.__init__(self)
        self.queue_dynastry = queue_dynastry
        self.queue_image = queue_image

    def run(self):
        while 1:
            if self.queue_dynastry.empty():
                break

            file = self.queue_dynastry.get()
            for image in os.listdir(FILEPATH + "/"+ file):

                self.queue_image.put(file + "/" + image)


class Consumer(threading.Thread):
    def __init__(self, queue_dynastry, queue_image):
        threading.Thread.__init__(self)
        self.queue_dynastry = queue_dynastry
        self.queue_image = queue_image

    def run(self):
        while 1:
            if self.queue_image.empty() and self.queue_dynastry.empty():
                break

            file = self.queue_image.get()

            out = OUT + "/" + file
            image = Image.open(FILEPATH + "/" + file).convert("RGB")
            w, h = image.size
            background = Image.new("RGB", size=(max(w, h), max(w, h)), color=(127, 127, 127))

            length = int(abs(w - h) // 2)
            box = (length, 0) if w < h else (0, length)
            background.paste(image, box)
            image_data = background.resize((224, 224), resample=Image.LANCZOS, reducing_gap=3)
            image_data.save(out)
            print(out)


def main():
    queue_dynastry = Queue()
    queue_image = Queue()
    files = os.listdir(FILEPATH)
    if not os.path.exists(OUT):
        os.mkdir(OUT)
    for file in files:
        if not os.path.exists(OUT + "/" + file):
            os.mkdir(OUT + "/" + file)
        queue_dynastry.put(file)

    for i in range(3):
        producer = Producer(queue_dynastry, queue_image)
        producer.start()

    time.sleep(3)
    for i in range(8):
        consumer = Consumer(queue_dynastry, queue_image)
        consumer.start()


if __name__ == '__main__':
    main()

