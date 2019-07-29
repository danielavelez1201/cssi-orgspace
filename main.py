import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
from google.appengine.ext import ndb


<<<<<<< HEAD

=======
>>>>>>> c4975ec6d1e23ae5c8d23ee779096d7f2f26e313
class User(ndb.Model):
    full_name = ndb.StringProperty()
    email = ndb.StringProperty()
    location = ndb.StringProperty()
    phone = ndb.IntegerProperty()
<<<<<<< HEAD
=======

class Event(ndb.Model):
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Donation(nbd.Model):
    donation = nbd.IntegerProperty(required = True)
    user = nbd.StringProperty

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/mainFeed')
        self.response.write(template.render())

class mainFeed(webapp2.RequestHandler):
    def get(self):
        event_query = Event.query()
        event_list = event_query.fetch()
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/')
        template_vars = {
            'event_list' : event_list,
            'currentUser' : current_user
        }
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render())




class addEvent(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.response.write(template.render())
    def post(self):
        title = self.request.get("title")
        date = self.request.get("date")
        time = self.request.get("time")
        location = self.request.get("location")
        event = Event(title = title, date = date, time = time, location = location)
        event.put()
        self.redirect('/mainFeed')

>>>>>>> c4975ec6d1e23ae5c8d23ee779096d7f2f26e313



class MainHandler(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()

      if user:
          signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
          email_address = user.nickname()
          orguser = User.query().filter(User.email == email_address).get()
          # If the user is registered...
          if orguser:
              # Greet them with their personal information
              self.response.write('''
              Welcome %s (%s)! <br> %s <br>''' % (
              orguser.full_name,
              email_address,
              signout_link_html))
              self.redirect('/mainFeed')
              # If the user isn't registered...
          else:
              # Offer a registration form for a first-time visitor:
                   self.response.write('''
                   Welcome to our site, %s!  Please sign up! <br>
                   <form method="post" action="/">
                   <label> Full Name:
                   <input type="text" name="first_name">
                   </label>
                    <label> Location:
                    <input type="text" name="location">
                    </label>
                     <label> Phone:
                     <input type="integer" name="phone">
                     </label>
                     <label> User Type: Organization
                     <input type="radio" name="organization" value = "organization">
                     </label>
                      <label>  User Type: User
                      <input type="radio" name="organization" value = "user" >
                      </label>
                   <input type="submit">
              </form><br> %s <br>
              ''' % (email_address, signout_link_html))
      else:
          # If the user isn't logged in...
          login_url = users.create_login_url('/')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          # Prompt the user to sign in.
          self.response.write('Please log in.<br>' + login_html_element)
  def post(self):
    # Code to handle a first-time registration from the form:
    user = users.get_current_user()
    orguser = User(
        full_name=self.request.get('full_name'),
        email=user.nickname(),
        location=self.request.get('location'),
        phone= int(self.request.get('phone')))

    orguser.put()
    self.redirect('/')

<<<<<<< HEAD

class Event(ndb.Model):
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))




class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/mainFeed')
        self.response.write(template.render())

class mainFeed(webapp2.RequestHandler):
    def get(self):
        event_query = Event.query()
        event_list = event_query.fetch()
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/')
        template_vars = {
            'event_list' : event_list,
            'currentUser' : current_user
        }
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render())




