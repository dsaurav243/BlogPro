from django.shortcuts import render
from .models import Blog
from .forms import EmailForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.mail import send_mail
from .forms import CommentForm
from taggit.models import Tag

# Create your views here.

def post_list_view(request,tag_slug = None):
    posts = Blog.objects.all()

    tag = None
    if tag_slug:
        print(tag_slug)
        tag =  get_object_or_404(Tag,slug = tag_slug)
        print(tag)

        posts = posts.filter(tags__in =[tag])


    paginator = Paginator(posts,2)
    page_number =  request.GET.get('page')
    try:
        page_objects =  paginator.get_page(page_number)
    except PageNotAnInteger:
        page_objects =  paginator.get_page(1)
    except EmptyPage:
        page_objects =  paginator.get_page(paginator.num_pages)

    print(page_objects)
    print(type(page_objects))

    return render(request,'blogapp/list.html',{'posts':page_objects,'tag':tag})


def home_view(request):
    return render(request,'blogapp/home.html')

def detail_view(request,year,month,day,slug):
    post  = get_object_or_404(Blog,slug= slug,
                              status = 'published',
                              publish__year =  year,
                              publish__month = month,
                              publish__day = day)

    comments = post.comments.filter(active = True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request,'blogapp/detail.html',{'post':post, 'comments': comments, 'new_comment':new_comment,'comment_form':comment_form})




def mail_send_view(request,id):
    post = get_object_or_404(Blog,id=id,status='published')
    sent =  False
    if request.method == "POST":
        form =  EmailForm(request.POST)
        if form.is_valid():
            cd =  form.cleaned_data
            post_url =  request.build_absolute_uri(post.get_absolute_url())
            subject = "{} ({}) recommends you to read {} ".format(cd['name'],cd['sender'],post.title)
            message = "Read Post at : \n {}\n\n {}'s Comments: \n {}".format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,cd['sender'],[cd['receiver']])
            sent = True
    else:
        form = EmailForm()

    return render(request,'blogapp/sharebyemail.html',{'form':form , 'post':post,'sent':sent})

def testimonials_view(request):
    return render(request,'blogapp/testimonials.html')

def contact_view(request):
    return render(request,'blogapp/contact.html')

def services_view(request):
    return render(request,'blogapp/services.html')

