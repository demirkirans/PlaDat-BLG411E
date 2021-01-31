from flask.views import View
from flask import render_template, request, redirect, url_for,session
from services.data.AutEntity import AutEntity
from services.data.Password import Password
from services.API.api import loginCompany, registerCompany, registerStudent, loginStudent, changePassword
import hashlib
class Authorization(View):


    def get_template_name(self):
        return render_template("./login.html")
    
    
    
    def dispatch_request(self, **kwargs):

        

        message =""

        if request.method == 'POST' and 'cmp-btn' in request.form:
            print(request.form)
            if request.form['cmp-btn'] == "login":
                print("company login")
                email = request.form.get("email")
                psw = request.form.get("psw")

                login = AutEntity(email,psw)
                login.hashing()
                response = loginCompany(login)
                print(response)
                if response == "403":
                    message = "User does not exist."
                elif response == "Unknow Error":
                    message = response
                else:
                    session['companyId'] = response
                    print("companyid", response)

                return redirect(url_for("companyhomepage"))

        if request.method == 'POST' and 'cmp-btn' in request.form:

            if request.form['cmp-btn'] == "register":
                print("company register")
                email = request.form.get('email')
                psw = request.form.get('psw')
                print(email,psw)

                register = AutEntity(email,psw,'gamgam')
                register.hashing()
                response = registerCompany(register)
                
                if response == "403":
                    message = "Email invalid"
                elif response == "Unknow Error":
                    message = response
                else:
                    message = "success"

                return render_template("./login.html", message=message)

            
        if request.method == 'POST'and 'std_btn' in request.form:
            if request.form['std_btn'] == "login":
                email = request.form.get("email")
                psw = request.form.get("psw")
                userName = "emrekaydu"
                print(email,psw)


                login = AutEntity(email,psw,userName)
                login.hashing()
                response = loginStudent(login)
                
                if response == "403":
                    session.pop('studentId', None)
                    session.pop('companyId', None)
                    message = "User does not exist."
                elif response == "Unknow Error":
                    message = response
                else:
                    session['studentId'] = response

                return redirect(url_for("homepage"))

        if request.method == 'POST' and 'std_btn' in request.form:
            if request.form['std_btn'] == "register":
                email = request.form.get("email")
                psw = request.form.get("psw")
                print(email,psw)

                register = AutEntity(email,psw)
                register.hashing()
                response = registerStudent(register)
                
                if response == "403":
                    message = "User exist."
                elif response == "Unknow Error":
                    message = response
         
                return render_template("./login.html", message=message)

        user_id = kwargs.get('passwordChange')
        if user_id:
            if request.method == "POST" and 'change-btn' in request.form:
                oldPassword = request.form.get("old_psw")
                newPassword = request.form.get("new_psw")
                message = None
                passwordDto = Password(user_id, newPassword, oldPassword)
                response = changePassword(passwordDto)
                print(response)
                if response == str(403):
                    message = "Password wrong"
                elif response == "true":
                    print("home go")
                    return redirect(url_for("homepage"))
                elif response == "Unknown Error. Try again":
                    message = response
            return render_template("./changePassword.html",message = message)
        return self.get_template_name()

def logOut():
    session.pop('studentId', None)
    session.pop('companyId', None)
    return redirect(url_for('/'))