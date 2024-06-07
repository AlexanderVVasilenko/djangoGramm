# feed/views.py
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, TemplateView

from feed.models import Post
from user_profile.forms import AuthorForm


class PostDetailView(DetailView):
    model = Post
    template_name = 'feed/post.html'


class HomePageView(TemplateView):
    model = Post
    template_name = 'feed/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            posts = Post.objects.all()
            context['object_list'] = posts
        else:
            form = AuthorForm()
            context['form'] = form
        return context

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['feed/home.html']
        else:
            return ['user_profile/login.html']

    def post(self, request, *args, **kwargs):
        form = AuthorForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']
            if "@" in email_or_username:
                user = auth.authenticate(email=email_or_username, password=password)
            else:
                user = auth.authenticate(username=email_or_username, password=password)

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                form.add_error(None, "Invalid username or password")

        return render(request, "user_profile/login.html", {"form": form})