# imageApp
imageApp script helps to draw lines on the loaded image. The Screen class can be be used as image loader if `preload=False`.

## How to use
Copy and paste imageApp.py file to your project directory. Then load and run as following:
```python
from imageApp import Screen

window = Screen('imgs/white_t.jpg',shape=(600,500))
window.add_event()
window.show()
```
## Troubleshoot
May raise following errors which is related to OpenCV version issue.

```
qt.qpa.plugin: Could not find the Qt platform plugin "xcb" in ""
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
```
Problem encountered with opencv-python 4.5.4.60

Problem solved with opencv-python 4.5.5.62

# OCR 
Helper function for isolating hand-written digits. Tested on digits-on-paper images. It works fine if digits are not overlapped. Solved with connected component algorithm. Utilized OpenCV `connectedComponentsWithStats` function.

