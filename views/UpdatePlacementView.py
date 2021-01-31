from flask.views import View
from flask import render_template, request, redirect, url_for,abort,flash, session
from services.data.Benefits import Benefits
from services.data.Certificate_Placement import Certificate_Placement
from services.data.Placement import Placement
from services.data.Skills_Placement import Skills_Placement
from services.data.Student_Specifications import StudentSpecifications
from services.API.api import sendPlacement, getSinglePlacement, updatePlacement

class UpdatePlacementView(View):

    def get_template_name(self,values):
        return render_template("./companyUpdatePlacement.html",values=values)
    
    def dispatch_request(self):
        skills = []
        certificate = []
        benefits = []
        c_ID = session["companyId"]
        p_ID = request.args.get('p_id')  

        if request.method == 'GET':
            response = getSinglePlacement(c_ID, p_ID)
            if response == "500":
                   abort(500)
            else:       
                values = response
                return self.get_template_name(values)

        if request.method == 'POST' and 'go-companyhomepage' in request.form:
            if request.form['go-companyhomepage'] == "companyhomepage":
                return redirect(url_for("companyhomepage"))

        if request.method == 'POST' and 'update_placement' in request.form:
            if request.form['update_placement'] == "save":
                title = request.form.get("title")
                category = request.form.get("category")
                email = request.form.get("email")
                location = request.form.get("location")
                salary = request.form.get("salary")
                description = request.form.get("description")
                placement = Placement(title, category, email, location, salary, description)

                benefit1 = request.form.get("benefits1")
                if(benefit1 is not None and (benefit1 != "")):
                    benefits.append(benefit1)
                benefit2 = request.form.get("benefits2")
                if(benefit2 is not None and (benefit2 != "")):
                    benefits.append(benefit2)
                benefit3 = request.form.get("benefits3")
                if(benefit3 is not None and (benefit3 != "")):
                    benefits.append(benefit3)
                benefit4 = request.form.get("benefits4")
                if(benefit4 is not None and (benefit4 != "")):
                    benefits.append(benefit4)
                benefit5 = request.form.get("benefits5")
                if(benefit5 is not None and (benefit5 != "")):
                    benefits.append(benefit5)
                benefit6 = request.form.get("benefits6")
                if(benefit6 is not None and (benefit6 != "")):
                    benefits.append(benefit6)                    
                benefits_list = Benefits(benefits)

                department_name = request.form.get("department_name")
                degree = request.form.get("degree")
                studentspecifications = StudentSpecifications(department_name, degree)


                Cpp = request.form.get("Cpp")
                if(Cpp is not None):
                    skills.append(Cpp)
                
                Python = request.form.get("Python")
                if(Python is not None):
                    skills.append(Python)
                
                Java = request.form.get("Java")
                if(Java is not None):
                    skills.append(Java)
                
                c_prog = request.form.get("C (Programming Language)")
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

                Machine_Learning = request.form.get("Machine Learning")
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

                skills_list = Skills_Placement(skills)
                
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
                certificate_list = Certificate_Placement(certificate)
                
                response = updatePlacement(placement, benefits_list, studentspecifications, skills_list, certificate_list, c_ID, p_ID)

                if response == "500":
                    abort(500)
                if response == "200":
                    message =  "Updating placement is succesful."   
                return redirect(url_for("companyhomepage"))        
        