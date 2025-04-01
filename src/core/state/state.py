class State:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        raise NotImplementedError("Subclasses should implement this method")

    def update(self):
        raise NotImplementedError("Subclasses should implement this method")

    def render(self):
        raise NotImplementedError("Subclasses should implement this method")
