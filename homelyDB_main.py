import pymongo
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

homeleyDB = myclient['homely']
user_cl = homeleyDB['users']
tool_cl = homeleyDB['tools']