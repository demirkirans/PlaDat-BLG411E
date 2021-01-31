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

    #get company id
    
    Company_ID = int(queryStringParameters['id'])
    
    ###      GET  CONTACT     ###
    
    table = dynamodb.Table('Jobs')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Company_ID').eq(Company_ID))
    responseBody = { }
    placements   = []
    
    if response['Count'] == 0:
        #no matching item
        print("No item was found :/")
        
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error- No item found in contact_student table *-*')
        }
    else:
        #extract id 
        
        for item in response['Items']:
            
            Placement_ID = item['ID']
            #we got placement id
            
            placement = {}
            
            ##################### Add attributes from Jobs TAble ##########################
            
            placement['Company_ID']         = int(item['Company_ID'])
            placement['Placement_ID']       = int(item['ID'])
            placement['Company_name']       = item['Company_name']
            placement['title']              = item['title']
            placement['description']        = item['description']
            placement['category']           = item['category']
            placement['contact_info']       = item['contact_info']
            placement['department_name']    = item['department_name']
            placement['degree']             = item['degree']
            placement['location']           = item['location']
            placement['salaries']           = int(item['salaries'])
            
            
            ################3 Add attributes from Skills_jobs table  #########################
            
            table = dynamodb.Table('Skills_jobs')
            skills = []
            
            db_response = table.scan(FilterExpression=Attr('Jobs_Company_ID').eq(Company_ID)&Attr('Jobs_ID').eq(Placement_ID))
            
            if db_response['Count'] == 0:
                return {
                    "statusCode": 500,
                    "body": json.dumps('Internal Server Error - No matching skills for placement')
                }
                
            else:
                for attribute in db_response['Items']:
                    skills.append(attribute['name'])
                
            #add skills to placement 
            placement['skills'] = skills
            
            
            
            #################### Add attributes from Benefits table  #################
            
            table = dynamodb.Table('Benefits')
            benefits = []
            
            db_response = table.scan(FilterExpression=Attr('Jobs_Company_ID').eq(Company_ID)&Attr('Jobs_ID').eq(Placement_ID))
            
            if db_response['Count'] == 0:
                return {
                    "statusCode": 500,
                    "body": json.dumps('Internal Server Error - No matching benefits for placement')
                }
                
            else:
                for attribute in db_response['Items']:
                    benefits.append(attribute['name'])
                
            #add skills to placement 
            placement['benefits'] = benefits
            
            
            #################### Add attributes from Certificates_job table  #################
            
            table = dynamodb.Table('Certificates_job')
            certificates = []
            
            db_response = table.scan(FilterExpression=Attr('Jobs_Company_ID').eq(Company_ID)&Attr('Jobs_ID').eq(Placement_ID))
            
            if db_response['Count'] == 0:
                print("No matching certificates for placement")
                

            else:
                for attribute in db_response['Items']:
                    certificates.append(attribute['name'])
                
            #add skills to placement 
            placement['certificates']  = certificates
        
        
            ############  WE GOT ALL ATTRIBUTES FOR A SINGLE PLACEMENT  #################
            
            placements.append(placement)
        
        
     
    responseBody['placements'] = placements
    
    return {
        "statusCode": 200,
        "body": json.dumps(responseBody)
    }
     
    