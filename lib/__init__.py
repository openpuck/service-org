# shared logic goes here
import json
import decimal
import validation
import database
import exceptions


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






