from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.image import Image

import cv2
from pyzbar.pyzbar import decode


class BarcodeScanner(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.img = Image()
        self.label = Label(text="Scan a barcode...")
        self.add_widget(self.img)
        self.add_widget(self.label)

        # Start the camera
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            for code in decode(frame):
                self.label.text = f"Detected: {code.data.decode('utf-8')}"
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.img.texture = img_texture


class BarcodeApp(App):
    def build(self):
        return BarcodeScanner()

if __name__ == '__main__':
    BarcodeApp().run()
