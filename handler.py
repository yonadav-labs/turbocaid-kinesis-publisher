import json
import datetime

import boto3

from stream import TurbocaidApplication, MedicaidDetail


def parse_value(value_entity):
    """
    build a valid value from various format value data
    """
    value = None
    if 'S' in value_entity:
        value = value_entity['S']
    elif 'M' in value_entity:
        value = {key: parse_value(val) for key, val in value_entity['M'].items()}
    elif 'L' in value_entity:
        value = [parse_value(ii) for ii in value_entity['L']]

    return value


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

            value_entity = val['M']['value']
            if is_insert or attr not in entity['dynamodb']['OldImage'] or value_entity != entity['dynamodb']['OldImage'][attr]['M']['value']:
                value = parse_value(value_entity)
                if not value:
                    continue

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
        if record['eventName'] in ['INSERT', 'MODIFY']:
            records += get_stream_records(record)

    print (json.dumps(records))
    if records:
        kinesis = boto3.client('kinesis', region_name='us-east-1')
        email = event['Records'][0]['dynamodb']['Keys']['email']['S']
        stream_name = 'sps-data-integration-test' if 'test' in email else 'sps_data'
        res = kinesis.put_records(Records=records, StreamName=stream_name)
        print (res, 'kinesis')
    return records
