import json
from bson import ObjectId

def handle_args(args):
    user = args.get('user')
    if user:
        user = str(args.get('user'))
    return user

def read_config():
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data["MONGODB_URL"]

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)