from django.contrib import admin
from discourz_app.models import Account, PollTopic, Debates, Chat, PastDebates

# Register your models here.
admin.site.register(Account)
admin.site.register(PollTopic)
admin.site.register(Debates)
admin.site.register(Chat)
admin.site.register(PastDebates)

username = "discourz404"
password = "discourz404"