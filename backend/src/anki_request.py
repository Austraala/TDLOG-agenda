import requests

# "action": "addNote",
    # "version": 6,
    # "params": {
    #     "note": {
    #         "deckName": "Default",
    #         "modelName": "Basic",
    #         "fields": {
    #             "Front": "front content",
    #             "Back": "back content"
    #         },
    #         "tags": [
    #             "yomichan"
    #         ],
    #         "audio": {
    #             "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
    #             "filename": "yomichan_ねこ_猫.mp3",
    #             "skipHash": "7e2c2f954ef6051373ba916f000168dc",
    #             "fields": [
    #                 "Front"
    #             ]
    #         }
    #     }
    # }

r = requests.post('http://127.0.0.1:8765', json={
    "action": "createModel",
        "version": 6,
        "params": {
            "modelName": "Task",
            "inOrderFields": ["Name", "Duration", "Difficulty"],
            "css": "Optional CSS with default to builtin css",
            "cardTemplates": [
                {
                    "Front": "Front html {{Name}}",
                    "Back": "Back html  {{Duration}}"
                }
            ]
        }
})
r = requests.post('http://127.0.0.1:8765', json={
    "action": "createModel",
        "version": 6,
        "params": {
            "modelName": "Fixed Task",
            "inOrderFields": ["Name", "Duration", "Difficulty", "Beginning date", "Recurring"],
            "css": "Optional CSS with default to builtin css",
            "cardTemplates": [
                {
                    "Front": "Front html {{Name}}",
                    "Back": "Back html  {{Duration}}"
                }
            ]
        }
})
r = requests.post('http://127.0.0.1:8765', json={
    "action": "createModel",
            "version": 6,
            "params": {
                "modelName": "Mobile Task",
                "inOrderFields": ["Name", "Duration", "Difficulty", "Deadline", "Divisions"],
                "css": "Optional CSS with default to builtin css",
                "cardTemplates": [
                    {
                        "Front": "Front html {{Name}}",
                        "Back": "Back html  {{Duration}}"
                    }
                ]
            }
})
r = requests.post('http://127.0.0.1:8765', json={
    "action": "modelNames",
    "version": 6
})

print(r.json())
