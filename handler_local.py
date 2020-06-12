import json

from handler import get_stream_records

if __name__ == '__main__':
    with open('./events/modify-2.json') as f:
        event = json.load(f)

    records = []
    for record in event['Records']:
        records += get_stream_records(record)

    print (records)
