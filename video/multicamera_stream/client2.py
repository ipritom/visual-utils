import socket
import time
import imagezmq

from camera_config.camera import CameraStream

camera1 = "" # camera rtsp link here
camera2 = "" # camera rtsp link here

client_name = camera2 # send RPi hostname with each image
source = CameraStream(src=camera2, width=500, height=360).start()

sender = imagezmq.ImageSender()
time.sleep(2.0)  # allow camera sensor to warm up

while True:  # send images as stream until Ctrl-C
    _ , image = source.read()
    sender.send_image(client_name, image)

    # print("SEND SUCCESS")