import json
import boto3
import time
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    #parse body of request body
    requestBody           = event['body']
    requestBody = json.loads(requestBody)

    ###          FOR JOB TABLE             ###
    Company_ID       = requestBody['Company_ID']
    #Company_name     = requestBody['Company_name']
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
        
    ####################    ADD  PLACEMENT    ##########################    
        
    table = dynamodb.Table('Jobs')
    
    response = table.scan()
    
    if response['Count'] == 0:
        #no item in Jobs table
        
        Jobs_ID = 0
    else:
        #there are items in table
        #find max id and increase by 1
 
        data=response['Items']
        x = []
        for item in data:
            x.append(item['ID'])
        Jobs_ID = max(x) + 1
        # ID assigned #
        
    ###  add the new item ###
        
    try:
        print("Adding new item")
        db_response = table.put_item(
            Item={
                'ID'                     : Jobs_ID,
                'Company_ID'             : Company_ID,
                'Company_name'           : Company_name,
                'description'            : description,
                'category'               : category,
                'contact_info'           : contact_info,
                'department_name'        : department_name,
                'degree'                 : degree,
                'location'               : location,
                'job_creation_timestamp' : int(time.time()),
                'salaries'               : salaries,
                'title'                  : title,
                'location'               : location
            }
        )
        # TODO: write code...
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps("Internal Server Error *-*")
        }
        
    
    #######################   ADD  SKILLS   ##################################
    
    table = dynamodb.Table('Skills_jobs')
    
    ### FIND ID  ###
    
    for skill in skills:
        
        
        response = table.scan()
        
        if response['Count'] == 0:
            #no item in Jobs table
            
            ID = 0
        else:
            #there are items in table
            #find max id and increase by 1
     
            data=response['Items']
            x = []
            for item in data:
                x.append(item['ID'])
            ID = max(x) + 1
            # ID assigned #
            
        ###  add the new item ###
            
        try:
            print("Adding new item")
            db_response = table.put_item(
                Item={
                    'ID'              : ID,
                    'Jobs_ID'         : Jobs_ID,
                    'Jobs_Company_ID' : Company_ID,
                    'name'            : skill
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }    
        
    
    ###############    ADD  BENEFITS     ####################################
    
    table = dynamodb.Table('Benefits')
    
    for benefit in benefits:
        
        
        response = table.scan()
        
        if response['Count'] == 0:
            #no item in Jobs table
            
            ID = 0
        else:
            #there are items in table
            #find max id and increase by 1
     
            data=response['Items']
            x = []
            for item in data:
                x.append(item['ID'])
            ID = max(x) + 1
            # ID assigned #
            
        ###  add the new item ###
            
        try:
            print("Adding new item")
            db_response = table.put_item(
                Item={
                    'ID'              : ID,
                    'Jobs_ID'         : Jobs_ID,
                    'Jobs_Company_ID' : Company_ID,
                    'name'            : benefit
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }    
        
    
    
    
    
    
    ################   ADD CERTIFICATES   ##################################
    
    if not certificates:
        return {
        "statusCode": 200,
        "body": json.dumps({
            "Placement_ID": int(Jobs_ID)
        })
    }
    else:
        
        table = dynamodb.Table('Certificates_job')
        
        for certificate in certificates:
            
            
            response = table.scan()
            
            if response['Count'] == 0:
                #no item in Jobs table
                
                ID = 0
            else:
                #there are items in table
                #find max id and increase by 1
         
                data=response['Items']
                x = []
                for item in data:
                    x.append(item['ID'])
                ID = max(x) + 1
                # ID assigned #
                
            ###  add the new item ###
                
            try:
                print("Adding new item")
                db_response = table.put_item(
                    Item={
                        'ID'              : ID,
                        'Jobs_ID'         : Jobs_ID,
                        'Jobs_Company_ID' : Company_ID,
                        'name'            : certificate
                    }
                )
                # TODO: write code...
            except ClientError as e:
                print(e.response['Error']['Message'])
                return {
                    'statusCode': 500,
                    'body': json.dumps("Internal Server Error *-*")
                }    
        
    ###   EVERYTHING IS OK ####
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "Placement_ID": int(Jobs_ID)
        })
    }
    
