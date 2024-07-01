from cards import Card
from crypt_image import CryptImage
from card_driver import DataBaseDriver
import json
from PIL import Image
import os


class CardManager:

    def __init__(self, database_url: str, images_dir: str):
        self.driver = self.get_driver(database_url)
        self.images_dir = images_dir

    def get_driver(self, database_url):
        return DataBaseDriver(database_url)

    def get_identifier(self, card):
        return "{}/{}".format(card.creator, card.name)

    def get_identifier_by_creator_and_name(self, creator, name):
        return "{}/{}".format(creator, name)

    def save(self, card: Card):
        dictionary = {"identifier": self.get_identifier(card),
                      "name": card.name,
                      "creator": card.creator,
                      "riddle": card.riddle,
                      "solution": card.solution,
                      "image path": "{}/{}/image.png".format(self.images_dir, self.get_identifier(card))}
        self.driver.Save(dictionary)
        path = os.path.normpath(
            "{}/{}".format(self.images_dir, self.get_identifier(card)))
        try:
            os.makedirs(path)
        except:
            pass
        card.image.image.save(
            "{}/{}/image.png".format(self.images_dir, self.get_identifier(card)))

    def load(self, identifier: str):
        dict = self.driver.Load(identifier)
        name = dict["name"]
        creator = dict["creator"]
        riddle = dict["riddle"]
        solution = dict["solution"]
        image_path = dict["image path"]
        print(image_path)
        return Card.create_from_path(
            name, creator, image_path, riddle, solution)
