# shared logic goes here
import boto3
import json
import decimal
import validation
# import exceptions

# LocationsTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('locations')
# LocationsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('locations')
# LocationAltnamesTable = boto3.resource('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1').Table('location_altnames')
# LocationAltnamesTable = boto3.resource('dynamodb', region_name='us-east-1').Table('location_altnames')
TeamsTable = boto3.resource('dynamodb', region_name='us-east-1').Table('teams')


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