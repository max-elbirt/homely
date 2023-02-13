class BOTUser:
    def __init__(self, user_id, user_name: str, last_added = None):
        self.user_id = user_id
        self.user_name = user_name
        self.last_added = last_added