# shared logic goes here
import boto3
import json
import decimal
import validation
import exceptions

TeamsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('teams')
LeaguesTable = boto3.resource('dynamodb', region_name='us-east-1').Table('leagues')
ConferencesTable = boto3.resource('dynamodb', region_name='us-east-1').Table('conferences')
SeasonsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('seasons')
InstitutionsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('institutions')


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_json(response):
    """
    Return a JSON object with actual number types.
    """
    return json.loads(json.dumps(response, cls=DecimalEncoder))


def create_update_expression(keys):
    """
    Generates an UpdateExpression string from a list of keys.
    :param keys: A list of keys.
    :return: An UpdateExpression string for Table.update_item()
    """
    # Expressions need to start with set
    expression = "set "

    # Build the expression from the keys
    for key in keys:
        expression += "%s = :%s, " % (key, key)

    # Strip off the last set of whitespace
    if expression.endswith(", "):
        expression = expression[:-2]

    # Return
    return expression


def create_expression_attribute_values(keys, event, body=True):
    """
    Build a dictionary for an ExpressionAttributeValues directive.
    :param keys: A list of keys.
    :param event: The event object containing their values.
    :return: A dictionary for Table.update_item()
    """
    # Sometimes we might not want to use the event body for our key values.
    event_key_source = event['body']
    if body is False:
        event_key_source = event

    # The Dictionary
    values = {}

    for key in keys:
        # This will throw a KeyError if for some reason the value was
        # not specified in the event.
        values[":%s" % key] = event_key_source[key]

    return values


def perform_update(table, event, keys, drop_id=True):
    # Remove the ID key since we don't let users change that.
    if drop_id is True:
        keys.remove('id')

    try:
        response = table.update_item(
            Key={
                'id': event['pathId']
            },
            UpdateExpression=create_update_expression(keys),
            ExpressionAttributeValues=create_expression_attribute_values(keys, event),
            ReturnValues="ALL_NEW"
        )

        return response['Attributes']
    except exceptions.ClientError as ce:
        raise exceptions.InternalServerException(ce.message)
