from django.db import models


# Create your models here.
class Blog(models.Model):

    class Meta:
        db_table = "blogs"

    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        db_table = "comments"

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return self.comment
