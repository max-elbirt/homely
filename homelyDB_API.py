import pymongo
from classes import User, Tool

my_client = pymongo.MongoClient("mongodb://localhost:27017/")

homely_DB = my_client['homely']
user_cl = homely_DB['users']
tool_cl = homely_DB['tools']

def add_tool(tool: Tool, user: User):
    tool_cl.insert_one(tool)
    if user_cl.find(tool.user_id) == -1:
        user_cl.insert_one(user)

def remove_tool(tool: Tool):
    tool_cl.delete_one(tool)

def borrow_tool(tool: Tool):
    if tool_cl[tool].availability:
        tool_cl[tool].set_availability(False)
    pass

def return_tool(tool: Tool):
    tool_cl[tool].set_availability(True)