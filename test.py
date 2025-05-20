from PIL import Image
import numpy as np

imageRGB = Image.open("texture1.png").convert("RGB") 
imageData = np.asarray(imageRGB)


