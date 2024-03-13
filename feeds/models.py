from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import serializers


User = get_user_model()


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class PostFile(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    file = models.FileField(upload_to="post_files/", blank=True, null=True)
    file_type = models.CharField(max_length=100, null=True)

    def to_dict(self):
        return {"file_id": self.id, "file": self.file.url, "file_type": self.file_type}


class CommentFile(models.Model):
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    file = models.FileField(upload_to="comment_files/", blank=True, null=True)
    file_type = models.CharField(max_length=100, null=True)

    def to_dict(self):
        return {"file_id": self.id, "file": self.file.url, "file_type": self.file_type}


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text_content = models.TextField(null=True)

    file = models.ManyToManyField(
        PostFile,
        blank=True,
        related_name="post_files",
    )

    location = models.CharField(max_length=255, blank=True, null=True)

    comments = models.ManyToManyField("Comment", related_name="post_comments")
    reactions = models.ManyToManyField("PostReaction", related_name="post_reactions")

    hashtags = models.ManyToManyField(Hashtag, blank=True)

    is_business_post = models.BooleanField(default=False, verbose_name="Business Post")

    is_personal_post = models.BooleanField(default=True, verbose_name="Personal Post")

    is_repost = models.BooleanField(default=False)

    repost = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    tagged_users = models.ManyToManyField(
        User, related_name="tagged_in_posts", blank=True
    )

    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    love_count = models.PositiveIntegerField(default=0)
    sad_count = models.PositiveIntegerField(default=0)
    angry_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_post_reactions(self):

        return {
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "love_count": self.love_count,
            "sad_count": self.sad_count,
            "angry_count": self.angry_count,
        }

    def get_files(self):

        return [file.to_dict() for file in self.file.all()]

    def get_repost(self):

        return self.repost.to_dict() if self.repost else None

    def to_dict(self):

        class TaggedUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ("id", "username")

        class HashtagSerializer(serializers.ModelSerializer):
            class Meta:
                model = Hashtag
                fields = ("name",)

        class UserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ("id", "username", "email", )

        tagged_user_serializer = TaggedUserSerializer(
            self.tagged_users.all(), many=True
        )

        hashtags_serializer = HashtagSerializer(self.hashtags.all(), many=True)

        user_serializer = UserSerializer(self.user)

        return {
            "id": self.id,
            "user": dict(user_serializer.data),
            "text_content": self.text_content,
            "files": self.get_files(),
            "location": self.location,
            "hashtags": hashtags_serializer.data,
            "tagged_users": tagged_user_serializer.data,
            "reaction": self.get_total_post_reactions(),
            "is_business_post": self.is_business_post,
            "is_personal_post": self.is_business_post,
            "is_repost": self.is_repost,
            "repost": self.get_repost(),
            "created_at": str(self.created_at),
        }


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    text_content = models.TextField()

    file = models.ForeignKey(
        CommentFile,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="comment_files",
    )
    reactions = models.ManyToManyField(
        "CommentReaction", related_name="comment_reactions"
    )
    replies = models.ManyToManyField("Reply", related_name="comment_replies")

    created_at = models.DateTimeField(auto_now_add=True)

    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    love_count = models.PositiveIntegerField(default=0)
    sad_count = models.PositiveIntegerField(default=0)
    angry_count = models.PositiveIntegerField(default=0)

    def get_reactions(self):

        return {
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "love_count": self.love_count,
            "sad_count": self.sad_count,
            "angry_count": self.angry_count,
        }

    def get_file(self):

        return self.file.to_dict() if self.file else None

    def to_dict(self):

        class TaggedUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ("id", "username")

        tagged_user = TaggedUserSerializer(self.user)

        return {
            "id": self.id,
            "post": self.post.id,
            "user": dict(tagged_user.data),
            "text_content": self.text_content,
            "file": self.get_file(),
            "reactions": self.get_reactions(),
            "created_at": str(self.created_at),
        }



class PostReaction(models.Model):
    LIKE = 1
    DISLIKE = 2
    LOVE = 3
    SAD = 4
    ANGRY = 5

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (LOVE, "Love"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_reactions"
    )
    reaction_type = models.SmallIntegerField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_user_reaction(self):

        return {
            "user": self.user.get_username(),
            "reaction_type": self.reaction_type,
        }

    def to_dict(self):

        return {
            "c": self.post.id,
            "user": self.user.id,
            "reaction_type": self.reaction_type,
            "created_at": str(self.created_at),
        }


class CommentReaction(models.Model):
    LIKE = 1
    DISLIKE = 2
    LOVE = 3
    SAD = 4
    ANGRY = 5

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (LOVE, "Love"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="comment_reactions"
    )
    reaction_type = models.SmallIntegerField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):

        return {
            "reaction_id": self.id,
            "comment": self.comment.id,
            "user": self.user.id,
            "reaction_type": self.reaction_type,
            "created_at": str(self.created_at),
        }


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text_content = models.TextField()
    reactions = models.ManyToManyField("ReplyReaction", related_name="reply_reactions")
    created_at = models.DateTimeField(auto_now_add=True)

    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    love_count = models.PositiveIntegerField(default=0)
    sad_count = models.PositiveIntegerField(default=0)
    angry_count = models.PositiveIntegerField(default=0)

    def get_reactions(self):

        return {
            "like_count": self.like_count,
            "dislike_count": self.dislike_count,
            "love_count": self.love_count,
            "sad_count": self.sad_count,
            "angry_count": self.angry_count,
        }

    def to_dict(self):

        return {
            "id": self.id,
            "comment": self.comment.id,
            "user": self.user.id,
            "text_content": self.text_content,
            "reactions": self.get_reactions(),
            "created_at": str(self.created_at),
        }


