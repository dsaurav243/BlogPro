from django.contrib import admin
from .models import Blog
from .models import Comment

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','body','publish','created','updated','status']
    prepopulated_fields = {'slug':('title',)}
    list_filter = ('author','status')
    search_fields = ('title','body')
    raw_id_fields = ('author',)
admin.site.register(Blog,BlogAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','body','post','created_on','active']
    list_filter = ('active','created_on')
    search_fields = ('name','email','body')
    actions = ['approve_comments']

    def approve_comments(self,request,queryset):
        queryset.update(active = True)


admin.site.register(Comment,CommentAdmin)







