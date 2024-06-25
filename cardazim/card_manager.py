from cards import Card
from crypt_image import CryptImage
import json
from PIL import Image
import os


class CardManager:

    def get_identifier(self, card):
        return "{}/{}".format(card.creator, card.name)

    def save(self, card: Card, dir_path: str):
        dictionary = {"card name": card.name,
                      "card creator": card.creator,
                      "card riddle": card.riddle,
                      "card solution": card.solution,
                      "image path": "{}/{}/image.jpg".format(dir_path, self.get_identifier(card))}
        json_object = json.dumps(dictionary, indent=5)
        path = os.path.normpath(
            "{}/{}".format(dir_path, self.get_identifier(card)))
        print(path)
        try:
            os.makedirs(path)
        except:
            pass
        with open("{}/{}/metadata.json".format(dir_path, self.get_identifier(card)), "w") as json_file:
            json_file.write(json_object)
        card.image.image.save(
            "{}/{}/image.png".format(dir_path, self.get_identifier(card)))

    def load(self, identifier: str, dir_path: str):
        json_object = None
        with open("{}/{}/metadata.json".format(dir_path, identifier), 'r') as openfile:
            json_object = json.load(openfile)
        name = json_object["card name"]
        creator = json_object["card creator"]
        riddle = json_object["card riddle"]
        solution = json_object["card solution"]
        image_path = json_object["image path"]
        return Card.create_from_path(
            name, creator, image_path, riddle, solution)
