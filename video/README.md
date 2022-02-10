# Multi-Camera Live Streaming

For accessing multi-camera feeds [imageZMQ](https://github.com/jeffbass/imagezmq) is used.

## How to Use
Enter Camera IP in `camera1.py` and `camera2.py`. 

Edit the `camerahub.sh` file. Enter the `conda.sh` source.

It is good to run `server.py` at first. To run server:

```
python server.py
```
To initiate client.

```
bash ./camerahub.sh
```

# Network Video Recorder (NVR)

A network video recorder (NVR) is a specialized computer system that includes a software program[1] that records video in a digital format to a disk drive, USB flash drive, SD memory card or other mass storage device.

`nvr.py` attempts to replicate the computer system. 