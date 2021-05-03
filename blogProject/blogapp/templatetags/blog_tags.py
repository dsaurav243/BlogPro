from blogapp.models import Blog
from django import template
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Blog.objects.count()

@register.inclusion_tag('blogapp/latest_post123.html')
def show_latest_posts():
    latest_posts = Blog.objects.order_by('-publish')[:3]
    most_commented = Blog.objects.annotate(total_comments=Count('comments')).order_by('-total_comments')[:4]
    return {'latest_posts':latest_posts,'most_commented':most_commented}


