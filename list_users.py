import pymongo

# Connect to databse
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["users"]

# Get users collection
collection = db["users"]

# Find users with has_key=""
empty_has_key_users = list(collection.find({"has_key": ""}))

# Find users with has_key=1
has_key_1_users = list(collection.find({"has_key": 1}))

# Show results
print("Uzytkownicy z has_key=\"\":")
for user in empty_has_key_users:
    print(user['name'])

print("\nUzytkownicy z has_key=1:")
for user in has_key_1_users:
    print(user['name'])

# Close client
client.close()
