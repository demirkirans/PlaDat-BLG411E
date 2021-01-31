import json
import boto3
import time
import decimal
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self).default(o)


dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    
    queryStringParameters = event['queryStringParameters']

    #get student id
    
    Student_ID = int(queryStringParameters['id'])
    
    ###      GET  CONTACT     ###
    
    table = dynamodb.Table('contact_student')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    responseBody = { }
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error- No item found in contact_student table *-*')
        }
    else:
        #extract id 
        data = response['Items'][0]
        
        responseBody['email']         = data['email']
        responseBody['first_name']    = data['first_name']
        responseBody['last_name']     = data['last_name']
        responseBody['location']      = data['location']
        responseBody['mobile_number'] = str(data['mobile_number'])
        
    
    ###      GET  EDUCATION   ###
    
    table = dynamodb.Table('Education')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error - No item found in Education table *-*')
        }
    else:
        #extract id 
        data = response['Items'][0]
        

        responseBody['university_name']            = data['university_name']
        responseBody['department_name']            = data['department_name']
        responseBody['university_start_year']      = data['university_start_year']
        responseBody['university_graduate_year']   = data['university_graduate_year']
        responseBody['GPA']                        = data['GPA'] 
   
    ###     GET EXPERIENCE    ###
    
    table = dynamodb.Table('Work_experience')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error - No item found in Work_experience table *-*')
        }
    else:
        #extract id 
        data = response['Items'][0]
        
        responseBody['company_name'] = data['company_name']
        responseBody['title']        = data['title']
        responseBody['start_date']   = data['start_date']
        responseBody['finish_date']  = data['finish_date']
        responseBody['description']  = data['description'] 
        
    
    ###     GET  SKILLS       ###
    
    table = dynamodb.Table('Skills')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error- No item found in skills table *-*')
        }
    else:
        #extract id 
        skills = []
        
        for item in response['Items']:
            skill = item['skills']
            skills.append(skill)
        
        responseBody['skills'] = skills
        

  
    ###     GET CERTIFICATES  ###
    
    table = dynamodb.Table('Certificates')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        
    else:
        #extract id 
        certificates = []
        
        for item in response['Items']:
            certificate = item['certificate_name']
            certificates.append(certificate)
        
        responseBody['certificate_names'] = certificates
        
    return {
        "statusCode": 200,
        "body": json.dumps(responseBody)
    }
        