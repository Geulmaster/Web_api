import json

def handle_args(args):
    user = args.get('user')
    if user:
        user = str(args.get('user'))
    return user

def read_config():
    with open('config.json') as config_file:
        data = json.load(config_file)
    return data["MONGODB_URL"]