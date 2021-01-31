import requests
import settings
import json
from flask import session

def loginCompany(data):
    url = settings.baseUrl

    url = url + "loginCompany"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Email": data.email,
        "Password": data.password
    }
    
    try:
        r = requests.post(
            url,
            json=data,
            headers=headers
            )
        if r.text == 403:
            session.pop('studentId', None)
            session.pop('companyId', None)
        print(r.text)
        return r.text
    except:
        error = "Unknow Error"
        return error

def registerCompany(data):

    url = settings.baseUrl

    url = url + "registerCompany"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Email": data.email,
        "Password": data.password,
        "Name": data.userName
    }
    
    try:
        r = requests.post(
            url,
            json=data,
            headers=headers
            )
        return r.text
    except:
        error = "Unknow Error"
        return error

def loginStudent(data):
    url = settings.baseUrl

    url = url + "loginStudent"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Email": data.email,
        "Password": data.password,
    }
    print(session)
    try:
        r = requests.post(
            url,
            json=data,
            headers=headers
            )
        print(r.text)
        if r.text == 403:
            session.pop('studentId', None)
            session.pop('companyId', None)
        return r.text
    except:
        error = "Unknow Error"
        return error

def registerStudent(data):

    url = settings.baseUrl

    url = url + "registerStudent"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Email": data.email,
        "Password": data.password,
        "Username":"emre"
    }
    
    try:
        r = requests.post(
            url,
            json=data,
            headers=headers
            )
        print(r.text)
        return r.text
    except:
        error = "Unknow Error"
        return error


'''''''''''''''''
@Author Alper Meriç
'''''''''''''''''
def sendResume(data1,data2,data3,data4,data5,id):

    url = settings.baseUrl

    url = url + "addresumestudent"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Student_ID": id, ###parametre olarak gönderilecek sonra
        "first_name": data1.first_name,
        "last_name": data1.last_name,
        "mobile_number": data1.mobile,
        "email": data1.email,
        "location": data1.location,
        "university_name": data2.university_name,
        "department_name": data2.department_name,
        "university_start_year": data2.university_start_year,
        "university_graduate_year": data2.university_graduate_year,
        "GPA": data2.actual_gpa,
        "company_name": data3.company_name,  
        "title":  data3.title,
        "start_date":  data3.start_date,
        "finish_date": data3.finish_date,
        "description": data3.descriptions,
        "skills":data4.Skills,
        "certificate_names":data5.certificate
    }

    r = requests.post(
        url,
        json=data,
        headers=headers
        )
    print(r.text)
    return r.text

'''''''''''''''''
@Author Alper Meriç
'''''''''''''''''
def deleteResume(data):
    url = settings.baseUrl
    url = url + "deleteresumestudent?id="+str(data)
    r=requests.delete(url)
    print(r.text)
    return r.text

'''''''''''''''''
@Author Alper Meriç
'''''''''''''''''
def getResume(data):
    url = settings.baseUrl
    url = url + "showresumestudent?id="+str(data)
    r=requests.get(url)
    print("hata")
    print(r.json())
    return r.json()

def changePassword(passwordDto):
    print(session)
    id = passwordDto.id
    password = passwordDto.hashig()

    url = settings.baseUrl
    if 'studentId' in session:
        sessionId= session.pop('studentId', None)
        session['studentId'] = sessionId
        if str(id) == sessionId:
            print("student")
            url = url + "changePasswordStudent"
    if 'companyId' in session:
        sessionId = session.pop('companyId', None)
        session['companyId'] = sessionId
        if id == sessionId:
            url = url + "changePasswordCompany"
    
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    try:
        r = requests.post(
            url,
            json=password,
            headers=headers
            )
        return r.text
    except:
        return "Unknown Error. Try again"

def searchJobsByCategory(category):
    dic = {
        "category": category
    }
    url = settings.baseUrl + "searchJobsByCategory"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    try:
        r = requests.post(
            url,
            json=dic,
            headers=headers
            )
        return r.json()
        print("category",r.json)
    except:
        return "Unknown Error. Try again"

def searchByLocation(location):
    dic = {
        "location": location
    }
    url = settings.baseUrl + "searchByLocation"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    try:
        r = requests.post(
            url,
            json=dic,
            headers=headers
            )
        return r.json()
        print("location",r.json)
    except:
        return "Unknown Error. Try again"

def searchByKeywords(key):

    dic = {
        "keywords": key
    }
    url = settings.baseUrl + "searchByKeywords"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    try:
        r = requests.post(
            url,
            json=dic,
            headers=headers
            )
        return r.json()
        print("key", r.json())
    except:
        return "Unknown Error. Try again"

def sortBydate():

    url = settings.baseUrl + "sortByDate"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    
    try:
        r = requests.get(
            url,
            headers=headers
            )
        return r.json()
    except:
        return "Unknown Error. Try again"

def sendPlacement(data_p, data_b, data_ss ,data_s, data_c, c_ID):

    url = settings.baseUrl

    url = url + "addplacementcompany"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Company_ID": int(c_ID),
        "title": data_p.title,
        "description": data_p.description,
        "category": data_p.category,
        "contact_info": data_p.email,
        "department_name": data_ss.department,
        "degree": data_ss.degree,
        "location": data_p.location,
        "salaries": int(data_p.salary),
        "skills": data_s.skills_placement,
        "benefits": data_b.benefits,
        "certificates": data_c.certificate_placement
    }
    r = requests.post(
        url,
        json=data,
        headers=headers
        )
    print('add',r.text)
    return r.text

def deletePlacement(c_ID, p_ID):
    url = settings.baseUrl
    url = url + "deleteplacementcompany?Company_ID="+str(c_ID)+"&Placement_ID="+str(p_ID)
    r = requests.delete(url)
    print('delete',r.text)
    return r.text

def updatePlacement(data_p, data_b, data_ss ,data_s, data_c, c_ID, p_ID):

    url = settings.baseUrl

    url = url + "updateplacementcompany"
    headers={'Content-type':'application/json', 'Accept':'application/json'}
    data = {
        "Company_ID": int(c_ID),       
        "Placement_ID": int(p_ID), 
        "title": data_p.title,
        "description": data_p.description,
        "category": data_p.category,
        "contact_info": data_p.email,
        "department_name": data_ss.department,
        "degree": data_ss.degree,
        "location": data_p.location,
        "salaries": int(data_p.salary),
        "skills": data_s.skills_placement,
        "benefits": data_b.benefits,
        "certificates": data_c.certificate_placement
    }
    r = requests.post(
        url,
        json=data,
        headers=headers
        )
    print('update', r.text)
    return r.text

def getSinglePlacement(c_id, p_id):
    url = settings.baseUrl
    url = url + "getsingleplacement?cid="+str(c_id)+"&pid="+str(p_id)
    r = requests.get(url)
    return r.json()

def getPlacements(c_id):
    url = settings.baseUrl
    url = url + "showplacementcompany?id="+str(c_id)
    headers = headers={'Content-type':'application/json', 'Accept':'application/json'}
    r = requests.get(url,headers=headers)
    return r.json()