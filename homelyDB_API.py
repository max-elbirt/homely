import pymongo
import gridfs
from classes import Tool
from classes import User
from telegram import Update
from telegram.ext import Updater

my_client = pymongo.MongoClient("mongodb://localhost:27017")

homely_DB = my_client['homely']
user_cl = homely_DB['users']
tool_cl = homely_DB['tools']
image_cl = homely_DB['images']

fs = gridfs.GridFS(homely_DB)

def store_image_to_user(update: Update, tool: Tool):
    image = update.message.photo[-1]
    image_data = image.get_file()

    image_ref = fs.put(image_data, filename=f'{tool.name}{tool.user_id}.jpg')

    tool_cl.update_one({"user_id": tool.user_id}, {"image_ref":image_ref})


def add_tool(tool: Tool, user: User):
    tool_cl.insert_one(tool.__dict__)
    print(user_cl.find({"user_id": user.user_id}), "ppppp1")
    if not user_cl.find_one({"user_id": user.user_id}):
        user_cl.insert_one(user.__dict__)

def remove_tool(tool: Tool):
    tool_cl.delete_one(tool.__dict__)

def borrow_tool(tool: Tool):
    if tool_cl[tool].availability:
        tool_cl[tool].set_availability(False)
    pass

def return_tool(tool: Tool):
    tool_cl[tool].set_availability(True)



