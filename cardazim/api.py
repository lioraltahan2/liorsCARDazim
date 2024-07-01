from flask import Flask, jsonify
from server import run_server
from card_manager import CardManager
import argparse
from card_driver import CardDriver
from cards import Card
app = Flask(__name__)


def run_api_server(host, port, database_url):
    print(database_url)
    global manager
    manager = CardManager(database_url, None)
    app.run(host=host, port=port)


@app.route('/creators')
def get_creators():
    return manager.driver.GetCreators()


@app.route('/creators/<string:creator_name>/cards/unsolved')
def get_creator_unsolved(creator_name):
    return manager.driver.GetCreatorCards(creator_name, solved=False)


@app.route('/creators/<string:creator_name>/cards/solved')
def get_creator_solved(creator_name):
    return manager.driver.GetCreatorCards(creator_name, solved=False)


@app.route('/creators/<string:creator_name>/cards/<string:card_name>')
def get_card_by_creator_and_name(creator_name, card_name):
    card = manager.load(
        manager.get_identifier_by_creator_and_name(creator_name, card_name))
    dictionary = {"identifier": manager.get_identifier(card),
                  "card name": card.name,
                  "card creator": card.creator,
                  "card riddle": card.riddle,
                  "card solution": card.solution,
                  "image path": "{}/{}/image.png".format(manager.images_dir, manager.get_identifier(card))}
    return dictionary


@app.route('/creators/<string:creator_name>/cards/<string:card_name>/image.jpg')
def get_image_by_creator_and_name(creator_name, card_name):
    card: Card = manager.load(
        manager.get_identifier_by_creator_and_name(creator_name, card_name))
    return card.image.image


@app.route('/cards/find/<string:field>/<string:lookup_string>')
def find_cards_with_str(field, lookup_string):
    return manager.driver.get_cards_with_str(field, lookup_string)


@app.route('/cards/creator/<string:creator_name>/cards/<string:card_name>/solve/<string:solution>')
def solve_card(creator_name, card_name, solution):
    identifier = manager.get_identifier_by_creator_and_name(
        creator_name, card_name)
    card = manager.load(identifier)
    if card.solution != None:
        return "card alresady solved"
    response = "Solution is not correct"
    if card.image.decrypt(solution):
        response = "Solution is correct"
        manager.driver.add_solution(identifier, solution)
    return response


def get_args():
    parser = argparse.ArgumentParser(
        description='Server listening on given ip and port.')
    parser.add_argument('host', type=str,
                        help='the server\'s ip')
    parser.add_argument('port', type=int,
                        help='the server\'s port')
    parser.add_argument('db', type=str,
                        help='the desired db url')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and getting data from clients.
    '''
    args = get_args()
    try:
        run_api_server(args.host, args.port,
                       args.db)
        return 0
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == "__main__":
    main()
