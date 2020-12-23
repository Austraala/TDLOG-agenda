import requests


def create_deck(deck_name):
    requests.post('http://127.0.0.1:8765', json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
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

def cloze_note(deck, text):
    requests.post('http://127.0.0.1:8765', json={
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck,
                "modelName": "Cloze",
                "fields": {
                    "Text": text,
                }
            }
        }
    })



decks_to_create = ["AnaCS", "MMC1", "PhyStat", "Optimisation"]

for deck_to_create in decks_to_create:
    create_deck(deck_to_create)

names = requests.post('http://127.0.0.1:8765', json={
    "action": "deckNamesAndIds",
    "version": 6,
})

print(names.json())




# print(requests.post('http://127.0.0.1:8765', json={
#         "action": "modelNamesAndIds",
#         "version": 6,
#     }).json())

requests.post('http://127.0.0.1:8765', json={
    "action": "deleteDecks",
    "version": 6,
    "params": {
        "decks": decks_to_create,
        "cardsToo": True
    }
})

names = requests.post('http://127.0.0.1:8765', json={
    "action": "deckNames",
    "version": 6,
})

print(names.json())
