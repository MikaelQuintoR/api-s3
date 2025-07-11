import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = event.get('bucket_name')
    key = event.get('object_key')
    op = event.get('operation', 'download').lower()
    expires = event.get('expires_in', 3600)

    if not bucket or not key:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Falta bucket_name u object_key'})
        }

    if op not in ('upload', 'download'):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'operation debe ser upload o download'})
        }

    try:
        if op == 'upload':
            # Para subir, usamos put_object
            url = s3.generate_presigned_url(
                'put_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expires,
                HttpMethod='PUT'
            )
            method = 'PUT'
        else:
            # Para descargar
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket, 'Key': key},
                ExpiresIn=expires,
                HttpMethod='GET'
            )
            method = 'GET'

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'url': url,
            'method': method,
            'expires_in': expires
        })
    }
