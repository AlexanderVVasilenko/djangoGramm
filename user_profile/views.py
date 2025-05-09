from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, RedirectView, FormView

from djangoGramm import settings
from feed.models import Post
from user_profile.forms import AuthorForm, EditProfileForm, BasicSignUpForm, FinalSignUpForm, CustomPasswordResetForm
from user_profile.models import User

import logging

logger = logging.getLogger(__name__)


class FollowUserView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_to_follow = User.objects.get(username=kwargs['username'])
            request.user.follow(user_to_follow)
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': user_to_follow.username}))
        return HttpResponseRedirect(reverse('home'))


class UnfollowUserView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_to_unfollow = User.objects.get(username=kwargs['username'])
            request.user.unfollow(user_to_unfollow)
            return HttpResponseRedirect(reverse('profile', kwargs={'pk': user_to_unfollow.username}))
        return HttpResponseRedirect(reverse('home'))


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "user_profile/user_profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['pk']
        user = get_object_or_404(User, username=username)
        posts = Post.objects.filter(user=user)
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
    form_class = CustomPasswordResetForm

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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        print("Set Password form is valid!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(FormView):
    form_class = BasicSignUpForm
    template_name = "user_profile/sign_up.html"
    success_url = reverse_lazy('confirmation_sent')

    def get_form_kwargs(self):
        """Ensure no `instance` argument is passed to `BasicSignUpForm`"""
        kwargs = super().get_form_kwargs()
        kwargs.pop("instance", None)
        return kwargs

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        logger.debug(f"Processing sign up form: {email}, {username}")

        if form.inactive_user:
            self.send_confirmation_email(form.inactive_user)
            return self.redirect_to_confirmation()

        active_users = [User.objects.filter(email=email, is_active=True).first(),
                        User.objects.filter(username=username, is_active=True).first()]
        if any(active_users):
            if active_users[0]:
                form.add_error("email", "Email already registered")
            elif active_users[1]:
                form.add_error("username", "Username already registered")
            return self.form_invalid(form)

        user = User(username=username, email=email)
        user.is_active = False
        user.set_password(password)
        user.save()
        logger.debug(f"New user registered: {email}")

        self.send_confirmation_email(user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        logger.error(f"Invalid form: {form.errors}")
        return self.render_to_response(self.get_context_data(form=form))

    def send_confirmation_email(self, user):
        """Send confirmation email to user with activation link."""
        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = reverse_lazy('confirm_email', kwargs={'uidb64': uidb64, 'token': token})

        subject = 'Confirm Your Email'
        message = render_to_string(
            'user_profile/confirmation_email.html',
            {'confirm_url': confirm_url, "username": user.username, "domain": current_site.domain})

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

    def redirect_to_confirmation(self):
        """Redirect to the confirmation sent page."""
        return render(
            self.request,
            "user_profile/confirmation_sent.html",
            {"email": self.request.POST.get("email")}
        )


class ConfirmEmailView(RedirectView):
    url = reverse_lazy('final_signup')

    def get_redirect_url(self, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.error(f"Invalid UID: {uidb64}")
            return render(self.request, "user_profile/activation_invalid.html")

        if not default_token_generator.check_token(user, token):
            logger.error(f"Ivalid token: {token}")
            return super().get_redirect_url(*args, **kwargs)
        
        if user.is_active:
            logger.info(f"User {user.username} as {user.email} has been activated successfully yet.")
            return super().get_redirect_url(*args, **kwargs)
        
        user.is_active = True
        user.save()
        login(self.request, user)
        return super().get_redirect_url(*args, **kwargs)


def custom_logout(request):
    logout(request)
    return redirect(reverse('home'))


class ConfirmationSentView(TemplateView):
    template_name = 'user_profile/confirmation_sent.html'


class FinalSignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'user_profile/final_signup.html', {"form": FinalSignUpForm()})

    def post(self, request, *args, **kwargs):
        form = FinalSignUpForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile', kwargs={'pk': request.user.pk}))
        return render(request, 'user_profile/final_signup.html', {"form": form})
