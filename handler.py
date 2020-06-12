import json
import datetime

import boto3

from stream import TurbocaidApplication, MedicaidDetail


def get_stream_records(entity):
    """
    generate stream records for kinesis
    :param entity: dict
    :return: dict
    """
    records = []
    details = []

    is_insert = entity['eventName'] == 'INSERT'
    app_id = entity['dynamodb']['Keys']['application_uuid']['S']

    for attr, val in entity['dynamodb']['NewImage'].items():
        if 'M' in val:
            if 'value' not in val['M'] or 'type' not in val['M'] or val['M']['type']['S'] != 'medicaid_detail':
                continue

            value = val['M']['value']['S']
            if is_insert or value != entity['dynamodb']['OldImage'][attr]['M']['value']['S']:
                detail = {
                    'event_id': entity['eventID'],
                    'uuid': val['M']['uuid']['S'],
                    'attribute_name': attr,
                    'attribute_value': value,
                    'created_at': val['M']['created_date']['S'],
                    'updated_at': val['M']['updated_date']['S']
                }
                
                details.append(detail)

    if is_insert:
        # TODO: take care of country, state, status
        turbo_app = TurbocaidApplication(
            event_id=entity['eventID'],
            uuid=app_id,
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat()
        )
        turbo_app.medicaid_details = [json.dumps(ii) for ii in details]
        details = [turbo_app]
    else:
        details = [MedicaidDetail(**detail) for detail in details]

    for detail in details:
        records.append({
            'Data': json.dumps(detail.__dict__),
            'PartitionKey': app_id
        })

    return records


def handler(event, context):
    print(event)
    records = []
    for record in event['Records']:
        records += get_stream_records(record)

    print (json.dumps(records))
    if records:
        kinesis = boto3.client('kinesis', region_name='us-east-1')
        res = kinesis.put_records(Records=records, StreamName='sps_data')
        print (res, 'kinesis')
    return records
