import json
import boto3
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    # TODO implement

    queryStringParameters = event['queryStringParameters']

    #get company and placement id 
    
    Company_ID   = int(queryStringParameters['Company_ID'])
    Placement_ID = int(queryStringParameters['Placement_ID'])

    ###         DELETE JOBS       ###
    
    table = dynamodb.Table('Jobs')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('ID').eq(Placement_ID)&Attr('Company_ID').eq(Company_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error - No item found in Jobs table *-*')
        }
    else:
        #extract id 

        try:
            print("Deleting item...")
            response = table.delete_item(
                Key={
                    'ID': Placement_ID
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error - Couldn't delete item in Jobs Table *-*")
            }
    
    
    
    ###        DELETE  SKILLS        ###
    
    table = dynamodb.Table('Skills_jobs')
    
    response = table.scan(FilterExpression=Attr('Jobs_ID').eq(Placement_ID)&Attr('Jobs_Company_ID').eq(Company_ID))
    
    if response['Count'] == 0:
        #no matching for given placement and company id
        
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error - No matching item in skills table  *-*")
        }
    else:
        #we have matching
        #delete skills
        
        for item in response['Items']:
            ID = item['ID']
            
            try:
                print("Deleting items...")
                delete_response = table.delete_item(
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
                    'body': json.dumps("Internal Server Error - Couldnt delete item in skills table *-*")
                }

    
    #############   UPDATE  BENEFITS    ######################
    
    table = dynamodb.Table('Benefits')
    
    response = table.scan(FilterExpression=Attr('Jobs_ID').eq(Placement_ID)&Attr('Jobs_Company_ID').eq(Company_ID))
    
    if response['Count'] == 0:
        #no matching for given placement and company id
        
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error - No matching item for Benefits table *-*")
        }
    else:
        #we have matching
        #delete skills
        
        for item in response['Items']:
            ID = item['ID']
            
            try:
                print("Deleting items...")
                delete_response = table.delete_item(
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
                    'body': json.dumps("Internal Server Error- Couldn't delete item in benefits table *-*")
                }
    
    ###        DELETE  CERTIFICATES  ###
    
    table = dynamodb.Table('Certificates_job')
    
    response = table.scan(FilterExpression=Attr('Jobs_ID').eq(Placement_ID)&Attr('Jobs_Company_ID').eq(Company_ID))
    
    if response['Count'] == 0:
        #no matching for given placement and company id
        print("No matching item for certificates")
        
    else:
        #we have matching
        #delete skills
        
        for item in response['Items']:
            ID = item['ID']
            
            try:
                print("Deleting items...")
                delete_response = table.delete_item(
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
                    'body': json.dumps("Internal Server Error- Couldn't delete item in certificate table *-*")
                }


    ###     PROGRAM GETS HERE   IF EVERYTHING IS OK   ####
    
    return {
        'statusCode': 200,
        'body': json.dumps('Items deleted *-*')
    }
