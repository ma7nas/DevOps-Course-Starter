import os, requests
from todo_app.data.Item import Item

myAPIKey = os.getenv('TRELLO_API_KEY')
myToken = os.getenv('TRELLO_TOKEN')
boardID = os.getenv('TRELLO_BOARD_ID')

#Implement get_trello_lists function

def get_cards():
    """
    Fetches all saved cards from Trello.

    Returns:
        list: The list of saved cards.
    """
    trello_params = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=trello_params).json()

    items = []
    for list in trello_lists:
        for card in list['cards']:
            item = Item.from_trello_card(card, list)
            items.append(item)

    return items

def add_card(title):
    """
    Adds a new card with the specified title to Trello.

    Args:
        title: The title of the card.

    Returns:
        card: The saved card.
    """
    trello_params = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=trello_params).json()
    for trello_list in trello_lists:
        list_name = trello_list.get("name")
        if list_name == 'To Do':
            to_do_list_id = trello_list.get("id")
            trello_card_data = {'key': {myAPIKey}, 'token': {myToken}, 'name': {title}, 'idList': {to_do_list_id}}
            new_card = requests.post(f'https://api.trello.com/1/cards', data=trello_card_data).json()

    return new_card

def update_as_done(card):
    """
    Updates an existing card in Trello to Done. If no existing card matches the ID of the specified card, nothing is changed.

    Args:
        card: The card to update to Done.
    """
    trello_params = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=trello_params).json()
    for trello_list in trello_lists:
        list_name = trello_list.get("name")
        if list_name == 'Done':
            done_list_id = trello_list.get("id")
            trello_card_data = {'key': {myAPIKey}, 'token': {myToken}, 'idList': {done_list_id}}
            done_card = requests.put(f'https://api.trello.com/1/cards/{card}', data=trello_card_data).json()

    return done_card

def delete_card(card):
    """
    Deletes an existing card in Trello. If no existing card matches the ID of the specified card, nothing is deleted.

    Args:
        card: The card to delete.
    """
    trello_card_data = {'key': {myAPIKey}, 'token': {myToken}}
    deleted_card = requests.delete(f'https://api.trello.com/1/cards/{card}', data=trello_card_data).json()

    return deleted_card
