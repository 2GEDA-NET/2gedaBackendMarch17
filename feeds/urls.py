from django.urls import path

from . import api

app_name = "feeds"

urlpatterns = [
    path("posts/", api.PostListAPIView.as_view(), name="all_post_on_feed"),
    path("post/", api.PostAPIView.as_view(), name="post_feed"),
    path("post/<int:post_id>/", api.SinglePostView.as_view(), name="post_single"),
    path(
        "post/<int:post_id>/comments/",
        api.CommentPostAPIView.as_view(),
        name="comment_on_post",
    ),
    path(
        "post/<int:post_id>/comments/<int:comment_id>/",
        api.SingleCommentAPIView.as_view(),
        name="comment-single",
    ),
    path(
        "post/<int:post_id>/comments/<int:comment_id>/reactions/",
        api.ReactionCommentView.as_view(),
        name="reaction_on_comment",
    ),


    path(
        "post/<int:post_id>/comments/<int:comment_id>/replies/",
        api.ReplyCommentView.as_view(),
        name="replies_on_comment",
    ),

    path(
        "post/<int:post_id>/comments/<int:comment_id>/replies/<int:reply_id>/",
        api.SingleReplyView.as_view(),
        name="reaction-single",
    ),

    path(
        "post/<int:post_id>/comments/<int:comment_id>/replies/<int:reply_id>/reactions/",
        api.SingleReplyReactionView.as_view(),
        name="reaction_on_reply",
    ),

    path(
        "post/<int:post_id>/reactions/",
        api.ReactionPostView.as_view(),
        name="reaction_on_post",
    ),

    path(
        "post/<int:post_id>/file/",
        api.AddFilePostAPIView.as_view(),
        name="add_file_on_post",
    ),
    path(
        "post/<int:post_id>/file/<int:file_id>/",
        api.SingleFilePostAPIView.as_view(),
        name="single_file_on_post",
    ),
    path("post/save/", api.SavedPostAPIView.as_view(), name="saved_post"),
    path("post/<int:post_id>/save/", api.SavePostAPIView.as_view(), name="save_post"),
    path("post/report/", api.ReportPostAPIView.as_view(), name="report_post"),
    path("friends/", api.FriendsAPIView.as_view(), name="feeds_friends"),
    path("status/", api.StatusAPIView.as_view(), name="status_friends"),
    path(
        "status/<int:status_id>/",
        api.SingleStatusAPIView.as_view(),
        name="status_friends",
    ),
]
