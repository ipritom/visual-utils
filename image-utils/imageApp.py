import cv2
import numpy as np

def read_image(source, mode=None, shape=None, rgb=False):
        '''
        OpenCV Image Reader with specified Shape.
        Unlike default OpenCV imshow() this script
        loads image in RGB by default.

        Paramerters:
        --------------
        source : image file path
        mode : Flags used for image file reading. 
               default : None
               grayscale : 0
        shape : <type : tuple> to resize image while 
                reading.
        rgb : <type : boolean> If True, image read with
              imread will be converted to RGB. OpneCV 
              read image in BGR. To read image at RGB 
              format keep mode = None (default).
        
        Returns:
        ----------
        image
        '''
        image = cv2.imread(source, mode)
        if shape!=None:
            image = cv2.resize(image,shape)

        if mode==None and rgb==True:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        return image

class Line:
    '''
    Data Structure class for holding starting (head) and
    ending (tail) coordinates of a Line.
    and tail point.
    '''
    def __init__(self,head,tail):
        self.head = head
        self.tail = tail
    
    def __str__(self) -> str:
        coord_str = f'{self.head} to {self.tail}'
        return coord_str

class Screen:
    '''
    Screen helps to draw lines on the loaded image.
    If preload=False it can be used as an image loader.
    '''
    def __init__(self, source, windowName='Untitled', mode=None, shape=None, preload=True):
        self.source = source
        self.windowName = windowName
        self.mode = mode 
        self.shape = shape
        self.image = None
        self.clone = None # to keep a clone on self image.
        self.EVENT_FLAG = False
        
        #loading image from source
        if preload:
            self.image = read_image(self.source, self.mode, self.shape)
            self.clone = self.image.copy()
        
        self.refPt = []
        self.DRAW_FLAG = False
        self.Lines = []
    
    def __call__(self) -> str:
        if self.image == None:
            self.image = read_image(self.source, self.mode, self.shape)
        return self.image
        
    def __str__(self) -> str:
        return self.source

    def load_image(self):
        self.image = read_image(self.source, self.mode, self.shape)
        self.clone = self.image.copy()

    def show(self):
        if self.EVENT_FLAG:
            cv2.imshow(self.windowName, self.image)
            cv2.setMouseCallback(self.windowName, self.draw_event)
        while True:
            cv2.imshow(self.windowName, self.image)
            #getting keys
            key = cv2.waitKey(1)
            # exit by key press q
            if key & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            # reset image with KeyPress 'r'
            elif key & 0xFF == ord('r'):
                self.image = read_image(self.source, self.mode, self.shape)
                self.clone = self.image.copy()
                self.Lines.clear()

            # undo image with KeyPress 'u'
            elif key & 0xFF == ord('u'):
                # taking fresh image
                self.image = read_image(self.source, self.mode, self.shape)
                self.Lines.pop()
                #TODO: put condition check - empty Lines list
                for line in self.Lines:
                    head = line.head
                    tail = line.tail
                    x, y = head
                    strXY = str(x)+", "+str(y)
                    cv2.putText(self.image, strXY, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (218,198,50), 2)
                    x, y = tail
                    strXY = str(x)+", "+str(y)
                    cv2.putText(self.image, strXY, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (218,198,50), 2)
                    cv2.line(self.image, head, tail, (0, 255, 0),2)
                self.clone = self.image.copy()
            # exit by closing window
            if cv2.getWindowProperty(self.windowName, cv2.WND_PROP_VISIBLE) <1:
                cv2.destroyAllWindows()
                break
    
    def add_event(self):
        # self.event = event
        self.EVENT_FLAG = True
    
    def draw_event(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt.append((int(x),int(y)))
            self.DRAW_FLAG = True
            # puting coordinate text at head (initially)
            strXY = str(x)+", "+str(y)
            cv2.putText(self.image, strXY, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (218,198,50), 2)
        if event == cv2.EVENT_MOUSEMOVE:
            # draw only if mouse is down
            if self.DRAW_FLAG:
                # draw the line
                self.image = self.clone.copy()
                cv2.line(self.image, (x,y),self.refPt[len(self.refPt)-2], (0, 255, 0),2)
                
        elif event == cv2.EVENT_LBUTTONUP:
            self.refPt.append((int(x),int(y)))
            self.image = self.clone.copy()
            # drawing line
            head = self.refPt[0]
            tail = self.refPt.pop()

            cv2.line(self.image, head, tail, (0, 255, 0), 2)
            ## creating a Line
            new_line = Line(head, tail)
            print(new_line)
            self.Lines.append(new_line)
            ## puting coordinate text
            # at head
            strXY = str( self.refPt[0][0])+", "+str( self.refPt[0][1])
            cv2.putText(self.image, strXY,  self.refPt[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (218,198,50), 2)
            # at tail
            strXY = str(x)+", "+str(y)
            cv2.putText(self.image, strXY, (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (218,198,50), 2)
            # reset parameters
            self.refPt.clear()
            self.DRAW_FLAG = False
            # updating image clone
            self.clone = self.image.copy()
                


######## testing app #######
if __name__ == "__main__":
    window = Screen('imgs/white_t.jpg',shape=(600,500))
    window.add_event()
    window.show()
  

