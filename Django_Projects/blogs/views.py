from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post
import json
from django.views.generic import (ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)

"""with open('posts.json') as f:
      posts_json = json.load(f  )
  for post in posts_json:
      post = Post(title = post['title'],content = post['content'],author_id = post['user_id'])
      post.save()
This is in the "python manage.py shell" to push all the post from the json files automatically"""

@login_required
def home(request):   # Function based views
    """ home function shouldn't be executed without login so "@login_required" decorated is used
    and that too for function based views. """
    context = {'Post' : Post.objects.all()}
    return render(request,'blogs/home.html',context)



class PostListView(LoginRequiredMixin, ListView): #Class based views
    """ Postlistview shouldn't be executed without login so "LoginRequiredMixin" is used
    and that too for class based views. """
    model = Post
    template_name = 'blogs/home.html'
    context_object_name = 'Post'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView): #Class based views
    """ Userlistview is for displaying all the posts related to a particular user. """
    model = Post
    template_name = 'blogs/user_posts.html'
    context_object_name = 'Post'
    ordering = ['-date_posted']
    paginate_by = 5
    def get_queryset(self):
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = "/"
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self,form):
        """This function is created just because we didnt add author above in the fields
        so without author a post cant be created.Before submitting the form we should add the author
        explicitly and that y we are overriding the form_valid here."""
        form.instance.author = self.request.user #setting the author
        return super().form_valid(form) # and validate the form in the parent class

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content' ]
    def form_valid(self,form):
        """This function is created just because we didnt add author above in the fields
        so without author a post cant be created.Before submitting the form we should add the author
        explicitly and that y we are overriding the form_valid here."""
        form.instance.author = self.request.user #setting the author
        return super().form_valid(form) # and validate the form in the parent class
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



@login_required
def about(request):
    return render(request,'blogs/about.html',{'title':'AboutPage'})