class ReplyReaction(models.Model):
    LIKE = 1
    DISLIKE = 2
    LOVE = 3
    SAD = 4
    ANGRY = 5

    REACTION_CHOICES = [
        (LIKE, "Like"),
        (DISLIKE, "Dislike"),
        (LOVE, "Love"),
        (SAD, "Sad"),
        (ANGRY, "Angry"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey(
        Reply, on_delete=models.CASCADE, related_name="reply_reactions"
    )
    reaction_type = models.SmallIntegerField(choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "reaction_id": self.id,
            "reply": self.reply.id,
            "user": self.user.id,
            "reaction_type": self.reaction_type,
            "created_at": str(self.created_at),
        }


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):

        return {
            "id": self.id,
            "user": self.user.id,
            "post": self.post.to_dict(),
            "created_at": str(self.created_at),
        }


class SharePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=True, null=True)
    shared_post = models.ForeignKey("Post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField()
    file = models.FileField(upload_to="status_files/", blank=True)

    tagged_users = models.ManyToManyField(
        User, related_name="tagged_in_status", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):

        class TaggedUserSerializer(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ("id", "username")

        tagged_user_serializer = TaggedUserSerializer(
            self.tagged_users.all(), many=True
        )

        return {
            "id": self.id,
            "caption": self.caption,
            "tagged_users": tagged_user_serializer.data,
            "file": self.file.url,
            "created_at": self.created_at,
        }


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, blank=True, on_delete=models.CASCADE, related_name="user_friends"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):

        return {"user": self.user.id, "friend": self.friend.id}


class ReportPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class BlockedUsers(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocked_users_set"
    )
    blocked_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="blocked_by_set"
    )
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked_user}"

    def to_dict(self):

        return {
            "blocked_user": self.blocked_user.id,
            "created_at": str(self.created_at),
        }







class PromotedPostManager(models.Manager):
    def get_promoted_posts(self):
        now = timezone.now()
        return self.filter(expired_at__gt=now)


class PromotedPost(models.Model):

    BASIC = 1
    STANDARD = 2
    PREMIUM = 3
    PRO = 4

    PLAN_CHOICES = [
        (BASIC, "Basic"),
        (STANDARD, "Standard"),
        (PREMIUM, "Premium"),
        (PRO, "Pro"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    plan = models.SmallIntegerField(choices=PLAN_CHOICES)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


    objects = PromotedPostManager()

    def isexpired(self):

        now = timezone.now()

        return self.expired_at > now

    def save(self, *args, **kwargs):

        if not self.created_at:
            self.created_at = timezone.now()

        plan_validity = {
            self.BASIC: timedelta(days=1),
            self.STANDARD: timedelta(days=7),
            self.PREMIUM: timedelta(days=14),
            self.PRO: timedelta(days=30),
        }

        self.expired_at = self.created_at + plan_validity.get(self.plan, timedelta(days=1))

        super().save(*args, **kwargs)

    def to_dict(self):

        return {
            "id": self.id,
            "user": self.user.id,
            "post": self.post.to_dict(),
            "is_promotion_expired": self.isexpired(),
            "description": self.description,
            "created_at": self.created_at,
            "expired_at": self.expired_at,
        }
