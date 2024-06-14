from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, TemplateView

from feed.forms import CommentForm
from feed.models import Post
from user_profile.forms import AuthorForm


class PostDetailView(DetailView):
    model = Post
    template_name = 'feed/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class HomePageView(TemplateView):
    template_name = 'feed/home.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            posts = Post.objects.all()
            context['object_list'] = posts
            context['user'] = self.request.user
            context['comment_form'] = CommentForm()
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
                if user.is_active:
                    auth.login(request, user)
                return HttpResponseRedirect(reverse("home"))
            else:
                form.add_error(None, "Invalid username or password")

        return render(request, "user_profile/login.html", {"form": form})


class CreateCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        form = CommentForm(request.POST)
        post = Post.objects.get(pk=post_id)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            referer = request.META.get('HTTP_REFERER', '')

            if reverse('post', kwargs={'pk': post_id}) in referer:
                return HttpResponseRedirect(reverse('post', kwargs={'pk': post_id}))
            elif reverse('home') in referer:
                return HttpResponseRedirect(reverse('home'))

        context = {
            'object': post,
            'comment_form': form,
        }
        return render(request, 'feed/post.html', context)
