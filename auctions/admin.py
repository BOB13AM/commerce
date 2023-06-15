from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(listing)
admin.site.register(bids)
admin.site.register(invalidbid)
admin.site.register(comments)
admin.site.register(commentreply)
