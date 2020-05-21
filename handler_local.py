import json

from handler import handler

if __name__ == '__main__':
    with open('./events/insert.json') as f:
        event = json.load(f)

    items = handler(event=event, context={})
