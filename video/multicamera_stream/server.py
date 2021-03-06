import cv2
import imagezmq


image_hub = imagezmq.ImageHub()

print("--- SERVER ON ---")

count = 0
while True:  # show streamed images until Ctrl-C
    camera_name, image = image_hub.recv_image()
    ########### DEBUG ##################
    print(camera_name, image)
    if len(image) == 0:
        print("NO")
    count += 1
    print(f'--- {count} ---')
    ####################################

    cv2.imshow(camera_name, image) # 1 window for each RPi
    image_hub.send_reply(b'OK')

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break