import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps



def change_contrast(img, level):
    # Input is a Image type
    # use Image.fromarray() on numpy
    factor = (259 * (level + 255)) / (255 * (259 - level))
    def contrast(c):
        return 128 + factor * (c - 128)
    return img.point(contrast)


def change_sharpness(img, level):
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(level)
    return img


def adjust(img, blevel, slevel, clevel, colevel):
    # brightness
    benhance = ImageEnhance.Brightness(img)
    img = benhance.enhance(blevel)
    # sharpness
    img = change_sharpness(img, slevel)
    # contrast
    img = change_contrast(img, clevel)
    # color
    cenhance = ImageEnhance.Color(img)
    img = cenhance.enhance(colevel)
    return img

def binarize(img):
    thresh = 5

    maxval = 255

    im_bin = (img > thresh) * maxval

    return im_bin.astype('uint8')

def improveImage(img):
    # img = cv2.imread(img_dir, -1)
    # img = binarize(img)
    
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((12,12), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 25)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, 
                                 beta=255, norm_type=cv2.NORM_MINMAX, 
                                 dtype=cv2.CV_8UC1)
        

        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv2.merge(result_planes)
    result_norm = cv2.merge(result_norm_planes)
    return result_norm


def convert_image(image):
    img = improveImage(image)
    img = adjust(Image.fromarray(img), 
                  blevel=0.6, slevel=1, clevel=255, 
                  colevel=1)
    return img


def read_image(path, return_array=True, gray=False):
    image = Image.open(path)
    if gray:
        image = ImageOps.grayscale(image)
    if return_array:
        return image.__array__()
    
    return image


def get_digit_cords(image):
    bounding_boxes = {}
    # Apply the Component analysis function
    analysis = cv2.connectedComponentsWithStats(image,
                                                4,
                                            cv2.CV_32S)
    
    totalLabels, label_ids, values, centroid = analysis
    
    for i in range(1, totalLabels):
        # Area of the component
        area = values[i, cv2.CC_STAT_AREA]
    
        x = values[i, cv2.CC_STAT_LEFT]
        y = values[i, cv2.CC_STAT_TOP]
        w = values[i, cv2.CC_STAT_WIDTH]
        h = values[i, cv2.CC_STAT_HEIGHT]

        
        bounding_boxes[i] = (x,y,w,h)
    return bounding_boxes

def isolate_digits(image, digit_cords):
    digit_crops = []
    digit_sorted = sorted(digit_cords.values(),key=lambda x: (x[0]))
    
    for pos in digit_sorted:
        x,y,w,h = pos
        digit_crops.append(image[y:y+h,x:x+w])
    
    return digit_crops

def extract_digits(path, post_invert=True):
    '''
    Extract digits only from the images. 
    params:
    --------
    path : path of the image
    post_invert : (default : True) if image is already
                inverted then make it false.
    '''
    # 1. read image from path (op: array)
    img = read_image(path, gray=True)
    # 2. gaussian blur
    # kernal size (3,3) | (5,5) kernal causes extra thickness in digits
    # sigmaX = 5 is optimum to blur out all the grains
    img_blur  = cv2.GaussianBlur(img.__array__(), (3,3), 5)
    # 3. convert_image (op: PIL format)
    img_conv = convert_image(img_blur)
    # 4. invert image
    if post_invert:
        inverted = np.invert(img_conv.__array__())
    else:
        inverted = img_conv.__array__()
    # 5. get digits 
    # resize first
    inverted = cv2.resize(inverted, (64,64))
    digit_cords = get_digit_cords(inverted)
    
    # drawing the boxed version
    # plt.imshow(inverted, cmap='gray')
    # returning the original inverted image and digit_map
    return inverted, digit_cords


def get_digit_crops(path, post_invert=True):
    ori_img, digit_map = extract_digits(path, post_invert=post_invert)
    crops = isolate_digits(ori_img, digit_map)
    return crops


# digit_crops = get_digit_crops('pic/53.png')


# plt.imshow(digit_crops[0],cmap='gray')
# plt.show()