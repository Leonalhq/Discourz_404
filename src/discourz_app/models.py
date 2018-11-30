from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
import uuid
import json
from datetime import datetime   

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'account/user_{0}/{1}'.format(instance.user.username, filename)

def poll_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'poll_topic/poll_{0}/{1}'.format(instance.id, filename)

# Create your models here.
class Account(models.Model):
    #username = models.CharField(max_length=20, primary_key=True, default='1234')
    #password = models.CharField(max_length=20, default='1234')
    #email = models.EmailField(null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    imgUrl = "static/avatar/man1.png"
    img = models.ImageField(upload_to=user_directory_path, default=imgUrl)
    bio = models.TextField(max_length=500, default='tell us about yourself')
    tags = models.TextField(max_length=500, default='["General"]')
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    debates = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    def set_tags(self,x):
        self.tags = json.dumps(x)
    def get_tags(self):
        tags = json.loads(self.tags)
        i=0
        myTags=""
        while(i<len(tags)):
            myTags+=","+tags[i]
            i+=1
        return myTags[1:]
    def get_tag_list(self):
        return json.loads(self.tags)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.account.save()


class PollTopic(models.Model):
    #uuid = models.AutoField(primary_key=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular poll topic",
    )
    title = models.TextField(max_length=100, default='')
    options = models.TextField(max_length=500, default='')
    votes = models.TextField(max_length=500, default='')
    voters = models.TextField(max_length=2000, default='')
    owner =  models.ForeignKey("Account", on_delete=models.SET_NULL, null=True)
    imgUrl = "static/img/default.jpg"
    img = models.ImageField(upload_to=poll_directory_path, default=imgUrl)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Debates(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this Debate",
    )
    isOpen = models.BooleanField(default=False)
    #positionOnTopicOptions = (
    #    ('Yes', 'Yes'),
    #    ('No', 'No'),
    #    ('Agree', 'Agree'),
    #    ('Disagree', 'Disagree'),
    #    ('For', 'For'),
    #    ('Against', 'Against'),
    #    ('Former', 'Former'),
    #    ('Latter', 'Latter')
    #)
    # title = models.CharField(max_length=500, default='')
    position = models.CharField(max_length=100) #, default='Select Position', choices=positionOnTopicOptions)
    category = models.CharField(max_length=100, default='')
    topic = models.CharField(max_length=500, default='')
    initial_user = models.CharField(max_length=500, default='')
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.topic

class PastDebates(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this Debate",
    )
    #positionOnTopicOptions = (
    #    ('Yes', 'Yes'),
    #    ('No', 'No'),
    #    ('Agree', 'Agree'),
    #    ('Disagree', 'Disagree'),
    #    ('For', 'For'),
    #    ('Against', 'Against'),
    #    ('Former', 'Former'),
    #    ('Latter', 'Latter')
    #)
    user1 = models.CharField(max_length=500, default='')
    user2 = models.CharField(max_length=500, default='')
    user1Position = models.CharField(max_length=100) #default='Select Position', choices=positionOnTopicOptions)
    user2Position = models.CharField(max_length=100) #default='Select Position', choices=positionOnTopicOptions)
    user1votes = models.IntegerField(default=0)
    user2votes = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='')
    topic = models.CharField(max_length=500, default='')
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.topic

class Chat(models.Model):
    username = models.CharField(max_length=100, default='myusername')
    message = models.TextField(default='')
    debates = models.ForeignKey(PastDebates, on_delete=models.CASCADE)

class VotedUsers(models.Model):
    username = models.CharField(max_length=100, default='myusername')
    debateVoted = models.ForeignKey(PastDebates, on_delete=models.CASCADE)
