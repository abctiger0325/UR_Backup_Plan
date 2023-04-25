import tkinter as tk
from pygrabber.dshow_graph import FilterGraph
import cv2


class CameraApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # get available camera devices
        self.camera_devices = self.get_camera_devices()

        # create dropdown menus
        self.camera1_label = tk.Label(self, text="Camera 1:")
        self.camera1_label.pack(side="left")
        self.camera1_var = tk.StringVar(value=list(self.camera_devices.keys())[0])
        self.camera1_dropdown = tk.OptionMenu(self, self.camera1_var, *self.camera_devices)
        self.camera1_dropdown.pack(side="left")

        self.camera2_label = tk.Label(self, text="Camera 2:")
        self.camera2_label.pack(side="left")
        self.camera2_var = tk.StringVar(value=list(self.camera_devices.keys())[0])
        self.camera2_dropdown = tk.OptionMenu(self, self.camera2_var, *self.camera_devices)
        self.camera2_dropdown.pack(side="left")

        # create update button
        self.update_button = tk.Button(self, text="Update", command=self.update_cameras)
        self.update_button.pack()

        # create camera display windows
        self.camera1_window = tk.Label(self, text="Camera 1")
        self.camera1_window.pack()
        self.camera2_window = tk.Label(self, text="Camera 2")
        self.camera2_window.pack()

    def get_camera_devices(self):
        # get number of available camera devices
        devices = FilterGraph().get_input_devices()

        available_cameras = {}

        for device_index, device_name in enumerate(devices):
            available_cameras[device_name] = device_index

        return available_cameras

    def update_cameras(self):
        # get selected camera devices
        camera1_index = self.camera_devices[self.camera1_var.get()]
        camera2_index = self.camera_devices[self.camera2_var.get()]

        # create filter graph and set camera sources
        # create capture objects
        capture1 = cv2.VideoCapture(camera1_index)
        capture2 = cv2.VideoCapture(camera2_index)

        # read frames and display in camera windows
        while True:
            ret1, frame1 = capture1.read()
            if ret1:
                frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                photo1 = tk.PhotoImage(data=cv2.imencode(".png", frame1)[1].tobytes())
                self.camera1_window.config(image=photo1)
                self.camera1_window.image = photo1

        # ret2, frame2 = capture2.read()
        # if ret2:
        #     frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        #     photo2 = tk.PhotoImage(data=cv2.imencode(".png", frame2)[1].tobytes())
        #     self.camera2_window.config(image=photo2)
        #     self.camera2_window.image = photo2


root = tk.Tk()
app = CameraApp(master=root)
app.mainloop()
