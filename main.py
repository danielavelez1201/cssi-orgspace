import webapp2
import jinja2
import os
import logging
import datetime
now = datetime.datetime.now()

from google.appengine.api import images

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

# MODELS
class Profile(ndb.Model):
    fullname = ndb.StringProperty(required = True)
    email = ndb.StringProperty(required = True)
    category = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = True)
    phone = ndb.IntegerProperty(required = True)
    bio = ndb.StringProperty(required = False)
    usertype = ndb.StringProperty(required =True)

class Event(ndb.Model):
    author = ndb.KeyProperty(kind = Profile)
    title = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = True)
    time = ndb.StringProperty(required = True)
    location = ndb.StringProperty(required = False)
    photo = ndb.BlobProperty(required=False)
    attendees = ndb.KeyProperty(kind = Profile, repeated = True)
    donations = ndb.KeyProperty(kind = "Donation", repeated = True)
    collaborators = ndb.KeyProperty(kind = "Collaborator", repeated = True)
    allComments = ndb.KeyProperty(kind = "Comment", repeated = True)
    def type(self):
        return "Event"
    def describe(self):
        return "%s on %s at %s at %s" % (event.title, event.date, event.time, event.location)

class Collaborator(ndb.Model):
    organization = ndb.KeyProperty(kind = Profile)
    description = ndb.StringProperty(required = True)
    event = ndb.KeyProperty(kind = Event)

class Post(ndb.Model):
    text = ndb.StringProperty(required = True)
    author = ndb.KeyProperty(kind = Profile)
    time = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = False)
    photo = ndb.BlobProperty(required=False)
    donations = ndb.KeyProperty(kind = "Donation", repeated = True)
    allComments = ndb.KeyProperty(kind = "Comment", repeated = True)
    def type(self):
        return "Post"

class Donation(ndb.Model):
    donation = ndb.IntegerProperty(required = True)
    event = ndb.KeyProperty(kind = Event, required = False)
    post = ndb.KeyProperty(kind = Post, required = False)
    user = ndb.KeyProperty(kind=Profile)

class Comment(ndb.Model):
    commentText = ndb.StringProperty(required = True)
    author = ndb.KeyProperty(kind = Profile)
    event = ndb.KeyProperty(kind = Event, required = False)
    post = ndb.KeyProperty(kind = Post, required = False)
    time = ndb.StringProperty(required = True)
    date = ndb.StringProperty(required = False)

# REQUEST HANDLERS

class Image(webapp2.RequestHandler):
    def get(self):
        product=ndb.Key(urlsafe=self.request.get("img_id")).get()
        if product.photo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(product.photo)
        else:
            self.response.out.write('No image')

