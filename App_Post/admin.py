from django.contrib import admin
from .models import Posts, LoveReact, Comment


# Register your models here.
admin.site.register(Posts)
admin.site.register(LoveReact)
admin.site.register(Comment)
