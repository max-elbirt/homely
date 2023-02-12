class Tool:
    def __init__(self, user_id, name, type_of = None, category = None, availability = False):
        self.user_id = user_id
        self.name = name
        self.type = type
        self.category = category
        self.availability = availability

    def get_availability(self):
        return self.availability

    def set_availability(self, status):
        self.availability = status


