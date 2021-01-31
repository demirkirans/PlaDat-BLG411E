'''
@Author Alper Meriç
'''
from flask.views import View
from flask import render_template, request, redirect, url_for
from services.API.api import searchJobsByCategory, searchByLocation, searchByKeywords, sortBydate
import json
class HomepageView(View):
    def __init__(self):
        self.jobs = None


    def get_template_name(self):
        return render_template("./homepage.html")
    
    
    def dispatch_request(self,**kwargs):

        if request.method == "POST":
            search = request.form.get('search-button')
            response = searchByKeywords(search)
            self.jobs = response
        
        if request.method == "GET":
            response = sortBydate()
            self.jobs = response


        if kwargs:
            print(kwargs)
            if kwargs.get('category'):
                category = kwargs.get('category')
                self.jobs = searchJobsByCategory(category)
                print("catego",self.jobs)

            if kwargs.get('location'):
                location = kwargs.get('location')
                self.jobs = searchByLocation(location)
                print("location",self.jobs)

            if kwargs.get('key'):
                location = kwargs.get('key')
                self.jobs = searchByKeywords(location)
                print("key",self.jobs)


        print(self.jobs)
        return render_template("./homepage.html", context = self.jobs)       