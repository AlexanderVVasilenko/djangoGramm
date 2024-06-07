# user_profile/views.py

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView

from djangoGramm import settings
from feed.models import Post
from user_profile.forms import AuthorForm, EditProfileForm, SignUpForm
from user_profile.models import User


class LoginView(TemplateView):
    template_name = "user_profile/login.html"

    def get(self, request, *args, **kwargs):
        form = AuthorForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
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


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['pk']
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user)  # Assuming a Post model with a user field
        context['user'] = user
        context['posts'] = posts
        context['is_owner'] = self.request.user == user  # Check if the logged-in user is viewing their own profile
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "user_profile/edit_profile.html"
    form_class = EditProfileForm
    model = User

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user


class ResetPasswordView(PasswordResetView):
    template_name = "user_profile/password_reset.html"
    form_class = PasswordResetForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                token_generator=default_token_generator,
                from_email=settings.EMAIL_HOST_USER,
                email_template_name='user_profile/password_reset_email.html',
                subject_template_name="user_profile/password_reset_subject.txt"
            )
            return render(request, self.template_name, {
                "form": self.form_class(),
                "message": "We have sent you"
            })

        return render(request, self.template_name, {"form": form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user_profile/password_reset_confirm.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "user_profile/sign_up.html"

    def get_success_url(self):
        return reverse_lazy('my_profile', kwargs={'my_username': self.object.username})

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

