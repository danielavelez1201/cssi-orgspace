import webapp2
import jinja2
import os
import logging
from google.appengine.api import users
from google.appengine.ext import ndb



class User(ndb.Model):
    fullname = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    phone = ndb.IntegerProperty(required = True)

class MainHandler(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()
      if user:
          signout_link_html = '<a href="%s">sign out</a>' % (
                user.create_logout_url('/mainFeed'))
          email_address = user.email()
          orguser = user.query().filter(user.email == email_address).get()
          # If the user is registered...
          if orguser:
              # Greet them with their personal information
              self.response.write('''
              Welcome %s (%s)! <br> %s <br>''' % (
              orguser.fullname,
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
                   <input type="text" name="fullname">
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
          login_url = profile.create_login_url('/')
          login_html_element = '<a href="%s">Sign in</a>' % login_url
          # Prompt the user to sign in.
          self.response.write('Please log in.<br>' + login_html_element)
  def post(self):
    # Code to handle a first-time registration from the form:
    user = user.get_current_user()
    orguser = Profile(
        fullname=self.request.get('fullname'),
        email=profile.email(),
        location=self.request.get('location'),
        phone= int(self.request.get('phone')))

    orguser.put()
    self.redirect('/mainFeed')



class Event(ndb.Model):
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))


class Donation(ndb.Model):
    donation = ndb.IntegerProperty(required = True)
    user = ndb.StringProperty

    event = ndb.KeyProperty(kind = Event, repeated = True)
    user = ndb.KeyProperty(kind = user,  repeated = True)
    def describe(self):
        return "%s donated %s to %s" % (donation.user.name, donation.donation, donation.event.title)

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

class collaborate(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/collaborate.html')
        self.response.write(template.render())

class signup(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/signup.html')
        self.response.write(template.render())
class comment(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/comment.html')
        self.response.write(template.render())

class donate(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/donate.html')
        self.response.write(template.render())
    def post(self):
        donation = self.request.get("donation")
        donation = Donation(donation = donation, event = event, user = user)
        donation.put()
        self.redirect('/thankyou')

class thankyou(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/thankyou.html')
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



class OrgProfilePage(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/organizationProfilePage.html')
        self.response.write(template.render())

class Update(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/updateProfile.html')
        self.response.write(template.render())
    def post(self):
        name = self.request.get("name")
        location = self.request.get("location")
        category = self.request.get("date")
        bio = self.request.get("bio")
        update = Update(name = title, location = location, category = category,  bio = bio)
        update.put()
        self.redirect('/organizationProfilePage')

class MainHandler(webapp2.RequestHandler):
  def get(self):
      user = users.get_current_user()


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



class logout(webapp2.RequestHandler):
    def post(self):
        self.redirect('/')

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

app = webapp2.WSGIApplication([
('/', mainFeed),
('/addEvent', addEvent),
# ('/mainFeed', mainFeed),
('/populateDatabase', populateDatabase),
('/donate', donate),
('/signup', signup),
('/collaborate', collaborate),
('/comment', comment),
('/logout', logout),
# ('/organizationProfilePage', organizationProfilePage),
# ('/updateProfile', updateProfile),
('/thankyou', thankyou),
# ('/organizationProfilePage', organizationProfilePage),
# ('/updateProfile', updateProfile)
], debug=True)
