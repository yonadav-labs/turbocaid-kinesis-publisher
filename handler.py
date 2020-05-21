def get_modified_attrs(entity, is_insert=False):
    result = []

    for attr, val in entity['NewImage'].items():
        if 'M' in val:
            if 'value' not in val['M']:
                continue
            value = val['M']['value']['S']
            if is_insert or value != entity['OldImage'][attr]['M']['value']['S']:
                item = {
                    'uuid': val['M']['uuid']['S'],
                    'attribute_name': attr,
                    'attribute_value': value,
                    'created_at': val['M']['created_date']['S'],
                    'updated_at': val['M']['updated_date']['S']
                }
                
                result.append(item)

    return result


def handler(event, context):
    # print(event)
    for record in event['Records']:
        if record['eventName'] == 'INSERT':
            items = get_modified_attrs(record['dynamodb'], True)
            # put TurbocaidApplication to Kinesis
        elif record['eventName'] == 'MODIFY':
            # put MedicaidDetail to Kinesis
            items = get_modified_attrs(record['dynamodb'])

    print (items)
    return items
