from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.urlresolvers import reverse
from django.utils.timezone import now

class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(
            votes=Count('vote')).order_by('-rank_score', '-votes')


class Link(models.Model):
    title = models.CharField("Event Name", max_length=100)
    #eventtype = models.CharField("Enter Event type (eg:Hackathon/Discussion etc)", max_length=200)
    submitter = models.ForeignKey(User)
    submitted_on = models.DateTimeField(auto_now_add=True)
    rank_score = models.FloatField(default=0.0)
    url = models.URLField("Event URL", max_length=250, blank=True)
    logo = models.URLField("Event Logo URL", max_length=250)
    address = models.CharField("Enter the Landmark", max_length=200)
    phone = models.CharField("Phone Number", max_length=10)
    email =models.CharField("Contact Email id", max_length=50)
    eventdate = models.DateTimeField("Event Date")
    description = models.TextField(blank=True)

    with_votes = LinkVoteCountManager()
    objects = models.Manager()            # default manager

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("link_detail", kwargs={"pk": str(self.id)})

    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.submitted_on
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

class idea(models.Model):
    teamname = models.CharField("Enter Your Team name",max_length=100)
    logo = models.URLField("url of ur logo")
    idea = models.TextField("Describe ur idea")
    url = models.URLField("Link to ur project")
    s1 = models.URLField("screen shot1 URL")
    s2 = models.URLField("screen shot2 URL")
    s3 = models.URLField("screen shot3 URL")
    hackathon = models.ForeignKey('Link')

    def __unicode__(self):
        return self.teamname

class Vote(models.Model):
    voter = models.ForeignKey(User)
    link = models.ForeignKey(Link)

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.link.title)

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    # Extra attributes
    bio = models.TextField(null=True)

    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
