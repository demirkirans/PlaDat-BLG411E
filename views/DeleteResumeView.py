'''
@Author Alper Meriç
'''
from flask.views import View
from flask import render_template, request, redirect, url_for,flash,abort,session
from services.API.api import deleteResume

class DeleteResumeView(View):


    def get_template_name(self):
        return render_template("./studentDeleteResume.html")
    
    
    def dispatch_request(self):
        id=session["studentId"]
        if request.method == 'POST' and 'delete-resume' in request.form:
            print(request.form)
            if request.form['delete-resume'] == "delete":
                response=deleteResume(id)
                if response == "500":
                   abort(500)
                if response == "200":
                    message =  "Deleting Resume succesful."  
            if request.form['delete-resume'] == "no-delete":
                print("silmeden gitti")
            return redirect(url_for("homepage"))
        return self.get_template_name() 
