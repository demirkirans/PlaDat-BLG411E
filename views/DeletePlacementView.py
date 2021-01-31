from flask.views import View
from flask import render_template, request, redirect, url_for,flash,abort,session
from services.API.api import deletePlacement

class DeletePlacementView(View):
    def get_template_name(self):
        return render_template("./companyDeletePlacement.html")
    
    def dispatch_request(self):
        if request.method == 'POST' and 'go-companyhomepage' in request.form:   
            if request.form['go-companyhomepage'] == "companyhomepage":
                return redirect(url_for("companyhomepage"))
        
        if request.method == 'POST' and 'delete_placement' in request.form:
            if request.form['delete_placement'] == "delete":
                if request.args.get('p_id'):
                    c_ID = session["companyId"]
                    p_ID = request.args.get('p_id')
                    response = deletePlacement(c_ID, p_ID)
                    if response == "500":
                        abort(500)
                    if response == "200":
                        message =  "Deleting Placement succesful."  
                return redirect(url_for("companyhomepage"))
        return self.get_template_name() 