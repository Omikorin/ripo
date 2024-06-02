import cv2
from System import System

# camera = addCamera(6.6, 8.8, 1.95, 0.7, 126) # pixel 7 pro

sys = System()
sys.load_image('test-apsc.jpg')
sys.configure(23.5, 15.6, 10, 0.7, 5, 2.5)
sys.run_test()
