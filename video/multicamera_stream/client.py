import time
import imagezmq
from camera_config.camera import CameraStream


def run(camera):
    # setting camera name as client name
    client_name = str(camera)
    # CameraStream object for 
    source = CameraStream(src=camera, width=500, height=360).start()
    print(f'--- Client {client_name}---')
    # creating sender
    sender = imagezmq.ImageSender()

    # running camera feed loop
    time.sleep(2.0)  # allow camera sensor to warm up
    while True:  # send images as stream until Ctrl-C
        _ , image = source.read()
        sender.send_image(client_name, image)