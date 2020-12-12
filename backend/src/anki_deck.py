import requests


def create_deck(deck_name):
    requests.post('http://127.0.0.1:8765', json={
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": deck_name
        }
    })

decks_to_create = ["AnaCS", "MMC1", "PhyStat", "Optimisation"]

for deck_to_create in decks_to_create:
    create_deck(deck_to_create)

names = requests.post('http://127.0.0.1:8765', json={
    "action": "deckNames",
    "version": 6,
})

print(names.json())

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
