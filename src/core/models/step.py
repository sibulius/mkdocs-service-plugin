class Step:
    def __init__(self, data):

        self.title = data.get("title")
        self.description = data.get("description")
        self.channel = data.get("channel")
        