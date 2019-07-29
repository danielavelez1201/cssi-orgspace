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

class Star(ndb.Model):
    name = ndb.StringProperty(required = True)
    birthyear = ndb.IntegerProperty(required = True)
    birthplace = ndb.StringProperty(required = True)
    wins = ndb.IntegerProperty(required = False)

    def describe(self):
        return "%s was born in %s in %s and has had %s wins" % (star.name, star.birthyear, star.birthplace, star.wins)

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
        template = jinja_env.get_template('templates/main.html')
        self.redirect('/')
        # self.response.write(template.render(template_vars))


<<<<<<< HEAD





=======
>>>>>>> e6828902e522dbc8ceea0276dca9ad1acc9970b1
class MainPage(webapp2.RequestHandler):
    def get(self):
        movie_query = Movie.query()
        movie_list = movie_query.fetch()
        star_query = Star.query()
        star_list = star_query.fetch()
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/')
        template_vars = {
            'star_list' : star_list,
            'movies': movie_list,
            'currentUser' : current_user
        }
        logging.info('***')
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('templates/main.html')
        self.response.write(template.render())

<<<<<<< HEAD
class addMovie(webapp2.RequestHandler):
=======
class addEvent(webapp2.RequestHandler):
>>>>>>> e6828902e522dbc8ceea0276dca9ad1acc9970b1
    def get(self):
        star_query = Star.query()
        star_list = star_query.fetch()
        template_vars = {
            'star_list' : star_list
        }
        template = jinja_env.get_template('templates/addMovie.html')
        self.response.write(template.render(template_vars))
    def post(self):
        title = self.request.get("title")
        runtime = float(self.request.get("runtime"))
        rating = float(self.request.get("rating"))
        star_keys = self.request.get("star_keys")
        movie = Movie(title = title, runtime = runtime, rating = rating, star_keys = star_keys)
        logging.info("Reaching this line")
        logging.info(star_keys)
        movie.put()
        self.redirect('/')


app = webapp2.WSGIApplication([
('/', MainPage),
<<<<<<< HEAD
('/profile',
=======
('/profile', Profile),
('/login', Login),
('/register', Register),
])
>>>>>>> e6828902e522dbc8ceea0276dca9ad1acc9970b1
