#!/usr/bin/env python
from lib.exceptions import *
from boto3.dynamodb.conditions import Key, Attr
from boto3 import resource


# Boto Constants
RESOURCE = "dynamodb"
REGION = "us-east-1"

# Table Names
TEAMS_TABLE = "teams"
LEAGUES_TABLE = "leagues"
CONFERENCES_TABLE = "conferences"
SEASONS_TABLE = "seasons"
INSTITUTIONS_TABLE = "institutions"


def _create_expression_attribute_values(keys, event, body=True):
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


def _create_key_condition_expression(key_dict):
    """
    Create a DynamoDB KeyConditionExpression object from a dictionary.
    :param key_dict: The key dictionary to build into a query.
    :return: A boto3.dynamodb.conditions.And or boto3.dynamodb.conditions.Equals
    """
    cond_obj = None
    for key in key_dict.keys():
        if cond_obj is None:
            # This is the first key
            cond_obj = Key(key).eq(key_dict[key])
            continue
        # Combine the objects together
        cond_obj = cond_obj & Key(key).eq(key_dict[key])

    # @TODO: This should probably spit out an exception.
    return cond_obj


def _create_update_expression(keys):
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


def get_table(name):
    """
    Return a Table object for a given name.
    :param name: The table name.
    :return: A Boto3 Table object.
    """
    return resource(RESOURCE, region_name=REGION).Table(name)


def create_element(table, event):
    """
    Create a new object in a table.
    :param table: The Table object to operate on.
    :param event: The event containing the object we want to insert.
    :return: The event body if success, Exception if failed.
    """
    try:
        table.put_item(Item=event['body'])
    except ClientError as ce:
        raise InternalServerException(ce.message)

    return event['body']


def read_element(table, event):
    """
    Read an object from a table.
    :param table: The Table object to operate on.
    :param event: The event containing the object we want to read.
    :return: The event body if success, Exception if failed.
    """
    try:
        response = table.get_item(Key={'id': event['pathId']})
    except ClientError as ce:
        raise InternalServerException(ce.message)

    if 'Item' not in response:
        raise NotFoundException("Object '%s' not found in table '%s'." % (event['pathId'], table.table_name))

    return response['Item']


def update_element(table, event, keys, drop_id=True):
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
            UpdateExpression=_create_update_expression(keys),
            ExpressionAttributeValues=_create_expression_attribute_values(keys, event),
            ReturnValues="ALL_NEW"
        )

        return response['Attributes']
    except ClientError as ce:
        raise InternalServerException(ce.message)


def delete_element(table, event):
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
    except ClientError as ce:
        if "ConditionalCheckFailedException" in ce.message:
            raise NotFoundException(
                "Object '%s' not found." % event['pathId'])

        raise InternalServerException(ce.message)


def scan_table(table):
    """
    Scan a table. Note - this is an expensive operation so don't do it
    too much.
    :param table:
    :return:
    """
    return table.scan()['Items']


def query_table(table, index, expression_dict):
    """
    Perform a query against a table.
    :param table: Table object.
    :param index: Name of the index to query.
    :param expression_dict: Dictionary of attributes needed to perform query.
    :return:
    """
    # We must turn the dict into a KeyConditionalExpression
    expression = _create_key_condition_expression(expression_dict)

    # Then perform the query
    results = table.query(
        IndexName=index,
        KeyConditionExpression=expression
    )
    if len(results['Items']) < 1:
        raise NotFoundException(
            "No objects found in '%s' query on table '%s'." % (table.table_name, index))

    return results['Items']