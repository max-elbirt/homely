class User:
    def __int__(self, user_id: int, user_name: str, last_added = None):
        self.chat_id = user_id
        self.user_name = user_name
        self.last_added = last_added