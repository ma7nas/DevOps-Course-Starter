import os, requests

myAPIKey = os.getenv('TRELLO_API_KEY')
myToken = os.getenv('TRELLO_TOKEN')
boardID = os.getenv('TRELLO_BOARD_ID')

toDoListID = ""     
doneListID = ""

#Add error handling from trello API

def get_trello_lists():
    """
    Fetches all lists and saved cards from Trello.

    Returns:
        list: All the items from Trello
    """
    payload = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=payload).json()
    return trello_lists

trello_lists = get_trello_lists()

for list in trello_lists:
    list_name = list.get("name")
    if list_name == "To Do":
        toDoListID = list.get("id")
    elif list_name == "Done":
        doneListID = list.get("id")