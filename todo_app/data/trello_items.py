import os, requests

myAPIKey = os.getenv('TRELLO_API_KEY')
myToken = os.getenv('TRELLO_TOKEN')
boardID = os.getenv('TRELLO_BOARD_ID')

def get_cards():
    """
    Fetches all saved cards from Trello.

    Returns:
        list: The list of saved cards.
    """
    trello_params = {'key': {myAPIKey}, 'token': {myToken}, 'cards': 'open', 'card_fields': 'name'}
    trello_lists = requests.get(f'https://api.trello.com/1/boards/{boardID}/lists', params=trello_params).json()

    cards = []
    for trello_list in trello_lists:
        card_status = trello_list.get("name")
        for card in trello_list['cards']:
            card["status"] = card_status
            cards.append(card)
    return cards

def get_card(id):
    """
    Fetches the saved card with the specified ID from Trello.

    Args:
        id: The ID of the card.

    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    cards = get_cards()
    return next((card for card in cards if card['id'] == int(id)), None)


def add_card(title):
    """
    Adds a new card with the specified title to Trello.

    Args:
        title: The title of the card.

    Returns:
        card: The saved card.
    """
    cards = get_cards()

    # Determine the ID for the item based on that of the previously added item
    id = cards[-1]['id'] + 1 if cards else 0

    card = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    cards.append(card)
    session['items'] = cards

    return card

def save_card(card):
    """
    Updates an existing card in Trello. If no existing card matches the ID of the specified card, nothing is saved.

    Args:
        card: The card to save.
    """
    existing_cards = get_cards()
    updated_cards = [card if card['id'] == existing_card['id'] else existing_card for existing_card in existing_cards]

    session['items'] = updated_cards

    return card

def delete_card(card):
    """
    Deletes an existing card in the session. If no existing card matches the ID of the specified card, nothing is deleted.

    Args:
        card: The card to delete.
    """
    existing_cards = get_cards()

    for index, existing_card in enumerate(existing_cards):
      if str(existing_card['id']) == card:
          del existing_cards[index] 
          break
    session['items'] = existing_cards
    return card
