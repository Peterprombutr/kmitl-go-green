
from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import time 

from GGK_Global_API_Keys import *

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource("dynamodb", region_name = REGION_NAME, endpoint_url = ENDPOINT_URL)
table = dynamodb.Table('waterpi_sensor_data')

def pullSpecificJSON(key = "sensor/data", timestamp = "1576748116833"):
    try:
        response = table.get_item(
            Key={
                'key': key,
                'timestamp': timestamp
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("**GetItem succeeded:")
        return(json.dumps(item, cls=DecimalEncoder))

def pullLatestJSON(key = "sensor/data"):
    try:
        response = table.query(
            KeyConditionExpression=Key('key').eq( key ),
            ExpressionAttributeNames={},
            ExpressionAttributeValues={},
            ScanIndexForward=False,
            Limit=1,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Items']
        return json.dumps(item, cls=DecimalEncoder)

def JSONstringToList(JList = pullLatestJSON() ):
    NewJList = ""
    lenJ = len(JList)
    for i in range(lenJ):
        NewJList = NewJList + JList[i]

    remove_list = [" ","{","}","[","]","\""]
    for _ in remove_list:
        NewJList = NewJList.replace(_,"")

    NewJList = NewJList.replace(",",":")
    NewJList = NewJList.split(":")
    print("**Get Latest Item")
    return NewJList # Return as List
