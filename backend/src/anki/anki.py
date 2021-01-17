import requests


def create_deck(deck_name):
    requests.post('http://127.0.0.1:8765', json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    })


def deck_names(Ids=False):
    if Ids:
        return requests.post('http://127.0.0.1:8765', json={"action": "deckNamesAndIds", "version": 6, }).json()
    return requests.post('http://127.0.0.1:8765', json={"action": "deckNames", "version": 6, }).json()


def delete_deck(decks):
    requests.post('http://127.0.0.1:8765', json={
        "action": "deleteDecks",
        "version": 6,
        "params": {
            "decks": decks,
            "cardsToo": True,
        }
    })


def clear_deck(decks):
    delete_deck(decks)
    for deck in decks:
        create_deck(deck)


def cards_in_deck(deck):
    return requests.post('http://127.0.0.1:8765', json={
        "action": "findCards",
        "version": 6,
        "params": {
            "query": "deck:" + deck
        }
    }).json()


def synchro_ankiweb():
    requests.post('http://127.0.0.1:8765', json={
        "action": "sync",
        "version": 6
    })


def basic_note(deck, front, back):
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
    new_sentence = ""
    number = 1
    position = 0
    while position < len(sentence):
        word_detected = False
        for word in hidden_words:
            if position + len(word) <= len(sentence) + 1 and sentence[position:position + len(word)] == word:
                word_detected = True
                new_sentence += "{{c" + str(number) + "::" + word + "}}"
                number += 1
                position += len(word)
        if not word_detected:
            new_sentence += sentence[position]
            position += 1
    return new_sentence


def cloze_note(deck, sentence, hidden_words):
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


