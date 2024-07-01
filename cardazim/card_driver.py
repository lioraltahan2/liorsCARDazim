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

    def GetCreatorCards(self, creator, solved):
        pass


class DataBaseDriver(CardDriver):
    def __init__(self, url):
        client: CardDriver = pymongo.MongoClient(url)
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
        return list(self.cards.find({}, {'_id': 0, 'creator': 1}))

    def GetCreatorCards(self, creator, solved=None):
        if solved == True:
            return self.cards.find({'creator': creator, 'solution': {"$ne": None}})
        if solved == False:
            return self.cards.find({'creator': creator, 'solution': None})
        return self.cards.find({'creator': creator})

    def get_cards_with_str(self, field, lookup_string):
        return list(self.cards.find({"$contains": {field: lookup_string}}))

    def add_solution(self, identifier, solution):
        self.cards.updateOne({"identifier": identifier}, {"$set": {"solution": solution}}
                             )
