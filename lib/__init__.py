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
