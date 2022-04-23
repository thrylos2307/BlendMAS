import cv2
import requests
import base64
import json
import numpy as np
from cryptography.fernet import Fernet
from io import BytesIO
from PIL import Image
from helper import encode_decode_img
# Read the original image
img = cv2.imread('grey_img.png') 


# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
# Display Sobel Edge Detection Images
# cv2.imshow('Sobel X', sobelx)
# cv2.waitKey(0)
# cv2.imshow('Sobel Y', sobely)
# cv2.waitKey(0)
# cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
# cv2.waitKey(0)

# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
# Display Canny Edge Detection Image
cv2.imwrite('edge.jpg', edges)


### enter the number to encrypt image and create transaction
image = open('edge.jpg','rb').read()
message = input("enter key to encrypt image (Integer):")
# user='tushar.arya'
user=input("enter user name:")
port=input("enter the node port number that is active:")

# Instance the Fernet class with the key
fil = open('public_key/'+user+'_key.pem', 'rb')
key=fil.read()
fil.close()
fernet = Fernet(key)
image=np.array(Image.open(BytesIO(image)))
image=encode_decode_img(image, message)

encMessage = fernet.encrypt(message.encode())

# api call to create new transaction
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

url = 'http://localhost:'+port+'/transaction/new'
payload = json.dumps({"image": image,
"sender": user,
"recipient": "recipient-address",
"message":encMessage.decode()})
response = requests.post(url, data=payload, headers=headers)
print(response)


