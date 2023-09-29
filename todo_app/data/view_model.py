class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items

    @property
    def done_items(self):
        done_item_list = []
        for item in self._items:
            if item.status == 'Done':
                done_item_list.append(item)
        return done_item_list