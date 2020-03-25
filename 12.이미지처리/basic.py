import cv2
import requests
import numpy
from PIL import Image

# PIL RGB, width: height
# OPENCV BGR height: width

pil_image = Image.open("sample.jpg")
opencv_image = numpy.array(pil_image)
opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

cv2.imshow("A", opencv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()