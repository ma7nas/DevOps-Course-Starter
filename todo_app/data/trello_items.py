import requests
from todo_app.data.Item import Item
from todo_app.data.trello_static_data_functions import myAPIKey, myToken, myBoardID, myToDoListID, myDoneListID

def get_trello_lists():
    """
    Fetches all lists and saved cards from Trello.

    Returns:
        list: All the items from Trello
    """
    payload = {'key': {myAPIKey()}, 'token': {myToken()}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{myBoardID()}/lists', params=payload).json()
    return trello_lists

def get_items():
    """
    Fetches all saved cards from Trello and instantiates an Item for each one.

    Returns:
        list: The list of saved items.
    """
    trello_lists = get_trello_lists()

    items = []
    for list in trello_lists:
        for card in list['cards']:
            item = Item.from_trello_card(card, list)
            items.append(item)

    return items

def add_item(name):
    """
    Adds a new item by creating a new card with the specified title in Trello.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    payload = {'key': {myAPIKey()}, 'token': {myToken()}, 'name': {name}, 'idList': {myToDoListID()}}
    new_item = requests.post(f'https://api.trello.com/1/cards', params=payload).json()

    return new_item

def update_as_done(card_id):
    """
    Updates an existing card in Trello to Done. If no existing card matches the ID of the specified card, nothing is changed.

    Args:
        card: The card to update to Done.
    """
    payload = {'key': {myAPIKey()}, 'token': {myToken()}, 'idList': {myDoneListID()}}
    done_item = requests.put(f'https://api.trello.com/1/cards/{card_id}', params=payload).json()

    return done_item

def delete_item(card_id):
    """
    Deletes an existing card in Trello. If no existing card matches the ID of the specified card, nothing is deleted.

    Args:
        card: The card to delete.
    """
    payload = {'key': {myAPIKey()}, 'token': {myToken()}}
    deleted_item = requests.delete(f'https://api.trello.com/1/cards/{card_id}',params=payload).json()

    return deleted_item
