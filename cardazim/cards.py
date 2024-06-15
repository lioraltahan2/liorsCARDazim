from crypt_image import CryptImage
from PIL import Image
import struct


class Card:

    def __init__(self,
                 name: str,              # The cards name
                 creator: str,           # The card creator's name
                 image: CryptImage,      # The card's image
                 riddle: str,            # The card's riddle
                 solution: str = None    # The solution for the riddle
                 ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return "<Card name={}, creator={}>".format(self.name, self.creator)

    def __str__(self):
        return "Card {} by {} \n riddle: {} \n solution: {}".format(self.name, self.creator, self.riddle,
                                                                    self.solution if self.solution != None
                                                                    else "unsolved")

    @classmethod
    def create_from_path(cls, name: str, creator: str, path: str, riddle: str, solution: str):
        return cls(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        series = bytearray([])
        # Add name :
        series += bytearray(struct.pack('N', len(self.name)))
        series += self.name.encode('utf-8')
        # Add Creator:
        series += bytearray(struct.pack('N', len(self.creator)))
        series += self.creator.encode('utf-8')
        # Add Image:
        w, h = self.image.image.size
        series += bytearray(struct.pack('N', w))
        series += bytearray(struct.pack('N', h))
        series += bytearray(self.image.image.tobytes())
        # Add Riddle:
        series += bytearray(struct.pack('N', len(self.riddle)))
        series += self.riddle.encode('utf-8')
        return bytes(series)

    @classmethod
    def deserialize(cls, data):
        index = 0
        # Get name:
        len = struct.unpack('N', data[index: index + 8])[0]
        index += 8
        name = data[index: index + len].decode('utf-8')
        index += len
        # Get Creator:
        len = struct.unpack('N', data[index: index + 8])[0]
        index += 8
        creator = data[index: index + len].decode('utf-8')
        index += len
        # Get Image:
        w = struct.unpack('N', data[index: index + 8])[0]
        index += 8
        h = struct.unpack('N', data[index: index + 8])[0]
        index += 8
        image = CryptImage(Image.frombytes(
            'RGBA', (w, h), data[index: index + (w * h * 4)]))
        index += w * h * 4
        # Add Riddle:
        len = struct.unpack('N', data[index: index + 8])[0]
        index += 8
        riddle = data[index: index + len].decode('utf-8')
        return cls(name, creator, image, riddle)
