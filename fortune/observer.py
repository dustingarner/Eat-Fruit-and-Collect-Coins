class Observer:
    def __init__(self, action: callable):
        self.action = action

    def do_action(self, *args, **kwargs):
        self.action(*args, **kwargs)


class Subject:
    def __init__(self):
        self.observer_list = []
    
    def add_observer(self, observer):
        self.observer_list.append(observer)
    
    def remove_observer(self, observer):
        if not observer in self.observer_list:
            return
        self.observer_list.remove(observer)
    
    def notify(self, *args, **kwargs):
        for observer in self.observer_list:
            observer.do_action(*args, **kwargs)
