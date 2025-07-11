import datetime

def lambdahandler(event, context):
    new_utc = datetime.datetime.utcnow().isoformat() + 'Z'
    return {
        'statusCode': 200,
        'body': {'timestamp_utc': new_utc}
    }