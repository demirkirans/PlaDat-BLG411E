import json
import urllib3
import boto3
import time
from boto3.dynamodb.conditions import Key,Attr
from botocore.exceptions import ClientError

def matching(student_skills, job_skills):
	counter = 0
	for s_skill in student_skills:
		for j_skill in job_skills:
			if s_skill in j_skill:
				counter += 1
	
	return (counter / len(job_skills)) * 100

dynamodb = boto3.resource('dynamodb', region_name = 'us-east-2')

def lambda_handler(event, context):
    # TODO implement
    
    queryStringParameters = event['queryStringParameters']

    #get company id
    
    Student_ID   = int(queryStringParameters['sid'])
    
    
    student_skills = []
    matched_placements = []
    
    ####### Gather student skills ######
    
    table = dynamodb.Table('Skills')
    
    #scan for given student id
    response = table.scan(FilterExpression=Attr('Student_ID').eq(Student_ID))
    
    if response['Count'] == 0:
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error- No item found in Skills table *-*')
        }
    else:
        for item in response['Items']:
            student_skills.append(item['skills'])
            
            
    ############Scan all jobs ################
    
    table = dynamodb.Table('Jobs')
    
    response = table.scan()
    
    if response['Count'] == 0:
        return {
            "statusCode": 500,
            'body': json.dumps('Internal server error- There is no placement to show *-*')
        }
    else:
        for item in response['Items']:
            Placement_ID = int(item['ID'])
            Company_ID   = int(item['Company_ID'])
            
            #######For every placement, collect their skills #######
            job_skills = []
            
            table = dynamodb.Table('Skills_jobs')
            
            db_response = table.scan(FilterExpression=Attr('Jobs_Company_ID').eq(Company_ID)&Attr('Jobs_ID').eq(Placement_ID))
            
            for attribute in db_response['Items']:
                job_skills.append(attribute['name'])
            
            #we got skills for that placement
            percentage_of_matching = matching(student_skills, job_skills)
            
            ##### if percentage is high ################
            if percentage_of_matching > 30:
                matched_placements.append((Company_ID, Placement_ID, percentage_of_matching))
            
    ###sort placements based on their matching rate
    
    matched_placements = sorted(matched_placements, key=lambda x: x[2], reverse=True)
    
    ##we got ids for matching placements 
    ##get all placements
    http = urllib3.PoolManager()
    placements = []
    
    for item in matched_placements:
        cid = item[0]
        pid = item[1]
        
        url = "https://hp8xm3yzr0.execute-api.us-east-2.amazonaws.com/prod/getsingleplacement?cid={}&pid={}".format(cid, pid)
        r = http.request('GET', url)
        
        data = r.data.decode('utf-8')
        data = json.loads(data)
        
        placements.append(data)
    
    responseBody = {}
    responseBody['placements'] = placements
    
    return {
        'statusCode': 200,
        'body': json.dumps(responseBody)
    }
