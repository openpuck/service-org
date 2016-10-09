# shared logic goes here
import boto3
import json
import decimal
import validation
import exceptions
from boto3.dynamodb.conditions import Attr

# TeamsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('teams')
# LeaguesTable = boto3.resource('dynamodb', region_name='us-east-1').Table('leagues')
# ConferencesTable = boto3.resource('dynamodb', region_name='us-east-1').Table('conferences')
# SeasonsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('seasons')
# InstitutionsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('institutions')

TEAMS_TABLE = "teams"
LEAGUES_TABLE = "leagues"
CONFERENCES_TABLE = "conferences"
SEASONS_TABLE = "seasons"
INSTITUTIONS_TABLE = "institutions"


def get_table(name):
    """
    Return a Table object for a given name.
    :param name: The table name.
    :return: A Boto3 Table object.
    """
    return boto3.resource('dynamodb', region_name='us-east-1').Table(name)


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


def update_database_element(table, event, keys, drop_id=True):
    """
    Perform an update to a table element.
    :param table: The Table to work on.
    :param event: The Event containing the new values.
    :param keys: List of keys to update.
    :param drop_id: Drop the ID field from keys
    :return: The attributes of the new object if success, Exception if not.
    """
    # Remove the ID key since we don't let users change that.
    if drop_id is True:
        try:
            keys.remove('id')
        except ValueError:
            pass

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


def create_database_element(table, event):
    """
    Create a new object in a table.
    :param table: The Table object to operate on.
    :param event: The event containing the object we want to insert.
    :return: The event body if success, Exception if failed.
    """
    try:
        table.put_item(Item=event['body'])
    except exceptions.ClientError as ce:
        raise exceptions.InternalServerException(ce.message)

    return event['body']


def read_database_element(table, event):
    """
    Read an object from a table.
    :param table: The Table object to operate on.
    :param event: The event containing the object we want to read.
    :return: The event body if success, Exception if failed.
    """
    try:
        response = table.get_item(Key={'id': event['pathId']})
    except exceptions.ClientError as ce:
        raise exceptions.InternalServerException(ce.message)

    if 'Item' not in response:
        raise exceptions.NotFoundException("Object '%s' not found in table '%s'." % (event['pathId'], table.table_name))

    return response['Item']


def delete_database_element(table, event):
    """
    Delete an object from a table.
    :param table: The Table object to operate on.
    :param event: The event containing the object we want to delete.
    :return: An empty JSON blob if True, Exception if failed.
    """
    try:
        table.delete_item(
            Key={'id': event['pathId']},
            ConditionExpression=Attr('id').eq(event['pathId'])
        )
        return {}
    except exceptions.ClientError as ce:
        if "ConditionalCheckFailedException" in ce.message:
            raise exceptions.NotFoundException(
                "Object '%s' not found." % event['pathId'])

        raise exceptions.InternalServerException(ce.message)
