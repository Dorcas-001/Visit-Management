import bcrypt

users = [
    {"username": "Dorcas", "password": "Dorcas@EC"},
    {"username": "Tshepo", "password": "Tshepo@EC"},
    {"username": "Innocent", "password": "Innocent@EC"},
    {"username": "Bruce", "password": "Bruce@EC"},
    {"username": "Penny", "password": "Penny@EC"},
    {"username": "Kevin R", "password": "KevinR@EC"},
    {"username": "Kevin K", "password": "KevinK@EC"},
    {"username": "Carmen", "password": "Carmen@EC"},
    {"username": "Frank", "password": "Frank@EC"},
    {"username": "Bishosi", "password": "Bishosi@EC"},
    {"username": "Michel", "password": "Michel@EC"},
    {"username": "Stella", "password": "Stella@EC"}
]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

hashed_users = [{"username": user["username"], "password": hash_password(user["password"])} for user in users]

import json
with open('users.json', 'w') as file:
    json.dump({"users": hashed_users}, file, indent=4)

print("Users with hashed passwords saved to users.json")
