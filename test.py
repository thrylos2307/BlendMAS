# import rsa
# import sys
# from env import mydb

# mycursor = mydb.cursor()
from PIL import Image
import base64
from cryptography.fernet import Fernet
import numpy as np
key = Fernet.generate_key() 
print(type(key))
message = input("enter key:")
# Instance the Fernet class with the key
fin = open('public_key/public_key.pem', 'wb')
 
# # writing encrypted data in image
fin.write(key)
fin.close()
fernet = Fernet(key)

encMessage = fernet.encrypt(message.encode())
fin = open('encrypt.txt', 'wb')
 
# # writing encrypted data in image
fin.write(encMessage)
fin.close()

# public_key, private_key = rsa.newkeys(1024)

# user_name=input("enter the username:")
# publicKeyPkcs1PEM = public_key.save_pkcs1().decode('utf8') 
# privateKeyPkcs1PEM = private_key.save_pkcs1().decode('utf8') 
# with open('public_key/'+user_name+'_public_key.pem','w+') as f:
#     f.write(publicKeyPkcs1PEM)

# with open('private_key/'+user_name+'_private_key.pem','w+') as f:
#     f.write(privateKeyPkcs1PEM)
#     sql = "INSERT INTO user_info(email, private_key) VALUES (%s, %s)"
#     val = (user_name, privateKeyPkcs1PEM)
#     mycursor.execute(sql, val)
#     mydb.commit()

# mydb.commit()

# file1 = open('public_key/'+user_name+'_public_key.pem',"r+") 
# p1=file1.read()
# publickey=rsa.PublicKey.load_pkcs1(p1.encode('utf8')) 

# file1 = open('private_key/'+user_name+'_private_key.pem',"r+") 
# p1=file1.read()
# privatekey=rsa.PrivateKey.load_pkcs1(p1.encode('utf8')) 

# def encrypt_text(plain_text):
#     plain_text = plain_text.encode('utf8')
#     encrypted_text = rsa.encrypt(plain_text, publickey)
#     return encrypted_text

# def decrypt_text(encrypted_text):
#     decrypted_text = rsa.decrypt(encrypted_text, privatekey)
#     return decrypted_text.decode('utf8')

# # testing


# # Read the original image
# key = int(input('Enter Key for encryption of Image : '))
# # print(plain_text)

# encrypted_text = encrypt_text(str(key))
# print("Encrypted text is = %s" %(encrypted_text))

# decrypted_text = decrypt_text(encrypted_text)
# print("Decrypted text is = %s" %(decrypted_text),"\n\n")
from io import BytesIO
# # # print(public_key,'\n',private_key)
fin = open('lion.jpg', 'rb')    
# storing image data in variable "image"
image = fin.read()
fin.close()
# image = Image.open('edge.jpg')
# print(type(image))
# converting image into byte array to
# perform encryption easily on numeric data
# image = bytearray(image)
image=np.array(Image.open(BytesIO(image)))
print(type(image))
# performing XOR operation on each value of bytearray
for index, values in enumerate(image):
    image[index] = values ^ int(message)

# opening file for writing purpose
fin = open('en.png', 'wb')
 
# writing encrypted data in image
fin.write(image)
fin.close()
print('Encryption Done...')



# fin = open('en.png', 'rb')
# # storing image data in variable "image"
# image = fin.read()
# fin.close()
 
# # converting image into byte array to perform decryption easily on numeric data
# image = bytearray(image)

# # performing XOR operation on each value of bytearray
# for index, values in enumerate(image):
#     image[index] = values ^ key

# # opening file for writing purpose
# fin = open('dec.png', 'wb')
 
# # writing decryption data in image
# fin.write(image)
# fin.close()
# print('Decryption Done...')
from cryptography.fernet import Fernet
# file1 = open('public_key/tushar_key.pem',"rb") 
# key=file1.read()

# fernet = Fernet(key)
# file1 = open('encrypt.txt',"rb") 
# encMessage=file1.read()

# key= fernet.decrypt(encMessage).decode()
 

fin = open('en.png', 'rb')
# storing image data in variable "image"
image = fin.read()
fin.close()

print(image)

# converting image into byte array to perform decryption easily on numeric data
image = bytearray(image)

# performing XOR operation on each value of bytearray
for index, values in enumerate(image):
    image[index] = values ^ int(21)

# opening file for writing purpose
fin = open('dec.png', 'wb')
 
# writing decryption data in image
fin.write(image)
fin.close()
print('Decryption Done...')