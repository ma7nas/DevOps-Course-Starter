import os, requests

def myAPIKey():
    return os.getenv('TRELLO_API_KEY')

def myToken():
    return os.getenv('TRELLO_TOKEN')

def myBoardID():
    return os.getenv('TRELLO_BOARD_ID')

def myToDoListID():
    return os.getenv('TRELLO_TODO_LIST_ID')
        
def myDoneListID():
    return os.getenv('TRELLO_DONE_LIST_ID')