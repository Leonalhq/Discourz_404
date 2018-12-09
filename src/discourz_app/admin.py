from django.contrib import admin
from discourz_app.models import Account, PollTopic, Debates, Chat, PastDebates, VotedUsers, Comment, Discussion

# Register your models here.
admin.site.register(Account)
admin.site.register(PollTopic)
admin.site.register(Debates)
admin.site.register(Chat)
admin.site.register(PastDebates)
admin.site.register(VotedUsers)
admin.site.register(Comment)
admin.site.register(Discussion)

username = "discourz404"
password = "discourz404"