from abc import ABC, abstractmethod
import os
import pymongo


class CardDriver(ABC):
    @abstractmethod
    def __init__(self, url):
        pass

    def Save(self, card):
        pass

    def Load(self, identifier):
        pass

    def GetCreators(self):
        pass

    def GetCreatorCards(self, creator):
        pass


class DataBaseDriver(CardDriver):
    def __init__(self, url):
        client = pymongo.MongoClient(url)
        self.cards = client["cardazim"].cards

    def Save(self, card):
        if (self.cards.find_one({'identifier': card['identifier']})):
            print(
                "Could not save card since there is already a card with this identifier")
            return
        self.cards.insert_one(card)

    def Load(self, identifier):
        return self.cards.find_one({'identifier': identifier})

    def GetCreators(self):
        self.cards['creator']

    def GetCreatorCards(self, creator):
        self.cards.find({'creator': creator})
