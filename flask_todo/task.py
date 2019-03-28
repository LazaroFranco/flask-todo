import datetime
# A timestamp of when they were created DONE
# A boolean marking the item as completed or not DONE
# Text of the actual to-do item DONE

class Item():


    count = 1
    def __init__(self, task):
        self.task = task
        self.task_timestamp = datetime.datetime.now()
        self.completed = False
        self.id = Item.count
        Item.count += 1
