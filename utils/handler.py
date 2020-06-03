def handle_args(args):
    user = args.get('user')
    if user:
        user = str(args.get('user'))

    return user