"""
This is anki functions file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""

#pylint: disable = C0114

import requests


def create_deck(deck_name):
    """ Creates a deck with the name of our choosing """
    requests.post('http://127.0.0.1:8765', json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    })


def deck_names():
    """ Prints deck names (used for testing) """
    dico = requests.post('http://127.0.0.1:8765', json={
        "action": "deckNames",
        "version": 6,
    }).json()
    return [val1 for key1, val1 in dico.items()][0]


def delete_deck(decks):
    """ Deletes deck from a list of existing decks """
    requests.post('http://127.0.0.1:8765', json={
        "action": "deleteDecks",
        "version": 6,
        "params": {
            "decks": decks,
            "cardsToo": True,
        }
    })


def clear_deck(decks):
    """ Clears decks from a list of existing decks """
    delete_deck(decks)
    for deck in decks:
        create_deck(deck)


def cards_in_deck(deck):
    """ Prints all card IDs from a chosen deck """
    return requests.post('http://127.0.0.1:8765', json={
        "action": "findCards",
        "version": 6,
        "params": {
            "query": "deck:" + deck
        }
    }).json()


def synchro_ankiweb():
    """ Synchronizes local data with AnkiWeb """
    requests.post('http://127.0.0.1:8765', json={
        "action": "sync",
        "version": 6
    })


def basic_note(deck, front, back):
    """ Adds a "Basic"-modelled Anki card to a deck """
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic",
                "fields": {
                    "Front": front,
                    "Back": back,
                }
            }
        }
    })


def basic_reversed_note(deck, front, back):
    """ Adds a "Basic (and reversed card)"-modelled Anki card to a deck """
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic (and reversed card)",
                "fields": {
                    "Front": front,
                    "Back": back,
                }
            }
        }
    })


def basic_optional_reversed_note(deck, front, back, add_reverse):
    """ Adds a "Basic (optional reversed card)"-modelled Anki card to a deck """
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic (optional reversed card)",
                "fields": {
                    "Front": front,
                    "Back": back,
                    "Add Reverse": add_reverse,
                }
            }
        }
    })


def basic_typein_note(deck, front, back):
    """ Adds a "Basic (type in the answer)"-modelled Anki card to a deck """
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Basic (type in the answer)",
                "fields": {
                    "Front": front,
                    "Back": back,
                }
            }
        }
    })


def transform_for_cloze(sentence, hidden_words):
    """ Transforms a sentence to create a "Cloze"-modelled Anki card """
    new_sentence = ""
    number = 1
    position = 0
    while position < len(sentence):
        word_detected = False
        for word in hidden_words:
            if position + len(word) <= len(sentence) + 1 \
                    and sentence[position:position + len(word)] == word:
                word_detected = True
                new_sentence += "{{c" + str(number) + "::" + word + "}}"
                number += 1
                position += len(word)
        if not word_detected:
            new_sentence += sentence[position]
            position += 1
    return new_sentence


def cloze_note(deck, sentence, hidden_words):
    """ Adds a "Cloze"-modelled Anki card to a deck """
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Cloze",
                "fields": {
                    "Text": transform_for_cloze(sentence, hidden_words),
                }
            }
        }
    })
