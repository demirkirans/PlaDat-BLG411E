from flask.views import View
from flask import render_template, request, redirect, url_for,session
from services.API.api import getPlacements, getSinglePlacement
import json

class CompanyHomepageView(View):
    def __init__(self):
        c_id = session['companyId']
        print(getPlacements(c_id))
        if type(getPlacements(c_id))== str :
            self.placements = " "
        else:
            self.placements = getPlacements(c_id).get('placements') # get context

    def get_template_name(self):
        return render_template("./companyhomepage.html", context=self.placements)
    
    def dispatch_request(self):
        return render_template("./companyhomepage.html", context=self.placements)
