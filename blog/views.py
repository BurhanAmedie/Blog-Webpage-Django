from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import posts
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

# Create your views here.

def home(request):
    context= {
    'posts' : posts.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = posts
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-Date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = posts
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5


    def get_queryset(self):
        user = get_object_or_404(User, username= self.kwargs.get('username'))
        return posts.objects.filter(author = user).order_by('-Date_posted')


class PostDetailView(DetailView):
    model = posts

class PostCreateView( LoginRequiredMixin, CreateView):
    model = posts
    fields = ['Title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = posts
    fields = ['Title', 'content']

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False







def about(request):
    return render(request, 'blog/about.html', {"Title": "about"})
