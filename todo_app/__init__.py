import os, requests

myAPIKey = os.getenv('TRELLO_API_KEY')
myToken = os.getenv('TRELLO_TOKEN')
boardID = os.getenv('TRELLO_BOARD_ID')

payload = {'key': {myAPIKey}, 'token': {myToken}}
trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=payload).json()

to_do_list_exists = False
done_list_exists = False

for trello_list in trello_lists:
    list_name = trello_list.get("name")
    if list_name == "To Do":
        to_do_list_exists = True
    elif list_name == "Done":
        done_list_exists = True

if not done_list_exists:
    payload = {'key': {myAPIKey}, 'token': {myToken}, 'name': "Done", 'idBoard': {boardID}}
    new_list = requests.post(f'https://api.trello.com/1/lists', data=payload).json()

if not to_do_list_exists:
    payload = {'key': {myAPIKey}, 'token': {myToken}, 'name': "To Do", 'idBoard': {boardID}}
    new_list = requests.post(f'https://api.trello.com/1/lists', data=payload).json()