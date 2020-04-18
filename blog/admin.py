from django.contrib import admin

# Register your models here.
from django.contrib import admin
from blog.models import Post, Category, Comment, Profile, ReplyComment

class PostAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(ReplyComment)