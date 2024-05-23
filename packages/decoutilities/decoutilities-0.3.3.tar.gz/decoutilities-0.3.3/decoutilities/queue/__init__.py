import datetime

class Queue:
    def __init__(self):
        self.queue = []
        self.log = []

    def add_item(self, item):
        self.queue.append(item)
        self.log_action('ADD', item)

    def remove_item(self):
        if self.queue:
            item = self.queue.pop(0)
            self.log_action('REMOVE', item)
            return item
        else:
            return None

    def check_item(self):
        if self.queue:
            item = self.queue[0]
            self.log_action('CHECK', item)
            return item
        else:
            return None

    def clear_queue(self):
        self.queue = []
        self.log_action('CLEAR', 'Queue cleared')

    def log_action(self, action, item):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{timestamp}] QUEUE {action} TO {item} ({len(self.queue)})'
        self.log.append(log_entry)

    def print_log(self):
        for log_entry in self.log:
            print(log_entry)