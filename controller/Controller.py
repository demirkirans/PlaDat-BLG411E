from flask import Flask
from views.HomepageView import HomepageView
from views.AddResumeView import AddResumeView
from views.DeleteResumeView import DeleteResumeView
from views.UpdateResumeView import UpdateResumeView
from views.Authorization import Authorization,logOut
from views.DeletePlacementView import DeletePlacementView
from views.AddPlacementView import AddPlacementView
from views.UpdatePlacementView import UpdatePlacementView
from views.CompanyHomepageView import CompanyHomepageView
class Controller:

    def __init__(self, app):
        self.app = app
        self.authorization_view = Authorization.as_view('/')
        self.homepage_view = HomepageView.as_view('homepage')
        self.addresume_view = AddResumeView.as_view('addresume')
        self.deleteresume_view = DeleteResumeView.as_view('deleteresume')
        self.updateresume_view = UpdateResumeView.as_view('updateresume')

        self.deleteplacement_view = DeletePlacementView.as_view('deleteplacement')
        self.addplacement_view = AddPlacementView.as_view('addplacement')
        self.updateplacement_view = UpdatePlacementView.as_view('updateplacement')
        self.companyhomepage_view = CompanyHomepageView.as_view('companyhomepage')


    def initialRouter(self):
        self.app.add_url_rule('/', view_func=self.authorization_view, methods=["GET", "POST"])
        self.app.add_url_rule('/homepage/', view_func=self.homepage_view, methods=["GET", "POST"])
        self.app.add_url_rule('/addresume/', view_func=self.addresume_view, methods=["GET", "POST"])
        self.app.add_url_rule('/deleteresume/', view_func=self.deleteresume_view, methods=["GET", "POST"])
        self.app.add_url_rule('/updateresume/', view_func=self.updateresume_view, methods=["GET", "POST"])
        self.app.add_url_rule('/homepage/', view_func=self.homepage_view, methods=["GET", "POST"])
        self.app.add_url_rule('/homepage/<category>/category',view_func=self.homepage_view, methods=["GET", "POST"] )
        self.app.add_url_rule('/homepage/<location>/location',view_func=self.homepage_view, methods=["GET", "POST"] )
        self.app.add_url_rule('/homepage/<key>/key',view_func=self.homepage_view, methods=["GET", "POST"] )
        self.app.add_url_rule('/logOut', view_func=logOut)
        self.app.add_url_rule('/<int:passwordChange>/', view_func=self.authorization_view, methods=["GET", "POST"])
        
        self.app.add_url_rule('/deleteplacement/', view_func=self.deleteplacement_view, methods=["GET", "POST"])
        self.app.add_url_rule('/addplacement/', view_func=self.addplacement_view, methods=["GET", "POST"])
        self.app.add_url_rule('/updateplacement/', view_func=self.updateplacement_view, methods=["GET", "POST"])
        self.app.add_url_rule('/companyhomepage/', view_func=self.companyhomepage_view, methods=["GET", "POST"])
