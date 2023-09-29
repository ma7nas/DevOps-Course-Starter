from todo_app.data.Item import Item
from todo_app.data.view_model import ViewModel

def test_view_model_filter_done_items():
    # Arrange
    items = [
        Item('1', 'Make breakfast', 'Done'),
        Item('2', 'Make lunch', 'To Do'),
        Item('3', 'Make dinner', 'To Do'),
        Item('4', 'Make tea', 'Done')
    ]

    view_model = ViewModel(items)
    
    # Act
    done_item_list = view_model.done_items

    # Assert
    assert len(done_item_list) == 2
    assert done_item_list[0].status == 'Done'
    assert done_item_list[1].status == 'Done'