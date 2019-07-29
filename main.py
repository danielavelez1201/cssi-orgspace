import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
from google.appengine.ext import ndb



def addStar():
    name = raw_input("What is the star name?")
    birthyear = raw_input("What year were they born in?")
    birthplace = raw_input("Where were they born?")
    wins = raw_input("How many wins do they have?")

class Event(ndb.Model):
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)

class Movie(ndb.Model):
    title = ndb.StringProperty(required = True)
    runtime = ndb.IntegerProperty(required = True)
    rating = ndb.FloatProperty(required= False, default = 0)
    star_keys = ndb.KeyProperty(kind = Star, required=False, repeated = True)
    def describe(self):
        return "%s is %d minute(s) long, with a rating of %f" % (self.title, self.runtime, self.rating)


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))




class populateDatabase(webapp2.RequestHandler):
    def get(self):
        hemsworth_key = Star(name = "Liam Hemsworth", birthyear= 1990, birthplace = 'Australia', wins = 6).put()
        lawrence_key = Star(name = "Jennifer Lawrence", birthyear= 1990, birthplace = 'Kentucky', wins = 117).put()
        Movie(title = "The Hunger Games", runtime = 142, rating = 7.2, star_keys = [hemsworth_key, lawrence_key]).put()
        Movie(title = "Independence Day: Resurgence", runtime = 120, rating = 5.2, star_keys = [hemsworth_key]).put()
        # template = jinja_env.get_template('templates/main.html')
        self.redirect('/')
        # self.response.write(template.render(template_vars))

class MainPage(webapp2.RequestHandler):
    def get(self):
        event_query = Event.query()
        event_list = event_query.fetch()
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/')
        template_vars = {
            'event_list' : event_list,
            'currentUser' : current_user
        }
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render())




class addEvent(webapp2.RequestHandler):
    def get(self):
        star_query = Star.query()
        star_list = star_query.fetch()

        template_vars = {
            'time': time
        }
        template = jinja_env.get_template('templates/addEvent.html')
        self.response.write(template.render(template_vars))
    def post(self):
        name = self.request.get("name")
        date = self.request.get("date")
        time = self.request.get("time")
        location = self.request.get("location")
        event = Event(title = title, date = date, time = time, location = location)
        event.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
('/', MainPage),
('/addEvent', addEvent)
])
