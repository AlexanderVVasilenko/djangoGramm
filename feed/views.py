from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView

from feed.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'feed/post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'feed/post.html'


def profile(request, username=None):
    return HttpResponse("")
