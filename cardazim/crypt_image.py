from PIL import Image
import hashlib
from Cryptodome.Cipher import AES
import io


class CryptImage():

    def __init__(self,
                 image: Image,           # The image
                 key_hash: bytes = None  # Hash of the key
                 ):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: str):
        '''
            Gets a path for an image and creates a non - encrypted image
        '''
        return cls(Image.open(path))

    def encrypt(self, key: str):
        '''
            Check that the image is already encrypted - If it is, does nothing
            O/W, encrypts the image and set hash_key to be 
        '''
        if self.key_hash != None:
            return
        w, h = self.image.size
        hash_object = hashlib.sha256(key.encode('utf-8'))
        key = hash_object.digest()
        hash_object = hashlib.sha256(key)
        self.key_hash = hash_object.digest()
        cipher = AES.new(key, AES.MODE_EAX, nonce=b'arazim')
        plain_img_bytearr = bytearray(self.image.tobytes())
        encrypted = cipher.encrypt(bytes(plain_img_bytearr[: (w * h) * 4]))
        self.image = Image.frombytes('RGBA', (w, h), bytearray(encrypted) +
                                     plain_img_bytearr[(w * h) * 4:])

    def decrypt(self, key: str):
        w, h = self.image.size
        hash_object = hashlib.sha256(key.encode('utf-8'))
        key = hash_object.digest()
        hash_object = hashlib.sha256(key)
        if hash_object.digest() != self.key_hash:
            return False
        cipher = AES.new(key, AES.MODE_EAX, nonce=b'arazim')
        enc_img_bytearr = bytearray(self.image.tobytes())
        plaintext = cipher.decrypt(bytes(enc_img_bytearr[: w * h * 4]))
        self.image = Image.frombytes('RGBA', (w, h), bytearray(plaintext) +
                                     enc_img_bytearr[w * h * 4:])
        self.key_hash = None
        return True
