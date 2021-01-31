'''
@Author Alper Meriç
'''
from flask.views import View
from flask import render_template, request, redirect, url_for,abort,flash,session
from services.data.Certificate import Certificate
from services.data.EducationalInfo import EducationalInfo
from services.data.Experience import Experience
from services.data.PersonalContactInfo import PersonalContactInfo
from services.data.Skills import Skills
from services.API.api import sendResume

class AddResumeView(View):


    def get_template_name(self):
        return render_template("./studentAddResume.html")
    
    
    def dispatch_request(self): 
        skills=[]
        certificate=[]
        id=session["studentId"]
        if request.method == 'POST' and 'go-homepage' in request.form:
            
            if request.form['go-homepage'] == "homepage":
                return redirect(url_for("homepage"))

        if request.method == 'POST' and 'add-resume' in request.form:
           
            if request.form['add-resume'] == "save":
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                mobile = request.form.get("mobile")
                email = request.form.get("email")
                location = request.form.get("location")
                personalContactInfo=PersonalContactInfo(first_name,last_name,mobile,email,location)

                university_name = request.form.get("university_name")
                department_name = request.form.get("department_name")
                university_start_year = request.form.get("university_start_year")
                university_graduate_year = request.form.get("university_graduate_year")
                actual_gpa = request.form.get("actual_gpa")
                educationalInfo=EducationalInfo(university_name,department_name,university_start_year,university_graduate_year,actual_gpa)

                company_name = request.form.get("company_name")
                title = request.form.get("title")
                start_date = request.form.get("start_date")
                finish_date = request.form.get("finish_date")
                descriptions = request.form.get("descriptions")
                experience=Experience(company_name,title,start_date,finish_date,descriptions)
     

                Cpp = request.form.get("Cpp")
                if(Cpp is not None):
                    skills.append(Cpp)
                
                Python = request.form.get("Python")
                if(Python is not None):
                    skills.append(Python)
                
                Java = request.form.get("Java")
                if(Java is not None):
                    skills.append(Java)
                
                c_prog = request.form.get("c_prog")
                if(c_prog is not None):
                    skills.append(c_prog)
                
                Javascript = request.form.get("Javascript")
                if(Javascript is not None):
                    skills.append(Javascript)

                Matlab = request.form.get("Matlab")
                if(Matlab is not None):
                    skills.append(Matlab)

                Object_Oriented_Programming = request.form.get("Object Oriented Programming")
                if(Object_Oriented_Programming is not None):
                    skills.append(Object_Oriented_Programming)

                Android_Programming = request.form.get("Android Programming")
                if(Android_Programming is not None):
                    skills.append(Android_Programming)

                Web_Programming = request.form.get("Web Programming")
                if(Web_Programming is not None):
                    skills.append(Web_Programming)

                Database_Management = request.form.get("Database Management")
                if(Database_Management is not None):
                    skills.append(Database_Management)

                NodeJs = request.form.get("NodeJs")
                if(NodeJs is not None):
                    skills.append(NodeJs)

                Docker = request.form.get("Docker")
                if(Docker is not None):
                    skills.append(Docker)
                
                Kubernetes = request.form.get("Kubernetes")
                if(Kubernetes is not None):
                    skills.append(Kubernetes)
                
                Linux = request.form.get("Linux")
                if(Linux is not None):
                    skills.append(Linux)
                
                Go = request.form.get("Go")
                if(Go is not None):
                    skills.append(Go)
                
                Swift = request.form.get("Swift")
                if(Swift is not None):
                    skills.append(Swift)
                
                Data_Structures = request.form.get("Data Structures")
                if(Data_Structures is not None):
                    skills.append(Data_Structures)

                Artificial_Intelligence = request.form.get("Artificial Intelligence")
                if(Artificial_Intelligence is not None):
                    skills.append(Artificial_Intelligence)

                Machine_Learning = request.form.get("MachineLearning")
                if(Machine_Learning is not None):
                    skills.append(Machine_Learning)

                Deep_Learning = request.form.get("Deep Learning")
                if(Deep_Learning is not None):
                    skills.append(Deep_Learning)

                Computer_Vision = request.form.get("Computer Vision")
                if(Computer_Vision is not None):
                    skills.append(Computer_Vision)

                Robotic = request.form.get("Robotic")
                if(Robotic is not None):
                    skills.append(Robotic)

                skills_list=Skills(skills)
                
                certificate_name1 = request.form.get("certificate_name1")
                if(certificate_name1 is not None and (certificate_name1 != "")):
                    certificate.append(certificate_name1)
                certificate_name2 = request.form.get("certificate_name2")
                if(certificate_name2 is not None and (certificate_name2 != "")):
                    certificate.append(certificate_name2)
                certificate_name3 = request.form.get("certificate_name3")
                if(certificate_name3 is not None and (certificate_name3 != "")):
                    certificate.append(certificate_name3)
                certificate_name4 = request.form.get("certificate_name4")
                if(certificate_name4 is not None and (certificate_name4 != "")):
                    certificate.append(certificate_name4)
                certificate_name5 = request.form.get("certificate_name5")
                if(certificate_name5 is not None and (certificate_name5 != "")):
                    certificate.append(certificate_name5)
                certificate_name6 = request.form.get("certificate_name6")
                if(certificate_name6 is not None and (certificate_name6 != "")):
                    certificate.append(certificate_name6)                    
                certificate_list=Certificate(certificate)
                
                response=sendResume(personalContactInfo,educationalInfo,experience,skills_list,certificate_list,id)
                if response == "500":
                   abort(500)
                if response == "200":
                    message =  "Adding Resume succesful." 
                    flash(message)    
                return redirect(url_for("homepage")) 
        return self.get_template_name()    
