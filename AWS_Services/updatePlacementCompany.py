import json
import boto3
import time
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    #parse body of request body
    requestBody           = event['body']
    #requestBody = json.loads(requestBody)
    requestBody = json.loads(requestBody)

    ###          FOR JOB TABLE             ###
    Company_ID       = requestBody['Company_ID']
    #Company_name     = requestBody['Company_name']
    Placement_ID     = requestBody['Placement_ID']
    title            = requestBody['title']
    description      = requestBody['description']
    category         = requestBody['category']
    contact_info     = requestBody['contact_info']
    department_name  = requestBody['department_name']
    degree           = requestBody['degree']
    #experience       = requestBody['experience']
    location         = requestBody['location']
    salaries         = requestBody['salaries']
    
    ###   FOR SKILLS  TABLE  ###
    skills           = requestBody['skills']
    ###  FOR BENEFITS TABLE  ###
    benefits         = requestBody['benefits']
    ###  FOR  CERTIFICATES TABLE  ###
    certificates     = requestBody['certificates']
    
    ###################   GET COMPANY NAME    ##########################
    
    table = dynamodb.Table('Company')
    
    response = table.scan(FilterExpression=Attr('ID').eq(Company_ID))
    
    if response['Count'] == 0:
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error - No matching company name for given company id *-*")
        }
    else:
        Company_name = response['Items'][0]['name']
        
    ####################    UPDATE  JOBS TABLE    ##########################    
        
    table = dynamodb.Table('Jobs')
    
    response = table.scan(FilterExpression=Attr('ID').eq(Placement_ID)&Attr('Company_ID').eq(Company_ID))
    
    if response['Count'] == 0:
        #no matching placement in database 
        
        return {
            "statusCode": 500,
            "body": json.dumps("Internal Server Error - no matching item for Jobs Table *-*")
        }
    else:
        #we have item
        
        #extract ID from item to be able to update item
        #ID = response['Items'][0]['ID']
        
        try:
            print('Updating item')
            db_response = table.update_item(
                Key={
                    'ID': Placement_ID
                },
                UpdateExpression="set title=:t, description=:d, Company_name=:cn, category=:c, contact_info=:ci, department_name=:dn, degree=:dg, #lct=:l, salaries=:s, job_creation_timestamp=:jct",
                ExpressionAttributeValues={
                    ':cn' : Company_name,
                    ':t'  : title,
                    ':d'  : description,
                    ':c'  : category,
                    ':ci' : contact_info,
                    ':dn' : department_name,
                    ':dg' : degree,
                    ':l'  : location,
                    ':s'  : salaries,
                    ":jct": int(time.time())
                },
                ExpressionAttributeNames={
                    '#lct': 'location'
                },
                ReturnValues="UPDATED_NEW"
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error - Couldnt update item for job table *-*")
            }
            
    ###########        UPDATE  SKILLS   ##############        
    
    
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
        #UPDATE SKILLS#        
                
        for skill in skills:
            #for every skill to be added
            # check is there any item in table then add new item #
            responsee = table.scan()
            count = responsee['Count']
            
            if count == 0:
                #no item in database. Initialize id to 0
                ID = 0
            else:
                #there are items in table. Find max id and set new ID to max(id) + 1
                data=responsee['Items']
                x = []
                for item in data:
                    x.append(item['ID'])
                ID = max(x) + 1
            # ID assigned #
            
            try:
                print("Adding new item")
                db_response = table.put_item(
                    Item={
                        'ID'              : ID,
                        'Jobs_Company_ID' : Company_ID,
                        'Jobs_ID'         : Placement_ID,
                        'name'            : skill
                    }
                )
            # TODO: write code...
            except ClientError as e:
                print(e.response['Error']['Message'])
                #couldnt update
                return {
                    'statusCode': 500,
                    'body': json.dumps("Internal Server Error - Couldn't add item in skills table  *-*")
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
        #UPDATE BENEFITS#        
                
        for benefit in benefits:
            #for every skill to be added
            # check is there any item in table then add new item #
            responsee = table.scan()
            count = responsee['Count']
            
            if count == 0:
                #no item in database. Initialize id to 0
                ID = 0
            else:
                #there are items in table. Find max id and set new ID to max(id) + 1
                data=responsee['Items']
                x = []
                for item in data:
                    x.append(item['ID'])
                ID = max(x) + 1
            # ID assigned #
            
            try:
                print("Adding new item")
                db_response = table.put_item(
                    Item={
                        'ID'              : ID,
                        'Jobs_Company_ID' : Company_ID,
                        'Jobs_ID'         : Placement_ID,
                        'name'            : benefit
                    }
                )
            # TODO: write code...
            except ClientError as e:
                print(e.response['Error']['Message'])
                #couldnt update
                return {
                    'statusCode': 500,
                    'body': json.dumps("Internal Server Error -Couldn't update item in benefits  *-*")
                }
    
    
    ###############   UPDATE CERTIFICATES   ##########################
    
    if not certificates:
        return {
        "statusCode": 200,
        "body": json.dumps("Placement changed *-*")
    }
    else:
        
        table = dynamodb.Table('Certificates_job')
        
        response = table.scan(FilterExpression=Attr('Jobs_ID').eq(Placement_ID)&Attr('Jobs_Company_ID').eq(Company_ID))
        
        if response['Count'] == 0:
            #no matching for given placement and company id
            print("No matching item in certificate table *-*")
            
            for certificate in certificates:
                #for every skill to be added
                # check is there any item in table then add new item #
                responsee = table.scan()
                count = responsee['Count']
                
                if count == 0:
                    #no item in database. Initialize id to 0
                    ID = 0
                else:
                    #there are items in table. Find max id and set new ID to max(id) + 1
                    data=responsee['Items']
                    x = []
                    for item in data:
                        x.append(item['ID'])
                    ID = max(x) + 1
                # ID assigned #
                
                try:
                    print("Adding new item")
                    db_response = table.put_item(
                        Item={
                            'ID'              : ID,
                            'Jobs_Company_ID' : Company_ID,
                            'Jobs_ID'         : Placement_ID,
                            'name'            : certificate
                        }
                    )
                # TODO: write code...
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    #couldnt update
                    return {
                        'statusCode': 500,
                        'body': json.dumps("Internal Server Error - Couldn't update item in certificate table *-*")
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
                        'body': json.dumps("Internal Server Error- Couldn't delete item in certificate table *-*")
                    }
            #UPDATE BENEFITS#        
                    
            for certificate in certificates:
                #for every skill to be added
                # check is there any item in table then add new item #
                responsee = table.scan()
                count = responsee['Count']
                
                if count == 0:
                    #no item in database. Initialize id to 0
                    ID = 0
                else:
                    #there are items in table. Find max id and set new ID to max(id) + 1
                    data=responsee['Items']
                    x = []
                    for item in data:
                        x.append(item['ID'])
                    ID = max(x) + 1
                # ID assigned #
                
                try:
                    print("Adding new item")
                    db_response = table.put_item(
                        Item={
                            'ID'              : ID,
                            'Jobs_Company_ID' : Company_ID,
                            'Jobs_ID'         : Placement_ID,
                            'name'            : certificate
                        }
                    )
                # TODO: write code...
                except ClientError as e:
                    print(e.response['Error']['Message'])
                    #couldnt update
                    return {
                        'statusCode': 500,
                        'body': json.dumps("Internal Server Error - Couldn't update item in certificate table *-*")
                    }
        
    
    return {
        "statusCode": 200,
        "body": json.dumps("Placement changed *-*")
    }
        
    