class addEvent(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.response.write(template.render())
    def post(self):
        title = self.request.get("title")
        date = self.request.get("date")
        time = self.request.get("time")
        location = self.request.get("location")
        event = Event(title = title, date = date, time = time, location = location)
        event.put()
        self.redirect('/mainFeed')

# class usertype (webapp2.RequestHandler):
#
#         }
#
#         template = jinja_env.get_template('templates/home.html')
#         self.response.write(template.render(template_vars))





#
# class Star(ndb.Model):
#     name = ndb.StringProperty(required = True)
#     birthyear = ndb.IntegerProperty(required = True)
#     birthplace = ndb.StringProperty(required = True)
#     wins = ndb.IntegerProperty(required = False)
#
#     def describe(self):
#         return "%s was born in %s in %s and has had %s wins" % (star.name, star.birthyear, star.birthplace, star.wins)
#
# class Movie(ndb.Model):
#     title = ndb.StringProperty(required = True)
#     runtime = ndb.IntegerProperty(required = True)
#     rating = ndb.FloatProperty(required= False, default = 0)
#     star_keys = ndb.KeyProperty(kind = Star, required=False, repeated = True)
#     def describe(self):
#         return "%s is %d minute(s) long, with a rating of %f" % (self.title, self.runtime, self.rating)
#
# def addStar():
#     name = raw_input("What is the star name?")
#     birthyear = raw_input("What year were they born in?")
#     birthplace = raw_input("Where were they born?")
#     wins = raw_input("How many wins do they have?")
#
# class Event(ndb.Model):
#     title = ndb.StringProperty(required = True)
#     date = ndb.StringProperty(required = True)
#     time = ndb.StringProperty(required = True)
#     location = ndb.StringProperty(required = False)
#     def describe(self):
#         return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)
#
# class Movie(ndb.Model):
#     title = ndb.StringProperty(required = True)
#     runtime = ndb.IntegerProperty(required = True)
#     rating = ndb.FloatProperty(required= False, default = 0)
#     star_keys = ndb.KeyProperty(kind = Star, required=False, repeated = True)
#     def describe(self):
#         return "%s is %d minute(s) long, with a rating of %f" % (self.title, self.runtime, self.rating)
#
#
# jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))
#
#
#
#
# class populateDatabase(webapp2.RequestHandler):
#     def get(self):
#         hemsworth_key = Star(name = "Liam Hemsworth", birthyear= 1990, birthplace = 'Australia', wins = 6).put()
#         lawrence_key = Star(name = "Jennifer Lawrence", birthyear= 1990, birthplace = 'Kentucky', wins = 117).put()
#         Movie(title = "The Hunger Games", runtime = 142, rating = 7.2, star_keys = [hemsworth_key, lawrence_key]).put()
#         Movie(title = "Independence Day: Resurgence", runtime = 120, rating = 5.2, star_keys = [hemsworth_key]).put()
#         # template = jinja_env.get_template('templates/main.html')
#         self.redirect('/')
#         # self.response.write(template.render(template_vars))


#
#
# class MainPage(webapp2.RequestHandler):
#     def get(self):
#         movie_query = Movie.query()
#         movie_list = movie_query.fetch()
#         star_query = Star.query()
#         star_list = star_query.fetch()
#         current_user = users.get_current_user()
#         signin_link = users.create_login_url('/')
#         template_vars = {
#             'star_list' : star_list,
#             'movies': movie_list,
#             'currentUser' : current_user
#         }
#         logging.info('***')
#         template = jinja_env.get_template('templates/main.html')
#         self.response.write(template.render(template_vars))
#     def post(self):
#         template = jinja_env.get_template('templates/main.html')
#         self.response.write(template.render())
#
#
#
#
# class addEvent(webapp2.RequestHandler):
#     def get(self):
#         star_query = Star.query()
#         star_list = star_query.fetch()
#         template_vars = {
#             'star_list' : star_list
#         }
#         template = jinja_env.get_template('templates/addMovie.html')
#         self.response.write(template.render(template_vars))
#     def post(self):
#         title = self.request.get("title")
#         runtime = float(self.request.get("runtime"))
#         rating = float(self.request.get("rating"))
#         star_keys = self.request.get("star_keys")
#         movie = Movie(title = title, runtime = runtime, rating = rating, star_keys = star_keys)
#         logging.info("Reaching this line")
#         logging.info(star_keys)
#         movie.put()
#         self.redirect('/')


=======


>>>>>>> c4975ec6d1e23ae5c8d23ee779096d7f2f26e313
app = webapp2.WSGIApplication([
('/', MainHandler),
('/addEvent', addEvent),
('/mainFeed', mainFeed),
('/populateDatabase', populateDatabase),
# ('/organizationProfilePage', organizationProfilePage),
# ('/updateProfile', updateProfile)
], debug=True)
<<<<<<< HEAD
# =======
# class MainPage(webapp2.RequestHandler):
#     def get(self):
#         event_query = Event.query()
#         event_list = event_query.fetch()
#         current_user = users.get_current_user()
#         signin_link = users.create_login_url('/')
#         template_vars = {
#             'event_list' : event_list,
#             'currentUser' : current_user
#         }
#         template = jinja_env.get_template('templates/main.html')
#         self.response.write(template.render(template_vars))
#     def post(self):
#         template = jinja_env.get_template('templates/main.html')
#         self.response.write(template.render())
#
#
#
#
# class addEvent(webapp2.RequestHandler):
#     def get(self):
#         star_query = Star.query()
#         star_list = star_query.fetch()
#
#         template_vars = {
#             'time': time
#         }
#         template = jinja_env.get_template('templates/addEvent.html')
#         self.response.write(template.render(template_vars))
#     def post(self):
#         name = self.request.get("name")
#         date = self.request.get("date")
#         time = self.request.get("time")
#         location = self.request.get("location")
#         event = Event(title = title, date = date, time = time, location = location)
#         event.put()
#         self.redirect('/')
#
#
# app = webapp2.WSGIApplication([
# ('/', MainPage),
# ('/addEvent', addEvent)
# ])
# >>>>>>> 7c40a38f2050eccdcb3be369013290eb415b8182
=======
>>>>>>> c4975ec6d1e23ae5c8d23ee779096d7f2f26e313
