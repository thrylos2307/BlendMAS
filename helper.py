from cryptography.fernet import Fernet
import sys
from env import mydb

mycursor = mydb.cursor()


def create_key_pair(user_name):
    key = Fernet.generate_key() 
    
    sql = "INSERT INTO user_info(email, private_key) VALUES (%s, %s)"
    val = (user_name, key)
    mycursor.execute(sql, val)
    mydb.commit()
    
    with open('public_key/'+user_name+'_key.pem','wb') as f:
        f.write(key)
        
    return "public key is save for user: "+user_name+", use this key to send your data securely"


def encode_decode_img(image,key):
# performing XOR operation on each value of bytearray
    for index, values in enumerate(image):
        image[index] = values ^ int(key)

    return str(image)

