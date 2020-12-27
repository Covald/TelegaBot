class Message:
    def __init__(self, Type=None, Chat_id=None, date=None, text=None, username=None):
        self.username = username
        self.Type = Type
        self.Chat_id = Chat_id
        self.text = text
        self.date = date
