"""
This is anki functions testing file for dev

   Jean-Loup Raymond & Benjamin Roulin & Aaron Fargeon
   ENPC - (c)

"""
# pylint: disable=E0401, C0114

from anki import create_deck, deck_names, \
    delete_deck, clear_deck, \
    cards_in_deck, synchro_ankiweb, \
    basic_note, basic_reversed_note, basic_optional_reversed_note, \
    basic_typein_note, cloze_note

decks_to_create = ["AnaCS", "MMC1", "PhyStat", "Optimisation", "Programmation"]

for deck_to_create in decks_to_create:
    create_deck(deck_to_create)

print(deck_names())

basic_note("AnaCS", "Basic AnaCS ?", "Yes, basic AnaCS.")
basic_note("AnaCS", "Still basic AnaCS ?", "Yes, still basic AnaCS.")
basic_typein_note("MMC1", "Type in MMC1 ?", "Yes, type in MMC1.")
basic_reversed_note("MMC1", "Reversed MMC1 ?", "Yes, reversed MMC1.")
basic_note("MMC1", "Basic MMC1 ?", "Yes, basic MMC1.")
basic_note("MMC1", "Still basic MMC1 ?", "Yes, still basic MMC1.")
basic_optional_reversed_note(
    "Optimisation", "Opt Reverse Opti ?", "Yes, opt reverse Opti.", "The reverse.")
basic_note("PhyStat", "Basic PhyStat ?", "Yes, basic PhyStat.")
cloze_note(
    "PhyStat",
    "Well yes, I would like a cloze note for the PhyStat please my dear sir, thank you !",
    ["yes", "would", "cloze", "PhyStat", "my dear sir"])
cloze_note("Programming", "No need to go to the exam to validate", ["go to the exam"])

clear_deck(["PhyStat"])
delete_deck(["Programming"])

print(cards_in_deck("AnaCS"))

synchro_ankiweb()
