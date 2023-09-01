import os, requests
from todo_app.data.Item import Item

myAPIKey = os.getenv('TRELLO_API_KEY')
myToken = os.getenv('TRELLO_TOKEN')
boardID = os.getenv('TRELLO_BOARD_ID')

#Implement get_trello_lists function
#Add error handling from trello API

def get_items():
    """
    Fetches all saved cards from Trello and creates a list of Items.

    Returns:
        list: The list of saved items.
    """
    payload = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=payload).json()

    items = []
    for list in trello_lists:
        for card in list['cards']:
            item = Item.from_trello_card(card, list)
            items.append(item)

    return items

def add_item(title):
    """
    Adds a new item by creating a new card with the specified title in Trello.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    payload_1 = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=payload_1).json()
    for list in trello_lists:
        list_name = list.get("name")
        if list_name == 'To Do':
            to_do_list_id = list.get("id")
            payload_2 = {'key': {myAPIKey}, 'token': {myToken}, 'name': {title}, 'idList': {to_do_list_id}}
            new_item = requests.post(f'https://api.trello.com/1/cards', data=payload_2).json()

    return new_item

def update_as_done(card_id):
    """
    Updates an existing card in Trello to Done. If no existing card matches the ID of the specified card, nothing is changed.

    Args:
        card: The card to update to Done.
    """
    payload_1 = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=payload_1).json()
    for list in trello_lists:
        list_name = list.get("name")
        if list_name == 'Done':
            done_list_id = list.get("id")
            payload_2 = {'key': {myAPIKey}, 'token': {myToken}, 'idList': {done_list_id}}
            done_item = requests.put(f'https://api.trello.com/1/cards/{card_id}', data=payload_2).json()

    return done_item

def delete_card(card_id):
    """
    Deletes an existing card in Trello. If no existing card matches the ID of the specified card, nothing is deleted.

    Args:
        card: The card to delete.
    """
    payload = {'key': {myAPIKey}, 'token': {myToken}}
    deleted_item = requests.delete(f'https://api.trello.com/1/cards/{card_id}', data=payload).json()

    return deleted_item
