import requests


# model_task = requests.post('http://127.0.0.1:8765', json={
#     "action": "createModel",
#         "version": 6,
#         "params": {
#             "modelName": "Task",
#             "inOrderFields": ["Name", "Duration", "Difficulty"],
#             "css": "Optional CSS with default to builtin css",
#             "cardTemplates": [
#                 {
#                     "Front": "Front html {{Name}}",
#                     "Back": "Back html  {{Duration}}"
#                 }
#             ]
#         }
# })
# model_fixed_task = requests.post('http://127.0.0.1:8765', json={
#     "action": "createModel",
#         "version": 6,
#         "params": {
#             "modelName": "Fixed Task",
#             "inOrderFields": ["Name", "Duration", "Difficulty", "Beginning date", "Recurring"],
#             "css": "Optional CSS with default to builtin css",
#             "cardTemplates": [
#                 {
#                     "Front": "Front html {{Name}}",
#                     "Back": "Back html  {{Duration}}"
#                 }
#             ]
#         }
# })
# model_mobile_task = requests.post('http://127.0.0.1:8765', json={
#     "action": "createModel",
#             "version": 6,
#             "params": {
#                 "modelName": "Mobile Task",
#                 "inOrderFields": ["Name", "Duration", "Difficulty", "Deadline", "Divisions"],
#                 "css": "Optional CSS with default to builtin css",
#                 "cardTemplates": [
#                     {
#                         "Front": "Front html {{Name}}",
#                         "Back": "Back html {{Duration}}"
#                     }
#                 ]
#             }
# })
# r = requests.post('http://127.0.0.1:8765', json={
#     "action": "modelNames",
#     "version": 6
# })
#
# print(r.json())