class Update(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/updateProfile.html')
        self.response.write(template.render())
    def post(self):
        location = self.request.get("location")
        category = self.request.get("category")
        bio = self.request.get("bio")
        update = Update(name = name, location = location, category = category,  bio = bio)
        self.redirect('/organizationProfilePage')
        user = Profile.query().filter

class updateProfile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user().email()
        profile = Profile.query().filter(user == Profile.email).get()
        template_vars={
            "profile" : profile
        }
        template = jinja_env.get_template('templates/updateProfile.html')
        self.response.write(template.render(template_vars))

    def post(self):
        location = self.request.get("location")
        category = self.request.get("category")
        bio = self.request.get("bio")
        phone = self.request.get("phone")
        fullname = self.request.get("fullname")

        user = users.get_current_user().email()
        profile = Profile.query().filter(user == Profile.email).get()

        profile.location = self.request.get("location")
        profile.category = self.request.get("category")
        profile.bio = self.request.get("bio")
        profile.phone = int(self.request.get("phone"))

        profile.put()

        self.redirect("/organizationProfilePage")
        # user = Profile.query().filter

class signupprofile (webapp2.RequestHandler):
     def get(self):
         mainFeed_template = jinja_env.get_template('templates/signupprofile.html')
         self.response.write(mainFeed_template.render())  # the response

class searchresults(webapp2.RequestHandler):
    def get(self):
        search_query = self.request.get('search_query')
        category_query = self.request.get('category')
        location_query = self.request.get('location')
        result_profiles = Profile.query().filter(Profile.fullname == search_query).filter(Profile.category == category_query).filter(Profile.location == location_query).fetch()
        # Get all the profiles
        profiles = Profile.query().fetch()

        # Start with an empty set of locations
        locations = set()

        # Loop through the ofiles and add each location to the set
        for profile in profiles:
            locations.add(profile.location)
        # Pass the set of locations to Jinja

        template_vars = {
            'result_profiles' : result_profiles,
            'search_query' : search_query,
            'category_query' : category_query,
            'location_query': location_query,
            'locations' : locations,
        }
        template = jinja_env.get_template('templates/searchresults.html')
        self.response.write(template.render(template_vars))

class profilePage(webapp2.RequestHandler):
    def get(self):
        profileStr = self.request.get("profile")
        profileKey = ndb.Key(urlsafe= profileStr)
        profile = profileKey.get()
        template_vars = {
            'profile' : profile,
        }
        template = jinja_env.get_template('templates/profilePage.html')
        self.response.write(template.render(template_vars))

class MainHandler(webapp2.RequestHandler):
#   def get(self):
    def post(self):
        # Code to handle a first-time registration from the form:
        user = users.get_current_user()
        orguser = Profile(
            fullname=self.request.get('fullname'),
            email=user.email(),
            location=self.request.get('location'),
            category=self.request.get('category'),
            phone= int(self.request.get('phone')),
            usertype=self.request.get('usertype'),
            )

        orguser.put()
        self.redirect('/mainFeed')

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/mainFeed')
        self.response.write(template.render())

class mainFeed(webapp2.RequestHandler):
    def get(self):
        event_query = Event.query()
        event_list = event_query.fetch()
        for event in event_list:
            event.total = 0
            for donation in event.donations:
                event.total += donation.get().donation
        for event in event_list:
            logging.info(event)
            counter = 3
            event.recentComments = []
            if not(event.allComments == []):
                logging.info("DETECTED COMMENTS")
                for comment in event.allComments:
                    if(counter > 0):
                        event.recentComments.append(comment)
                        counter = counter -1
            logging.info(event.recentComments)
        post_query = Post.query()
        post_list = post_query.fetch()
        for post in post_list:
            post.total = 0
            for donation in post.donations:
                post.total += donation.get().donation
        logging.info("STARTING FOR LOOP HERE")
        for post in post_list:
            logging.info(post)
            counter = 3
            post.recentComments = []
            if not(post.allComments == []):
                for comment in post.allComments:
                    if(counter > 0):
                        post.recentComments.append(comment)
                        counter = counter -1
            logging.info(post.recentComments)
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/mainFeed')
        signout_link = users.create_logout_url('/')
        user = ""
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        userKey = user.Key
        template_vars = {
            'userKey' : userKey,
            'user' : user,
            'post_list' : post_list,
            'event_list' : event_list,
            'currentProfile' : current_user,
            'signin_link' : signin_link,
            'signout_link': signout_link,
        }
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render(template_vars))
    def post(self):
        template = jinja_env.get_template('templates/mainFeed.html')
        self.response.write(template.render())

class collaborate(webapp2.RequestHandler):
    def get(self):
        event = self.request.get("event")
        eventKey = ndb.Key(urlsafe=event)
        event = eventKey.get()
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        template_vars = {
            'user' : user,
            'urlsafeEvent' : self.request.get("event"),
            'event' : event
        }
        eventKey = self.request.get("event")
        template = jinja_env.get_template('templates/collaborate.html')
        self.response.write(template.render(template_vars))
    def post(self):
        event = self.request.get("event")
        eventKey = ndb.Key(urlsafe=event)
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        event = eventKey.get()
        description = self.request.get("description")
        collaborator = Collaborator(author = user.key, event = event.key, description = description).put()
        if not(collaborator in event.collaborators):
            if (event.collaborators):
                event.collaborators.append(collaborator)
            else:
                event.collaborators = [collaborator]
        event.put()
        self.redirect('/collaborators?event=' + str(eventKey.urlsafe()))

class EventAttendee(webapp2.RequestHandler):
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
        self.redirect('/mainFeed')

class postComment(webapp2.RequestHandler):
    def get(self):
        item = self.request.get("item")
        itemKey = ndb.Key(urlsafe=item)
        item = itemKey.get()
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        template_vars = {
            'user' : user,
            'urlsafeItem' : self.request.get("item"),
            'item' : item
        }
        template = jinja_env.get_template('templates/postComment.html')
        self.response.write(template.render(template_vars))
    def post(self):
        item = self.request.get("item")
        itemKey = ndb.Key(urlsafe=item)
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        item = itemKey.get()
        commentText = self.request.get("commentText")
        time = now.hour
        date = now.date
        logging.info("TYPE HERE")
        logging.info(type(item))
        if(item.type() == "Event"):
            comment = Comment(commentText = commentText, author = user.key, event = item.key, time = str(time), date = str(date)).put()
        else:
            comment = Comment(commentText = commentText, author = user.key, post = item.key, time = str(time), date = str(date)).put()
        if not(comment in item.allComments):
            if (item.allComments):
                item.allComments.append(comment)
            else:
                item.allComments = [comment]
        item.put()
        self.redirect('/allComments?item=' + str(itemKey.urlsafe()))

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
        amount = int(self.request.get("donation"))
        eventKey = self.request.get("event")
        eventKey = ndb.Key(urlsafe=eventKey)
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

