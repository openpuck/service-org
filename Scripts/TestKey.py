#!/usr/bin/env python

from boto3.dynamodb.conditions import Key

data = {
    'foo': 'ASD',
    'bar': 'QWE',
    'baz': 'LOLZ'
}

object = None
for key in data.keys():
    if object is None:
        object = Key(key).eq(data[key])
        print object.get_expression().values()
    else:
        object = object & Key(key).eq(data[key])

# print object.get_expression().values()[1][0].expression_format