import sys
import bcrypt
from pymongo import MongoClient

username, plain_pwd = sys.argv[1], sys.argv[2]
hashed_pwd = bcrypt.hashpw(plain_pwd.encode(), bcrypt.gensalt())
DB_CONNECTION = MongoClient("mongodb://localhost:27017")
COLLECTION = DB_CONNECTION.users["users"]
COLLECTION.insert_one({"name": username, "password": hashed_pwd, "has_key": ""})