class donatePost(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/donatePost.html')
        logging.info("GET POST HERE")
        logging.info(self.request.get("postItem"))
        template_vars = {
            'urlsafePost' : self.request.get("postItem")
        }
        self.response.write(template.render(template_vars))
    def post(self):
        logging.info("POST POST HERE")
        logging.info(self.request.get("postItem"))
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        logging.info(user)
        amount = int(self.request.get("donation"))
        postKey = self.request.get("postItem")
        postKey = ndb.Key(urlsafe=postKey)
        donation = Donation(donation = amount, post = postKey, user = user.key)
        donation.put()
        postItem = postKey.get()
        if not(donation.key in postItem.donations):
            if (postItem.donations):
                postItem.donations.append(donation.key)
            else:
                postItem.donations = [donation.key]
        postItem.put()
        self.redirect('/thankyouPost?postItem=' + str(postKey.urlsafe()) + '&donation=' + str(amount))

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

class thankyouPost(webapp2.RequestHandler):
    def get(self):
        postKey = self.request.get("postItem")
        logging.info("EVENT HERE")
        postKey = ndb.Key(urlsafe=postKey)
        logging.info(postKey)
        postItem = postKey.get()
        donation = self.request.get("donation")
        template = jinja_env.get_template('templates/thankyouPost.html')
        template_vars = {
            'postItem' : postItem,
            'donation' : donation
        }
        self.response.write(template.render(template_vars))

class addEvent(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.response.write(template.render())
    def post(self):
        user = users.get_current_user().email()
        author = Profile.query().filter(user == Profile.email).get()
        authorKey = author.key
        title = self.request.get("title")
        date = self.request.get("date")
        time = self.request.get("time")
        location = self.request.get("location")
        logging.info("PHOTO HERE")
        logging.info(self.request.get("photo"))
        photo = images.resize(self.request.get("photo"), 650, 650)
        attendees = []
        donations = []
        collaborators = []
        allComments = []
        event = Event(allComments = allComments, photo = photo, author = authorKey, title = title, date = date, time = time, location = location, attendees = attendees, donations = donations, collaborators = collaborators)
        event.put()
        self.redirect('/mainFeed')

class OrgProfilePage(webapp2.RequestHandler):
    def get(self):
        profileKey = self.request.get("profile")
        profileKey = ndb.Key(urlsafe=profileKey)
        profile = profileKey.get()
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        if profile.fullname == user.fullname:
            profile.isUser = True
        else:
            profile.isUser = False
        template_vars = {
            'profile' : profile,
        }
        template = jinja_env.get_template('templates/organizationProfilePage.html')
        self.response.write(template.render(template_vars))

class populateDatabase(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/addEvent.html')
        self.redirect('/mainFeed')
        self.response.write(template.render())

class About(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        signin_link = users.create_login_url('/mainFeed')
        template_vars = {
            'signin_link' : signin_link
        }
        template = jinja_env.get_template('templates/about.html')
        self.response.write(template.render(template_vars))

class MeetTheTeam(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/meetTheTeam.html')
        self.response.write(template.render())

class createPost(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/createPost.html')
        self.response.write(template.render())
    def post(self):
        postText = self.request.get("postText")
        logging.info("TEXT HERE")
        logging.info(postText)
        photo = self.request.get("photo")
        user = users.get_current_user().email()
        user = Profile.query().filter(user == Profile.email).get()
        photo = images.resize(self.request.get("photo"), 650, 650)
        userKey = user.key
        time = now.hour
        date = now.date
        donations = []
        post = Post(photo = photo, text = postText, author = userKey, time = str(time), date = str(date), donations = donations)
        post.put()
        self.redirect('/mainFeed')

class collaborators(webapp2.RequestHandler):
    def get(self):
        eventKey = self.request.get("event")
        eventKey = ndb.Key(urlsafe=eventKey)
        logging.info(eventKey)
        event = eventKey.get()
        template_vars = {
            'event': event
        }
        template = jinja_env.get_template('templates/collaborators.html')
        self.response.write(template.render(template_vars))

class allComments(webapp2.RequestHandler):
    def get(self):
        itemKey = self.request.get("item")
        itemKey = ndb.Key(urlsafe=itemKey)
        item = itemKey.get()
        logging.info("AUTHOR HERE")
        logging.info(item.author)
        template_vars = {
            'item': item
        }
        template = jinja_env.get_template('templates/allComments.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
('/mainFeed', mainFeed),
('/mainhandler', MainHandler),
('/addEvent', addEvent),
('/populateDatabase', populateDatabase),
('/donate', donate),
('/attendevent', EventAttendee),
('/collaborate', collaborate),
('/postComment', postComment),
('/allComments', allComments),
('/donatePost', donatePost),
('/createPost', createPost),
('/signupprofile', signupprofile),
('/updateProfile', updateProfile),
('/thankyouPost', thankyouPost),
('/', About),
('/searchresults', searchresults),
('/collaborators', collaborators),
('/profilePage', profilePage),
('/meetTheTeam', MeetTheTeam),
('/image', Image),
('/organizationProfilePage', OrgProfilePage),
('/thankyou', thankyou),
], debug=True)
