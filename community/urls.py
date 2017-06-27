from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import NewPostView, PostDetailView, NewCommentView, NewCommentReplyView, HomeView, UpvotePostView, \
    RemoveUpvoteFromPostView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='dashboard'),
    url(r'^new-post/$', NewPostView.as_view(), name='new-post'),
    url(r'^post/(?P<pk>\d+)/$', PostDetailView.as_view(), name='post-detail'),
    url(r'new-comment/$', NewCommentView.as_view(), name='new-comment'),
    url(r'new-comment-reply/$', NewCommentReplyView.as_view(), name='new-comment-reply'),
    url(r'^upvote/(?P<link_pk>\d+)/$', UpvotePostView.as_view(), name='upvote-submission'),
    url(r'^upvote/(?P<link_pk>\d+)/remove/$', RemoveUpvoteFromPostView.as_view(), name='remove-upvote'),
]
