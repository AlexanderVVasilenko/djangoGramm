from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView

from feed.models import Post
from user_profile.forms import AuthorForm, EditProfileForm
from user_profile.models import User


def index(request):
    return "Hello World!"


def my_profile(request):
    return "Hello World!"


def settings(request):
    return "Hello World!"


class LoginView(TemplateView):
    template_name = "user_profile/index.html"

    def get(self, request, *args, **kwargs):
        form = AuthorForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = AuthorForm(request.POST)
        print("Form errors:", form.errors)
        print(form.cleaned_data)
        if form.is_valid():
            print(form)
            email_or_username = form.cleaned_data["email_or_username"]
            password = form.cleaned_data["password"]
            if "@" in str(email_or_username):
                user = authenticate(request, email=email_or_username, password=password)
            else:
                user = authenticate(request, username=email_or_username, password=password)

            if user is not None:
                login(request, user)
                print("Logged in successfully")
                return HttpResponseRedirect(reverse('my_profile', kwargs={'my_username': user.username}))
            else:
                form.add_error(None, "Invalid username or password")

        return render(request, self.template_name, {"form": form})


class ProfileView(TemplateView):
    template_name = "user_profile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['my_username']
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user)  # Assuming a Post model with a user field
        context['user'] = user
        context['posts'] = posts
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "user_profile/edit_profile.html"
    form_class = EditProfileForm
    model = User
    success_url = reverse_lazy("my_profile")

    def get_object(self):
        return self.request.user

