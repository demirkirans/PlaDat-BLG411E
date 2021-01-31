import json
import boto3
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    # TODO implement

    queryStringParameters = event['queryStringParameters']

    #get student id
    
    Student_ID = int(queryStringParameters['id'])
    
    ###         DELETE CONTACT       ###
    
    table = dynamodb.Table('contact_student')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error *-*')
        }
    else:
        #extract id 
        ID = response['Items'][0]['ID']
        
        try:
            print("Deleting item...")
            response = table.delete_item(
                Key={
                    'ID': ID
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
    
    
    ###         DELETE EDUCATION     ###
    
    table = dynamodb.Table('Education')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error *-*')
        }
    else:
        #extract id 
        ID = response['Items'][0]['ID']
        
        try:
            print("Deleting item...")
            response = table.delete_item(
                Key={
                    'ID': ID
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
    
    
    ###        DELETE EXPERIENCE     ###
    
    table = dynamodb.Table('Work_experience')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error *-*')
        }
    else:
        #extract id 
        ID = response['Items'][0]['ID']
        
        try:
            print("Deleting item...")
            response = table.delete_item(
                Key={
                    'ID': ID
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
    
    
    ###        DELETE  SKILLS        ###
    
    table = dynamodb.Table('Skills')
    
    #find matching item
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    #delete skills one by one
    for item in response['Items']:
        ID = item['ID']
        
        try:
            print("Deleting item...")
            response = table.delete_item(
                Key={
                    'ID': ID
                }
            )
        # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }

    
    ###        DELETE  CERTIFICATES  ###
    
    table = dynamodb.Table('Certificates')
    
    #find matching item
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no certificates
        print("No matching item for certificates")
    
    else:
        #delete skills one by one
        for item in response['Items']:
            ID = item['ID']
            
            try:
                print("Deleting item...")
                response = table.delete_item(
                    Key={
                        'ID': ID
                    }
                )
            # TODO: write code...
            except ClientError as e:
                print(e.response['Error']['Message'])
                #couldnt update
                return {
                    'statusCode': 500,
                    'body': json.dumps("Internal Server Error *-*")
                }


    ###     PROGRAM GETS HERE   IF EVERYTHING IS OK   ####
    
    return {
        'statusCode': 200,
        'body': json.dumps('Items deleted *-*')
    }
