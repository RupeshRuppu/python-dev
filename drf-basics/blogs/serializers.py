from .models import Blog, Comment
from rest_framework.serializers import ModelSerializer


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class BlogSerializer(ModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Blog
        fields = "__all__"
