from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, TemplateView, View

from .models import Post, Comment
from .forms import CommentModelForm


class HomeView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)

        now = timezone.now()
        posts = Post.objects.all()
        # ctx['posts'] = Post.objects.all()
        for post in posts:
            num_votes = post.upvotes.count()
            num_comments = post.comment_set.count()
            date_diff = now - post.submitted_on
            number_of_days_since_submission = date_diff.days
            post.rank = num_votes + num_comments - number_of_days_since_submission

        sorted_posts = sorted(posts, key=lambda x: x.rank, reverse=True)
        ctx['posts'] = sorted_posts

        return ctx


class NewPostView(CreateView):
    model = Post
    fields = (
        'title', 'body'
    )

    template_name = 'new_post.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewPostView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.submitted_by = self.request.user
        new_post.is_published = True
        new_post.save()
        self.object = new_post

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super(PostDetailView, self).get_context_data(**kwargs)
        submission_comments = Comment.objects.filter(commented_on=self.object, in_reply_to__isnull=True)
        ctx['comments'] = submission_comments
        ctx['comment_form'] = CommentModelForm(initial={'link_pk': self.object.pk})
        return ctx


class NewCommentView(CreateView):
    form_class = CommentModelForm
    http_method_names = ('post',)
    template_name = 'comment.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        parent_post = Post.objects.get(pk=form.cleaned_data['link_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_post
        new_comment.commented_by = self.request.user
        new_comment.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': parent_post.pk}))

    def get_initial(self):
        initial_data = super(NewCommentView, self).get_initial()
        initial_data['link_pk'] = self.request.GET['link_pk']

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentView, self).get_context_data(**kwargs)
        ctx['post'] = Post.objects.get(pk=self.request.GET['link_pk'])
        return ctx


class NewCommentReplyView(CreateView):
    form_class = CommentModelForm
    template_name = 'comment_reply.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCommentReplyView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(NewCommentReplyView, self).get_context_data(**kwargs)
        ctx['parent_comment'] = Comment.objects.get(pk=self.request.GET['parent_comment_pk'])
        return ctx

    def get_initial(self):
        initial_data = super(NewCommentReplyView, self).get_initial()
        link_pk = self.request.GET['link_pk']
        initial_data['link_pk'] = link_pk
        parent_comment_pk = self.request.GET['parent_comment_pk']
        initial_data['parent_comment_pk'] = parent_comment_pk
        return initial_data

    def form_valid(self, form):
        parent_post = Post.objects.get(pk=form.cleaned_data['link_pk'])
        parent_comment = Comment.objects.get(pk=form.cleaned_data['parent_comment_pk'])
        new_comment = form.save(commit=False)
        new_comment.commented_on = parent_post
        new_comment.in_reply_to = parent_comment
        new_comment.commented_by = self.request.user
        new_comment.save()
        return HttpResponseRedirect(reverse('post-detail', kwargs={'pk': parent_post.pk}))


class UpvotePostView(View):
    def get(self, request, link_pk, **kwargs):
        post = Post.objects.get(pk=link_pk)
        post.upvotes.add(request.user)
        return HttpResponseRedirect(reverse('dashboard'))


class RemoveUpvoteFromPostView(View):
    def get(self, request, link_pk, **kwargs):
        post = Post.objects.get(pk=link_pk)
        post.upvotes.remove(request.user)
        return HttpResponseRedirect(reverse('dashboard'))
