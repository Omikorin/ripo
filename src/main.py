import cv2
from System import System



# camera = addCamera(6.6, 8.8, 1.95, 0.7, 126) # pixel 7 pro

sys = System()
sys.configure(23.5, 15.6, 10, 0.7, 5, 2.5)
image = cv2.imread('test-apsc.jpg')
sys.load_image(image)
sys.run_test()