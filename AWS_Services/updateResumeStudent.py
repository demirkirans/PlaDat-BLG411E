import json
import boto3
import time
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    #parse body of request body
    #requestBody            = json.loads(event['body'])
    #queryStringParameters  = json.loads(event['queryStringParameters'])
    requestBody           = event['body']
    #queryStringParameters = event['queryStringParameters']
    requestBody = json.loads(requestBody)

    #add informations on -Personal and Contact Info- tab
    #if queryStringParameters['key'] == 'contact':
    
    ###  GET CONTACT INFORMATION  ###
    Student_ID     = requestBody['Student_ID']
    Student_ID     = int(Student_ID)
    first_name     = requestBody['first_name']
    last_name      = requestBody['last_name']
    mobile_number  = requestBody['mobile_number']
    email          = requestBody['email']
    location       = requestBody['location']
    ###   GET EDUCATION INFORMATION  ###
    university_name           = requestBody['university_name']
    department_name           = requestBody['department_name']
    university_start_year     = requestBody['university_start_year']
    university_graduate_year  = requestBody['university_graduate_year']
    GPA                       = str(requestBody['GPA'])
    ###        WORK  EXPERIENCE  ###
    company_name     = requestBody['company_name']
    title            = requestBody['title']
    start_date       = requestBody['start_date']
    finish_date      = requestBody['finish_date']
    description      = requestBody['description']
    ###         SKILLS            ###
    skills           = requestBody['skills']
    ###         CERTIFICATES      ###
    certificate_names     = requestBody['certificate_names']
        
        
    ########    PERSONAL INFO & CONTACT    ########################    
        
    ###  PUT ITEM INTO DATABASE ###
    table = dynamodb.Table('contact_student')
    
    ### FIND ID  ###
    
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        
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
        
        ###  add the new item ###
            
        try:
            print("Adding new item")
            db_response = table.put_item(
                Item={
                    'ID'           : ID,
                    'Student_ID'   : Student_ID,
                    'first_name'   : first_name,
                    'last_name'    : last_name,
                    'mobile_number': mobile_number,
                    'email'        : email,
                    'location'     : location
                }
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
        
        
  
    else:
        #extract ID from item to be able to update item
        ID = response['Items'][0]['ID']
        
        try:
            print('Updating item')
            db_response = table.update_item(
                Key={
                    'ID': ID
                },
                UpdateExpression="set email=:e, first_name=:fn, last_name=:ln, #lct=:l, mobile_number=:m",
                ExpressionAttributeValues={
                    ':e' : email,
                    ':fn': first_name,
                    ':ln': last_name,
                    ':l' : location,
                    ':m' : mobile_number
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
                'body': json.dumps("Internal Server Error *-*")
            }
        
        
     
        
    #add information on -Educational Info- tab
    #elif queryStringParameters['key'] == 'education':
        
        
    ##################      EDUCATION     ################################
    
    ###  PUT ITEM INTO DATABASE ###
    table = dynamodb.Table('Education')
    
    ### FIND ID  ###
    
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        
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
                    'ID'                      : ID,
                    'Student_ID'              : Student_ID,
                    'university_name'         : university_name,
                    'department_name'         : department_name,
                    'university_start_year'  : university_start_year,
                    'university_graduate_year': university_graduate_year,
                    'GPA'                     : GPA
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
        
    else:
        #extract ID from item to be able to update item
        ID = response['Items'][0]['ID']
        
        try:
            print('Updating item')
            db_response = table.update_item(
                Key={
                    'ID': ID
                },
                UpdateExpression="set GPA=:g, university_graduate_year=:ugy, university_name=:un, university_start_year=:usy, department_name=:dn",
                ExpressionAttributeValues={
                    ':g'  : GPA,
                    ':usy': university_start_year,
                    ':ugy': university_graduate_year,
                    ':un' : university_name,
                    ':dn' : department_name
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
        
    #elif queryStringParameters['key'] == 'experience':
    
    #################    WORK EXPERIENCE   #############################
    
    table = dynamodb.Table('Work_experience')
    
    ### FIND ID  ###
    
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:

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
                    'ID'            : ID,
                    'Student_ID'    : Student_ID,
                    'company_name'  : company_name,
                    'title'         : title,
                    'start_date'    : start_date,
                    'finish_date'   : finish_date,
                    'description'   : description
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

    else:
        #extract ID from item to be able to update item
        ID = response['Items'][0]['ID']
        
        try:
            print('Updating item')
            db_response = table.update_item(
                Key={
                    'ID': ID
                },
                UpdateExpression="set company_name=:cn, title=:t, start_date=:sd, finish_date=:fd, description=:d",
                ExpressionAttributeValues={
                    ':cn' : company_name,
                    ':t'  : title,
                    ':sd' : start_date,
                    ':fd' : finish_date,
                    ':d'  : description
                },
                ReturnValues="UPDATED_NEW"
            )
            # TODO: write code...
        except ClientError as e:
            print(e.response['Error']['Message'])
            #couldnt update
            return {
                'statusCode': 500,
                'body': json.dumps("Internal Server Error *-*")
            }
        
    #elif queryStringParameters['key'] == 'skills':
    
    ############################    SKILLS  ################################
    
    table = dynamodb.Table('Skills')
    
    ### FIND ID THAT MATCHES WITH STUDENT ID AND SKILL ###
    
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))

    if response['Count'] == 0:
        #no matching item
        
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
                        'ID'            : ID,
                        'Student_ID'    : Student_ID,
                        'skills'        : skill
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
    
    else:
        #extract ID from item to be able to update item
        for item in response['Items']:
            ID = item['ID']
            
            try:
                print("Deleting items...")
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
                        'ID'            : ID,
                        'Student_ID'    : Student_ID,
                        'skills'        : skill
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
                
    #elif queryStringParameters['key'] == 'certificate':
        
 
    ##################    CERTIFICATES   #############################
    
    if not certificate_names:
        return {
            "statusCode": 200,
            "body": json.dumps("Items updated *-*")
        }
    else:
        
        table = dynamodb.Table('Certificates')
        
        ### FIND ID  ###
        
        response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
        
        if response['Count'] == 0:
            #no matching item
            
            for certificate in certificate_names:
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
                            'ID'                : ID,
                            'Student_ID'        : Student_ID,
                            'certificate_name'  : certificate
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
    
        else:
            #extract ID from item to be able to update item
            for item in response['Items']:
                ID = item['ID']
                
                try:
                    print("Deleting items...")
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
                    
            for certificate in certificate_names:
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
                            'ID'                : ID,
                            'Student_ID'        : Student_ID,
                            'certificate_name'  : certificate
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
                    
    #############   EVERYTHING IS OK  ###############
            
    return {
        'statusCode': 200,
        'body': json.dumps("Items added *-*")
    }    
    
    
