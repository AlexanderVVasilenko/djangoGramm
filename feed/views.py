# feed/views.py

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.db.models import Q, QuerySet

from feed.forms import CommentForm, PostForm
from feed.models import Post, Photo
from user_profile.forms import AuthorForm
from user_profile.models import User


class SearchView(ListView):
    model = User
    template_name = 'feed/search.html'
    context_object_name = "users"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return User.objects.filter(
                Q(username__icontains=query) |
                Q(name__icontains=query)
            ).distinct()

        return User.objects.none()

    def get_context_data(self, **kwargs):
        s_context = super().get_context_data(**kwargs)
        s_context["query"] = self.request.GET.get("q", "")
        return s_context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'feed/post_create.html'
    success_url = reverse_lazy("feed:home")

    def form_valid(self, form, *args, **kwargs):
        print(self.request.FILES)
        form.instance.user = self.request.user
        self.object = form.save()

        files = form.cleaned_data.get("images")

        if files:
            form.instance.user = self.request.user
            for i, f in enumerate(files):
                Photo.objects.create(post=self.object, image=f, index=i)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print("Errors in form:", form.errors)
        print("Data у FILES:", self.request.FILES)
        print("Files in form:", form.files)  # Має бути не порожнім!
        print("Errors:", form.errors)
        return super().form_invalid(form)


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

    def get(self, request):
        """Render the login form on GET request."""
        form = AuthorForm()
        if not self.request.user.is_authenticated:
            return render(request, "user_profile/login.html", {"form": form})
        return super(HomePageView, self).get(request)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_pks = list(self.request.user.following.values_list('pk', flat=True))
            user_pks.append(self.request.user.pk)
            return Post.objects.filter(user__pk__in=user_pks).distinct().order_by('-pk')
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # posts = Post.objects.all()
            context['object_list'] = self.get_queryset()
            context['user'] = self.request.user
            context['comment_form'] = CommentForm()
            form = AuthorForm()
            context['form'] = form
        else:
            context['object_list'] = []
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
            try:
                if "@" in email_or_username:
                    email_or_username = User.objects.get(email=email_or_username).username
                user = auth.authenticate(username=email_or_username, password=password)
            except User.DoesNotExist:
                user = None

            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                return HttpResponseRedirect(reverse("feed:home"))
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

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('feed:home')))

        context = {
            'object': post,
            'comment_form': form,
        }
        return render(request, 'feed/post.html', context)


class ToggleLikeView(View):
    def post(self, request, *args, **kwargs):
        post_id = self.kwargs.get('pk')
        post = Post.objects.get(pk=post_id)

        like = post.likes.filter(user=request.user)
        if like.exists():
            like.delete()
            liked = False
        else:
            post.like_post(request.user)
            liked = True

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "liked": liked,
                "post_id": post_id,
                "message": "You have successfully liked",
                "liked_count": post.likes.count()
            })

        refer = request.META.get('HTTP_REFERER', reverse("feed:home"))
        return HttpResponseRedirect(refer)
