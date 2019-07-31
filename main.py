import webapp2
import jinja2
import os
import logging



from google.appengine.api import images

from google.appengine.api import users
from google.appengine.ext import ndb



class Profile(ndb.Model):
    fullname = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    password = ndb.StringProperty(required = True)
    category = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    phone = ndb.IntegerProperty(required = True)
    usertype = ndb.StringProperty(required =True )

class signupprofile (webapp2.RequestHandler):
     def get(self):
         mainFeed_template = jinja_env.get_template('templates/signupprofile.html')
         self.response.write(mainFeed_template.render())  # the response

class Event(ndb.Model):
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    photo = ndb.BlobProperty(required=False)
    attendees = ndb.KeyProperty(kind = Profile, repeated = True)
    donations = ndb.KeyProperty(kind = "Donation", repeated = True)
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)

class Donation(ndb.Model):
    donation = ndb.IntegerProperty(required = True)
    event = ndb.KeyProperty(kind = Event)
    user = ndb.KeyProperty(kind=Profile)
    def describe(self):
        user = Profile.query().filter(self.user == Profile.key).get().full_name
        return "%s donated %s to %s" % (user, self.donation, self.event.title)

class Update(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/updateProfile.html')
        self.response.write(template.render())
    def post(self):
        location = self.request.get("location")
        category = self.request.get("category")
        bio = self.request.get("bio")
        update = Update(name = name, location = location, category = category,  bio = bio)
        update.put()
        self.redirect('/organizationProfilePage')


class MainHandler(webapp2.RequestHandler):
#   def get(self):
#
    def post(self):
        # Code to handle a first-time registration from the form:
        print 'MainHandler POST!!!!!!!!!'
        user = users.get_current_user()
        orguser = Profile(
            fullname=self.request.get('fullname'),
            email=user.email(),
            password=self.request.get('password'),
            location=self.request.get('location'),
            category=self.request.get('category'),
            phone= int(self.request.get('phone')),
            usertype=self.request.get('usertype'),
            )

        orguser.put()
        self.redirect('/')

class Image(ndb.Model):
    def get(self):
        product=ndb.Key(urlsafe=self.request.get("img_id")).get()
        if product.photo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(product.photo)
        else:
            self.response.out.write('No image')


jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))



class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/')
        self.response.write(template.render())

class mainFeed(webapp2.RequestHandler):
    def get(self):
        event_query = Event.query()
        event_list = event_query.fetch()
        for event in event_list:
            event.total = 0
            for donation in event.donations:
                event.total += donation.get().donation
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/')
        template_vars = {
            'event_list' : event_list,
            'currentProfile' : current_user,
            'signin_link' : signin_link,
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
        event = self.request.get("event")
        eventKey = ndb.Key(urlsafe=event)
        event = eventKey.get()
        template_vars = {
            'event' : event
        }
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        logging.info(user)
        eventKey = self.request.get("event")
        if not(user.key in event.attendees):
            if (event.attendees):
                event.attendees.append(user.key)
            else:
                event.attendees = [user.key]
        event.put()
        self.redirect('/')


class comment(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/comment.html')
        self.response.write(template.render())

class donate(webapp2.RequestHandler):
    def get(self):

        template = jinja_env.get_template('templates/donate.html')
        template_vars = {
            'urlsafeEvent' : self.request.get("event")
        }
        self.response.write(template.render(template_vars))
    def post(self):
        logging.info("POINT 1")
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        logging.info(user)
        eventKey = self.request.get("event")
        eventKey = ndb.Key(urlsafe=eventKey)
        logging.info(eventKey)
        logging.info("DONATION HERE")
        logging.info(self.request.get("donation"))
        amount = int(self.request.get("donation"))
        donation = Donation(donation = amount, event = eventKey, user = user.key)
        donation.put()
        event = eventKey.get()
        if not(donation.key in event.donations):
            if (event.donations):
                event.donations.append(donation.key)
            else:
                event.donations = [donation.key]
        event.put()
        self.redirect('/thankyou?event=' + str(eventKey.urlsafe()) + '&donation=' + str(amount))

class thankyou(webapp2.RequestHandler):
    def get(self):
        eventKey = self.request.get("event")
        logging.info("EVENT HERE")
        eventKey = ndb.Key(urlsafe=eventKey)
        logging.info(eventKey)
        event = eventKey.get()
        logging.info(event)
        donation = self.request.get("donation")
        template = jinja_env.get_template('templates/thankyou.html')
        template_vars = {
            'donation' : donation,
            'event' : event
        }
        self.response.write(template.render(template_vars))

class addEvent(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.response.write(template.render())
    def post(self):
        title = self.request.get("title")
        date = self.request.get("date")
        time = self.request.get("time")
        location = self.request.get("location")
        photo = images.resize(self.request.get("pic", 250, 250))
        attendees = []
        donations = []
        event = Event(title = title, date = date, time = time, location = location, attendees = attendees, donations = donations, photo = photo)
        event.put()
        self.redirect('/')



class OrgProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user().email()
        profile = Profile.query().filter(user == Profile.email).get()
        template_vars = {
            'profile' : profile,
        }
        template = jinja_env.get_template('templates/organizationProfilePage.html')
        self.response.write(template.render(template_vars))

    def post(self):
        template_vars = {
            "fullname": self.request.get("fullname"),
            "location": self.request.get("location"),
            "phone": self.request.get("phone"),
        }
        template = jinja_env.get_template('templates/organizationProfilePage.html')
        self.response.write(template.render(template_vars))

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/mainFeed')
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
        self.redirect('/')

app = webapp2.WSGIApplication([
('/', mainFeed),
('/mainhandler', MainHandler),
('/addEvent', addEvent),
# ('/mainFeed', mainFeed),
('/populateDatabase', populateDatabase),
('/donate', donate),
('/signup', signup),
('/collaborate', collaborate),
('/comment', comment),

('/signupprofile', signupprofile),
('/updateProfile', Update),
# ('/organizationProfilePage', organizationProfilePage),

# ('/logout', logout),
('/organizationProfilePage', OrgProfilePage),


# ('/updateProfile', updateProfile),
('/thankyou', thankyou),
# ('/organizationProfilePage', organizationProfilePage),
# ('/updateProfile', updateProfile)
], debug=True)
