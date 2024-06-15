import sys
import pytest
import socket
from mock_socket import MockSocket
import hashlib


@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', MockSocket)


'''
    Test the the client transfer the properties of the card correctly
'''


def test_run_client(mock_socket):
    sys.path.append(sys.path[0][: len(sys.path[0]) - 5] + "cardazim")
    import client
    from cards import Card
    ip = '127.0.0.1'
    host = '1300'
    name = 'my_card'
    creator = 'nobody'
    path = sys.path[0] + '/image.png'
    riddle = 'cant think of one'
    solution = 'hard to think of a solution when you dont know the question'
    client.send_data(ip, host, name, creator, path, riddle, solution)
    card = Card.deserialize((MockSocket.sent_data))
    assert MockSocket.addr == (ip, host)
    assert card.name == name
    assert card.creator == creator
    assert card.riddle == card.riddle
    assert card.solution == None
    assert card.image.key_hash == None
