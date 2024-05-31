from django.contrib import admin
from django.contrib import admin
from .models import Department, Post, PostImage

admin.site.register(Department)
admin.site.register(Post)
admin.site.register(PostImage)