from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, UpdateView, CreateView, DetailView, RedirectView

from djangoGramm import settings
from feed.models import Post
from user_profile.forms import AuthorForm, EditProfileForm, BasicSignUpForm, FinalSignUpForm
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
                if user.is_active:
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
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        print("Set Password form is valid!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class SignUpView(CreateView):
    form_class = BasicSignUpForm
    template_name = "user_profile/sign_up.html"
    success_url = reverse_lazy('confirmation_sent')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        self.send_confirmation_email(user)
        return response

    def send_confirmation_email(self, user):
        current_site = get_current_site(self.request)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_url = reverse_lazy('confirm_email', kwargs={'uidb64': uidb64, 'token': token})

        subject = 'Confirm Your Email'
        message = render_to_string(
            'user_profile/confirmation_email.html',
            {'confirm_url': confirm_url, "username": user.username, "domain": current_site.domain})

        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])


class ConfirmEmailView(RedirectView):
    url = reverse_lazy('final_signup')

    def get_redirect_url(self, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token) and user:
                user.is_active = True
                user.save()
                login(self.request, user)
                return super().get_redirect_url(*args, **kwargs)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(self.request, 'user_profile/activation_invalid.html')

        return reverse_lazy('confirmation_failed')


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
